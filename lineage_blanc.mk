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

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_NAME := lineage_blanc
PRODUCT_DEVICE := blanc
PRODUCT_MANUFACTURER := HUAWEI
PRODUCT_BRAND := HUAWEI
PRODUCT_MODEL := BLA-L29

PRODUCT_BUILD_PROP_OVERRIDES += \
    DeviceProduct=BLA-L29
