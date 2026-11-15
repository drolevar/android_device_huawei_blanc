#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from the common OEM chipset makefile.
$(call inherit-product, device/huawei/kirin970-common/common.mk)

# Current BLA .225 stock Android reports ro.product.first_api_level=26.
# Override the common donor's launch API without changing its VNDK selection.
PRODUCT_SHIPPING_API_LEVEL := 26

# AAPT
PRODUCT_AAPT_CONFIG := normal
PRODUCT_AAPT_PREF_CONFIG := xxhdpi

# Boot animation
TARGET_SCREEN_HEIGHT := 2160
TARGET_SCREEN_WIDTH := 1080

# BLA gralloc requires ion_open/ion_alloc_fd; the platform default is a stub.
# Select Lineage's real ION provider for this device's existing kernel allocator.
$(call soong_config_set_bool,libion,legacy_impl,true)

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
