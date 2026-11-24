#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/huawei/blanc

# BLA-L29 EMUI 12 .225: measured super capacity, confirmed by stock LP
# metadata block_devices[super].size and super_device.total_size.
# Capture provenance and limitations: docs/BLA-225-EVIDENCE.md.
BOARD_SUPER_PARTITION_SIZE := 5771362304

# Include the common OEM chipset BoardConfig.
include device/huawei/kirin970-common/BoardConfigCommon.mk

# Measured BLA .225 stock kernel AVB hash descriptor names the kernel partition.
# This does not change signing, partition capacity or the separate ramdisk rules.
BOARD_HUAWEI_KERNEL_AVB_PARTITION_NAME := kernel
# Measured BLA .225 stock ramdisk AVB hash descriptor names the ramdisk partition.
BOARD_HUAWEI_RAMDISK_AVB_PARTITION_NAME := ramdisk

# Keep warning/notice/info messages in the console (including pstore when its
# backend is registered) during bring-up. The inherited level 4 hides these.
# This changes console filtering, not printk's ring buffer or ADB permissions.
ifneq ($(filter userdebug eng,$(TARGET_BUILD_VARIANT)),)
BOARD_KERNEL_CMDLINE := $(filter-out loglevel=%,$(BOARD_KERNEL_CMDLINE)) loglevel=7
endif

# Display
TARGET_SCREEN_DENSITY := 420

# ODM
ODM_MANIFEST_SKUS := \
    BLA-L09 \
    BLA-L29

ODM_MANIFEST_BLA-L09_FILES := $(DEVICE_PATH)/odm/manifest_BLA-L09.xml
ODM_MANIFEST_BLA-L29_FILES := $(DEVICE_PATH)/odm/manifest_BLA-L29.xml

# Wi-Fi (BCM4359 STA / SoftAP firmware reload paths from /proc/device-tree/bcm_wifi)
WIFI_DRIVER_FW_PATH_PARAM := "/sys/module/bcmdhd/parameters/firmware_path"
WIFI_DRIVER_FW_PATH_STA := "/vendor/firmware/fw_bcm4359_hw.bin"
WIFI_DRIVER_FW_PATH_AP := "/vendor/firmware/fw_bcm4359_apsta_hw.bin"
WIFI_DRIVER_FW_PATH_P2P := "/vendor/firmware/fw_bcm4359_hw.bin"

# Require the proprietary files BoardConfig from the reviewed BLA extraction.
include vendor/huawei/blanc/BoardConfigVendor.mk
