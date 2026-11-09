#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/huawei/blanc

# Donor geometry inherited from Berkeley. This is NOT a measured BLA-L29
# EMUI 12 .225 capacity. Replace only after the firmware inventory described
# in README.md; this preparation branch is not an installable device port.
BOARD_SUPER_PARTITION_SIZE := 4848615424

# Include the common OEM chipset BoardConfig.
include device/huawei/kirin970-common/BoardConfigCommon.mk

# Display
TARGET_SCREEN_DENSITY := 420

# ODM
ODM_MANIFEST_SKUS := \
    BLA-L09 \
    BLA-L29

ODM_MANIFEST_BLA-L09_FILES := $(DEVICE_PATH)/odm/manifest_BLA-L09.xml
ODM_MANIFEST_BLA-L29_FILES := $(DEVICE_PATH)/odm/manifest_BLA-L29.xml

# Require the proprietary files BoardConfig from the reviewed BLA extraction.
include vendor/huawei/blanc/BoardConfigVendor.mk
