#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from the common OEM chipset makefile.
$(call inherit-product, device/huawei/kirin970-common/common.mk)

# AAPT
PRODUCT_AAPT_CONFIG := normal
PRODUCT_AAPT_PREF_CONFIG := xxhdpi

# Boot animation
TARGET_SCREEN_HEIGHT := 2160
TARGET_SCREEN_WIDTH := 1080

# Init
PRODUCT_PACKAGES += \
    init.hisi.odm.rc

# Keylayout
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/fingerprint.kl:$(TARGET_COPY_OUT_VENDOR)/usr/keylayout/fingerprint.kl

# Overlay
PRODUCT_PACKAGES += \
    FrameworksOverlayBLA

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# Sensors
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/android.hardware.sensor.unavailable.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.sensor.unavailable.xml

# The product requires a reviewed BLA blob extraction; a missing vendor tree
# must fail configuration instead of producing a silently incomplete product.
$(call inherit-product, vendor/huawei/blanc/blanc-vendor.mk)
