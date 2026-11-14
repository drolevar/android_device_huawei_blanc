# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

"""Host fixtures only; put the selected tools/extract-utils on PYTHONPATH."""

import io
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from extract_utils.file import File, FileList
from extract_utils.fixups_blob import BlobFixupCtx
from extract_utils.makefiles import (
    MakefilesCtx,
    ProductPackagesCtx,
    file_stem_package_name,
    write_product_copy_files,
)
from extract_utils.source import DiskSource
from extract_utils.prohibited_files import check_prohibited_file


DEVICE = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(DEVICE / 'extract-files.py'))['module']


class ExtractionTest(unittest.TestCase):
    def apply_fixup(self, name, content):
        fixup = MODULE.blob_fixups.get(name)
        self.assertIsNotNone(fixup, f'No BLA fixup for {name}')
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'fixture.xml'
            target.write_bytes(content)
            fixup.run(BlobFixupCtx(str(DEVICE)), File(name), str(target))
            return target.read_bytes()

    def test_bla_sensor_xml_parses_after_encoding_and_comment_repairs(self):
        # Synthetic XML exercises the BLA paths absent from the BKL recipe.
        fixture = (b'<?xml version="1.0" encoding="GB2312"?>'
                   b'<camera><!-- bad L-R-Ev comment --><value>\xe9</value></camera>')
        for sensor in ['imx219', 'imx319', 'imx386dual']:
            with self.subTest(sensor=sensor):
                result = self.apply_fixup(
                    f'odm/etc/camera/davinci/{sensor}/imgproc.xml', fixture)
                self.assertEqual(ET.fromstring(result).find('value').text, '\xe9')
                self.assertIn(b'<value>\xe9</value>', result)

    def test_xml_without_encoding_preserves_legacy_bytes(self):
        result = self.apply_fixup(
            'odm/etc/camera/hdccalib/hw_calib_setting.xml',
            b'<?xml version="1.0"?><camera><value>\xe9</value></camera>')
        self.assertEqual(ET.fromstring(result).find('value').text, '\xe9')

    def test_hdr_mismatched_tag_and_comments_parse_after_repairs(self):
        result = self.apply_fixup(
            'odm/etc/display/effect/algorithm/hdr_engine.xml',
            b'<?xml version="1.0" encoding="gb2312"?>'
            b'<hdr><subversion>1</subverison><!-- default --->'
            b'<!-- default-><!-- outdoor-></hdr>')
        self.assertEqual(ET.fromstring(result).find('subversion').text, '1')

    def test_inventory_installs_media_and_nfc_at_existing_vendor_consumers(self):
        files = FileList(check_elf=True)
        files.add_from_file(str(DEVICE / 'proprietary-files.txt'))
        out = io.StringIO()
        ctx = MakefilesCtx(False, io.StringIO(), io.StringIO(), out, io.StringIO())
        packages = ProductPackagesCtx(True, 'huawei', '/unused',
                                      'vendor/huawei/blanc/proprietary',
                                      'proprietary', {})
        write_product_copy_files(ctx, packages, files.copy_files)
        for destination in ['etc/media_profiles_V1_0.xml', 'etc/libnfc-nci.conf',
                            'etc/libnfc-nxp.conf', 'libnfc-nxp_RF.conf']:
            self.assertTrue(f':$(TARGET_COPY_OUT_VENDOR)/{destination}' in out.getvalue(),
                            f'Missing generated vendor copy rule for {destination}')

    def test_odm_gps_module_does_not_collide_with_common_vendor_gps(self):
        files = FileList(check_elf=True)
        files.add_from_file(str(DEVICE / 'proprietary-files.txt'))
        selected = {f.dst: f for f in files.all_files}
        for base in ['gps.default', 'gps47531.default']:
            name = f'odm/lib64/hw/{base}.so'
            with self.subTest(name=name):
                self.assertTrue(name in selected, f'Missing ODM GPS candidate {name}')
                stem, module_name = file_stem_package_name(selected[name], can_have_stem=True)
                self.assertEqual(stem, base)
                self.assertEqual(module_name, base + '_blanc')

    def test_every_fixup_targets_an_extracted_destination(self):
        files = FileList(check_elf=True)
        files.add_from_file(str(DEVICE / 'proprietary-files.txt'))
        destinations = {f.dst for f in files.all_files}
        self.assertEqual(set(MODULE.blob_fixups) - destinations, set())

    def test_media_remap_prefers_odm_when_both_source_paths_exist(self):
        files = FileList(check_elf=True)
        files.add_from_file(str(DEVICE / 'proprietary-files.txt'))
        media = files.get_file('vendor/etc/media_profiles_V1_0.xml')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, content in [(media.src, b'BLA ODM'), (media.dst, b'other vendor')]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            target = root / 'copied.xml'
            self.assertTrue(DiskSource(str(root)).copy_file_to_path(media, str(target)))
            self.assertEqual(target.read_bytes(), b'BLA ODM')

    def test_camera_native_fixups_replace_only_the_required_dependency(self):
        # Build a tiny host ELF, not a proprietary or handset executable.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dependency = root / 'libstdc++.so'
            subprocess.run(['cc', '-shared', '-nostdlib', '-x', 'c', '-',
                            '-Wl,-soname,libstdc++.so', '-o', str(dependency)],
                           input=b'void fixture(void) {}', check=True, capture_output=True)
            for name in ['libarcsoft_beautyshot.so', 'libmrc_cg_beauty.so', 'libvidhance.so']:
                with self.subTest(name=name):
                    target = root / name
                    subprocess.run(['cc', '-shared', '-nostdlib', '-x', 'c', '-',
                                    '-Wl,--no-as-needed', '-L' + tmp, '-lstdc++',
                                    '-Wl,-soname,' + name, '-o', str(target)],
                                   input=b'void fixture_user(void) {}', check=True,
                                   capture_output=True)
                    MODULE.fixup_module_file(File('odm/lib64/' + name), str(target))
                    dynamic = subprocess.check_output(['readelf', '-d', str(target)], text=True)
                    self.assertIn('[libstdc++_vendor.so]', dynamic)
                    self.assertNotIn('[libstdc++.so]', dynamic)
                    self.assertIn('[' + name + ']', dynamic)

    def test_native_inventory_passes_default_extractor_filename_checks(self):
        files = FileList(check_elf=True)
        files.add_from_file(str(DEVICE / 'proprietary-files.txt'))
        blocked = []
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / 'synthetic.so'
            fixture.write_bytes(b'synthetic megface megvii MEGVII marker')
            for file in files.all_files:
                if file.ext != '.so':
                    continue
                try:
                    check_prohibited_file(file.dst, str(fixture))
                except SystemExit:
                    blocked.append(file.dst)
        self.assertEqual(blocked, [])


if __name__ == '__main__':
    unittest.main()
