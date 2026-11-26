#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from the common OEM chipset makefile.
$(call inherit-product, device/huawei/kirin970-common/common.mk)

# Current BLA .225 stock Android reports ro.product.first_api_level=26.
# Override the common donor's launch API without changing its VNDK selection.
PRODUCT_SHIPPING_API_LEVEL := 26

# Debug builds retain Android startup logs once encrypted /data is available.
# Use the platform logcatd service; its normal init gate prevents early writes.
# Eight 1 MiB rotated files plus the active file; kernel/pstore covers earlier
# failures only when its backend is registered. Do not change ADB authentication.
ifneq ($(filter userdebug eng,$(TARGET_BUILD_VARIANT)),)
PRODUCT_SYSTEM_PROPERTIES += \
    logd.logpersistd=logcatd \
    logd.logpersistd.buffer=main,system,crash,events,kernel \
    logd.logpersistd.size=8 \
    logd.logpersistd.rotate_kbytes=1024
endif

# AAPT
PRODUCT_AAPT_CONFIG := normal
PRODUCT_AAPT_PREF_CONFIG := xxhdpi

# Boot animation
TARGET_SCREEN_HEIGHT := 2160
TARGET_SCREEN_WIDTH := 1080

# BLA gralloc requires ion_open/ion_alloc_fd; the platform default is a stub.
# Select Lineage's real ION provider for this device's existing kernel allocator.
$(call soong_config_set_bool,libion,legacy_impl,true)

# Camera (Huawei .225 service interposer, CameraX Basic Extensions, Aperture 1x/2x RRO)
PRODUCT_SYSTEM_PROPERTIES += \
    ro.camerax.extensions.enabled=true

PRODUCT_VENDOR_PROPERTIES += \
    ro.camera.notify_nfc=1

DEVICE_PACKAGE_OVERLAYS += \
    $(LOCAL_PATH)/overlay-lineage

# Init & Camera
PRODUCT_PACKAGES += \
    init.hisi.odm.rc \
    hicam.hal.service \
    androidx.camera.extensions.impl.blanc \
    huawei_blanc_camera_extensions.xml \
    libshim_camera_tls \
    libtinyxml2-v29

# Keylayout
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/fingerprint.kl:$(TARGET_COPY_OUT_VENDOR)/usr/keylayout/fingerprint.kl

# Overlay
PRODUCT_PACKAGES += \
    FrameworksOverlayBLA \
    NfcOverlayBLA

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# Sensors
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/android.hardware.sensor.unavailable.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/android.hardware.sensor.unavailable.xml

# Telephony
PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.telephony.cdma.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.cdma.xml \
    frameworks/native/data/etc/android.hardware.telephony.gsm.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.gsm.xml \
    frameworks/native/data/etc/android.hardware.telephony.ims.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.ims.xml

# The product requires a reviewed BLA blob extraction; a missing vendor tree
# must fail configuration instead of producing a silently incomplete product.
$(call inherit-product, vendor/huawei/blanc/blanc-vendor.mk)
