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


if __name__ == "__main__":
    unittest.main()
