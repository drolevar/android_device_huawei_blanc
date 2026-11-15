# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

"""Host-only config and retained-provider checks; requires ANDROID_BUILD_TOP.

This does not run Soong, load a vendor blob or invoke a real device ioctl.
BLA_ION_TEST_PROVIDER=ion.c reproduces the platform failure-stub control.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


DEVICE = Path(__file__).resolve().parents[1]


def platform_root():
    value = os.environ.get('ANDROID_BUILD_TOP')
    if not value:
        raise unittest.SkipTest('Set ANDROID_BUILD_TOP to the resolved platform checkout')
    return Path(value).resolve()


class IonProductTest(unittest.TestCase):
    def test_blanc_requests_a_typed_real_ion_provider(self):
        root = platform_root()
        config = (root / 'build/make/core/config.mk').read_text()
        definitions = []
        for name in ['soong_config_define_internal', 'soong_config_set_bool']:
            found = re.findall(r'^define ' + name + r'\n.*?^endef', config, re.M | re.S)
            self.assertEqual(len(found), 1, f'Unrecognized platform macro: {name}')
            definitions.append(found[0])
        fixture = '\n'.join(definitions) + f'''
define inherit-product
endef
include {DEVICE}/device.mk
.PHONY: report
report:
\t@printf '%s\\n' '$(SOONG_CONFIG_libion_legacy_impl)' '$(SOONG_CONFIG_TYPE_libion_legacy_impl)' '$(SOONG_CONFIG_NAMESPACES)' '$(SOONG_CONFIG_libion)'
'''
        result = subprocess.run(['make', '--no-print-directory', '-f', '-', 'report'],
                                input=fixture, text=True, capture_output=True, timeout=15,
                                check=True)
        value, kind, namespaces, variables = result.stdout.splitlines()
        self.assertEqual(value, 'true', 'BLA gralloc needs working ion_open/ion_alloc_fd')
        self.assertEqual(kind, 'bool', 'Blueprint select requires a boolean, not a string')
        self.assertIn('libion', namespaces.split())
        self.assertIn('legacy_impl', variables.split())


class IonProviderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = platform_root()
        provider = os.environ.get('BLA_ION_TEST_PROVIDER', 'ion_legacy.c')
        if provider not in {'ion.c', 'ion_legacy.c'}:
            raise ValueError('Provider must be ion.c or ion_legacy.c')
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.binary = Path(temporary.name) / 'ion-contract'
        ion = root / 'system/memory/libion'
        compiler = os.environ.get('BLA_TEST_CC', 'cc')
        command = [compiler, '-std=gnu23', '-D_GNU_SOURCE', '-O1',
                   '-ffunction-sections', '-fdata-sections',
                   '-I' + str(ion / 'include_legacy'),
                   '-I' + str(ion / 'kernel-headers'),
                   '-I' + str(root / 'system/logging/liblog/include'),
                   str(ion / provider), str(DEVICE / 'tests/ion_contract.c'),
                   '-Wl,--gc-sections,--wrap=open,--wrap=close,--wrap=ioctl',
                   '-o', str(cls.binary)]
        compiled = subprocess.run(command, capture_output=True, text=True, timeout=60)
        if compiled.returncode:
            raise AssertionError(compiled.stderr)
        output = os.environ.get('BLA_ION_TEST_OUTPUT')
        if output:
            dest = Path(output)
            dest.mkdir(parents=True, exist_ok=True)
            copied = dest / 'ion-contract'
            shutil.copy2(cls.binary, copied)
            inputs = [ion / provider, DEVICE / 'tests/ion_contract.c',
                      ion / 'include_legacy/ion/ion.h',
                      ion / 'kernel-headers/linux/ion_4.19.h']
            record = {'scope': 'Host source fixture with wrapped I/O; no actual kernel/device access',
                      'provider': provider, 'command': command, 'exit_status': 0,
                      'compiler': subprocess.check_output([compiler, '--version'], text=True),
                      'inputs': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                      'artifact': {'path': str(copied),
                                   'sha256': hashlib.sha256(copied.read_bytes()).hexdigest()}}
            (dest / 'build-receipt.json').write_text(json.dumps(record, indent=2) + '\n')

    def check_case(self, name):
        result = subprocess.run([str(self.binary), name], capture_output=True,
                                text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_modern_ioctl_preserves_size_mask_flags_and_returns_buffer_fd(self):
        self.check_case('allocation')

    def test_open_denial_is_reported_before_any_ioctl(self):
        self.check_case('open_error')

    def test_allocation_error_preserves_output_fd(self):
        self.check_case('allocation_error')

    def test_null_output_does_not_invoke_ioctls(self):
        self.check_case('null_output')

    def test_close_error_returns_negative_errno(self):
        self.check_case('close_error')


if __name__ == '__main__':
    unittest.main()
