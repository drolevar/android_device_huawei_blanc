# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
"""Evaluate actual BLA/common/vendor BoardConfig includes using GNU Make."""
import os
from pathlib import Path
import subprocess
import unittest


class KernelDescriptorConfigTest(unittest.TestCase):
    def test_all_variants_select_measured_kernel_name_without_capacity_change(self):
        top = os.environ.get("ANDROID_BUILD_TOP")
        if not top:
            self.skipTest("Set ANDROID_BUILD_TOP to evaluate actual product includes")
        device = Path(os.environ.get("BLA_TEST_DEVICE_TREE", Path(__file__).resolve().parents[1]))
        for variant in ("user", "userdebug", "eng"):
            with self.subTest(variant=variant):
                source = (f"TARGET_BUILD_VARIANT := {variant}\n"
                          f"include {device / 'BoardConfig.mk'}\n"
                          "$(info descriptor=$(BOARD_HUAWEI_KERNEL_AVB_PARTITION_NAME))\n"
                          "$(info ramdisk_descriptor=$(BOARD_HUAWEI_RAMDISK_AVB_PARTITION_NAME))\n"
                          "$(info capacity=$(BOARD_BOOTIMAGE_PARTITION_SIZE))\n"
                          "$(info ramdisk_capacity=$(BOARD_BOOT_RAMDISKIMAGE_PARTITION_SIZE))\n"
                          "$(info header=$(BOARD_BOOT_HEADER_VERSION))\n"
                          "all:\n\t@:\n")
                proc = subprocess.run(["make", "-rR", "-s", "-f", "-"],
                                      input=source, cwd=top, text=True,
                                      capture_output=True, timeout=20)
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                values = dict(line.split("=", 1) for line in proc.stdout.splitlines() if "=" in line)
                self.assertEqual(values["descriptor"], "kernel")
                self.assertEqual(values["ramdisk_descriptor"], "ramdisk")
                self.assertEqual(values["capacity"], "25165824")
                self.assertEqual(values["ramdisk_capacity"], "2097152")
                self.assertEqual(values["header"], "1")

    def test_lineage_blanc_debug_props_scoped_to_non_user(self):
        top = os.environ.get("ANDROID_BUILD_TOP")
        if not top:
            self.skipTest("Set ANDROID_BUILD_TOP to evaluate actual product includes")
        device = Path(os.environ.get("BLA_TEST_DEVICE_TREE", Path(__file__).resolve().parents[1]))
        for variant in ("userdebug", "eng", "user"):
            with self.subTest(variant=variant):
                source = (
                    f"TARGET_BUILD_VARIANT := {variant}\n"
                    "SRC_TARGET_DIR := build/make/target\n"
                    "define inherit-product\n"
                    "$(if $(filter vendor/lineage/config/common_full_phone.mk,$(1)),$(eval include vendor/lineage/config/common.mk))\n"
                    "endef\n"
                    "PRODUCT_NOT_DEBUGGABLE_IN_USERDEBUG := preset\n"
                    f"include {device / 'lineage_blanc.mk'}\n"
                    "$(info adb_insecure=$(WITH_ADB_INSECURE))\n"
                    "$(info not_dbg=$(PRODUCT_NOT_DEBUGGABLE_IN_USERDEBUG))\n"
                    "$(info sys_ext=$(PRODUCT_SYSTEM_EXT_PROPERTIES))\n"
                    "$(info sys_def=$(PRODUCT_SYSTEM_DEFAULT_PROPERTIES))\n"
                    "all:\n\t@:\n"
                )
                proc = subprocess.run(
                    ["make", "-rR", "-s", "-f", "-"],
                    input=source,
                    cwd=top,
                    text=True,
                    capture_output=True,
                    timeout=20,
                )
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                values = dict(line.split("=", 1) for line in proc.stdout.splitlines() if "=" in line)
                if variant == "user":
                    self.assertEqual(values["adb_insecure"], "")
                    self.assertNotIn("ro.adb.secure=0", values["sys_def"].split())
                    self.assertNotIn("ro.adb.secure=0", values["sys_ext"].split())
                else:
                    self.assertEqual(values["adb_insecure"], "true")
                    self.assertEqual(values["not_dbg"], "")
                    self.assertIn("ro.adb.secure=0", values["sys_ext"].split())
                    self.assertNotIn("ro.adb.secure=1", values["sys_ext"].split())
                    self.assertIn("ro.adb.secure=0", values["sys_def"].split())
                    self.assertIn("persist.sys.usb.config=adb", values["sys_def"].split())


if __name__ == "__main__":
    unittest.main()
