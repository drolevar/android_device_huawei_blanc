#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/non_ab_device.mk)

# Inherit from blanc device
$(call inherit-product, device/huawei/blanc/device.mk)

# Bring-up diagnostics: keep userdebug/eng debuggable (ro.debuggable=1, ro.adb.secure=0)
# with early root USB adbd while preserving standard user security defaults.
ifneq ($(TARGET_BUILD_VARIANT),user)
WITH_ADB_INSECURE := true
endif

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

ifneq ($(TARGET_BUILD_VARIANT),user)
PRODUCT_NOT_DEBUGGABLE_IN_USERDEBUG :=
PRODUCT_SYSTEM_DEFAULT_PROPERTIES += \
    ro.adb.secure=0 \
    persist.sys.usb.config=adb
endif

PRODUCT_NAME := lineage_blanc
PRODUCT_DEVICE := blanc
PRODUCT_MANUFACTURER := HUAWEI
PRODUCT_BRAND := HUAWEI
PRODUCT_MODEL := BLA-L29

PRODUCT_BUILD_PROP_OVERRIDES += \
    DeviceProduct=BLA-L29
