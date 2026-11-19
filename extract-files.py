#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/huawei',
    'vendor/huawei/kirin970-common',
]

blob_fixups: blob_fixups_user_type = {
    # Explicit BLA stock paths whose bytes need the inherited XML repairs.
    # See docs/BLA-225-EVIDENCE.md; these are not BKL sensor substitutions.
    (
        'odm/etc/camera/HwaPerfRecord/config.xml',
        'odm/etc/camera/LaserCali/LaserCali.xml',
        'odm/etc/camera/LaserCali/LaserCaliDefault.xml',
        'odm/etc/camera/LaserCali/LaserCaliDefault_Sharp.xml',
        'odm/etc/camera/LaserCali/LaserCali_Sharp.xml',
        'odm/etc/camera/LaserCali/LaserSelfCali.xml',
        'odm/etc/camera/LaserCali/LaserSelfCali_Sharp.xml',
        'odm/etc/camera/bgAdj/background_adj.xml',
        'odm/etc/camera/bshutter/imx386/algo.xml',
        'odm/etc/camera/bshutter/imx386/info.xml',
        'odm/etc/camera/bshutterRaw/arsr_cfg.xml',
        'odm/etc/camera/bshutterRaw/cc_cfg.xml',
        'odm/etc/camera/bshutterRaw/dpcc_cfg.xml',
        'odm/etc/camera/bshutterRaw/hsn_raw.xml',
        'odm/etc/camera/bshutterRaw/sharpen_cfg.xml',
        'odm/etc/camera/bshutterRaw/yuvnf_cfg.xml',
        'odm/etc/camera/colorDM/config.xml',
        'odm/etc/camera/davinci/imx219/dhdr_ivp.xml',
        'odm/etc/camera/davinci/imx219/hdr.xml',
        'odm/etc/camera/davinci/imx219/hwnie.xml',
        'odm/etc/camera/davinci/imx219/imgproc.xml',
        'odm/etc/camera/davinci/imx219/ivp_hdr2.xml',
        'odm/etc/camera/davinci/imx219/mddavinci/imgproc.xml',
        'odm/etc/camera/davinci/imx219/multiframe.xml',
        'odm/etc/camera/davinci/imx319/dhdr_ivp.xml',
        'odm/etc/camera/davinci/imx319/hdr.xml',
        'odm/etc/camera/davinci/imx319/hwnie.xml',
        'odm/etc/camera/davinci/imx319/imgproc.xml',
        'odm/etc/camera/davinci/imx319/ivp_hdr2.xml',
        'odm/etc/camera/davinci/imx319/mddavinci/imgproc.xml',
        'odm/etc/camera/davinci/imx319/multiframe.xml',
        'odm/etc/camera/davinci/imx386dual/colorfusion.xml',
        'odm/etc/camera/davinci/imx386dual/dcsr2.xml',
        'odm/etc/camera/davinci/imx386dual/dhdr_ivp.xml',
        'odm/etc/camera/davinci/imx386dual/hwnie.xml',
        'odm/etc/camera/davinci/imx386dual/imgproc.xml',
        'odm/etc/camera/davinci/imx386dual/ivp_hdr2.xml',
        'odm/etc/camera/davinci/imx386dual/mddavinci/imgproc.xml',
        'odm/etc/camera/davinci/imx386dual/multiframe.xml',
        'odm/etc/camera/davinci/imx386dual/nicefood/imgproc.xml',
        'odm/etc/camera/dcamera/config.xml',
        'odm/etc/camera/dcvalidation.xml',
        'odm/etc/camera/facedetection/config.xml',
        'odm/etc/camera/frontbokeh/fcve.xml',
        'odm/etc/camera/hdccalib/hw_calib_setting.xml',
        'odm/etc/camera/hdflash/imx386/hdflash.xml',
        'odm/etc/camera/hwbeauty/default/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/bm/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/lm/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/ntdny/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/oz/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/rh/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/zdfz/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx319/zg/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/bm/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/lm/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/ntdny/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/oz/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/rh/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/zdfz/hwbeauty_params.xml',
        'odm/etc/camera/hwbeauty/imx386dual/zg/hwbeauty_params.xml',
        'odm/etc/camera/hwldc/imx219/hwldc_config.xml',
        'odm/etc/camera/hwldc/imx319/hwldc_config.xml',
        'odm/etc/camera/hwscope/default/hwsz.xml',
        'odm/etc/camera/ippalgoconfig.xml',
        'odm/etc/camera/ispenhnc/ispenhncalgoconfig.xml',
        'odm/etc/camera/mempoolcfg.xml',
        'odm/etc/camera/mmi/afcvalidation.xml',
        'odm/etc/camera/mmi/config.xml',
        'odm/etc/camera/mmi/hw_ois_calib_setting.xml',
        'odm/etc/camera/mmi/hwhallcodeCalib.xml',
        'odm/etc/camera/mmi/pdoffsetcalib_back.xml',
        'odm/etc/camera/mmi7cm/MHA_imx286dual/mmi7cmConfig.xml',
        'odm/etc/camera/moderecomm/config.xml',
        'odm/etc/camera/monitor_config.xml',
        'odm/etc/camera/motiondetection/mdconfig.xml',
        'odm/etc/camera/multidenoise/imx219/ivp_mfnr2.xml',
        'odm/etc/camera/multidenoise/imx219/multiframe.xml',
        'odm/etc/camera/multidenoise/imx319/dcsr2.xml',
        'odm/etc/camera/multidenoise/imx319/hwnie_cb.xml',
        'odm/etc/camera/multidenoise/imx319/ivp_mfnr2.xml',
        'odm/etc/camera/multidenoise/imx319/multiframe.xml',
        'odm/etc/camera/multidenoise/imx319/seamless_hdr.xml',
        'odm/etc/camera/multidenoise/imx386dual/colorfusion.xml',
        'odm/etc/camera/multidenoise/imx386dual/hwnie_cb.xml',
        'odm/etc/camera/multidenoise/imx386dual/hwnie_mb.xml',
        'odm/etc/camera/multidenoise/imx386dual/ivp_mfnr2.xml',
        'odm/etc/camera/multidenoise/imx386dual/multiframe.xml',
        'odm/etc/camera/multidenoise/multidenoise.xml',
        'odm/etc/camera/multiexpofusion/default/multiframe.xml',
        'odm/etc/camera/multiexpofusion/imx386dual/multiframe.xml',
        'odm/etc/camera/offlinealgocfg.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_cb.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_cb_dlsr.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_co.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_co_dlsr.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_dlsr.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_mo.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_mo_dlsr.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_star.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_to.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwnie_to_dlsr.xml',
        'odm/etc/camera/opticalzoom/imx386dual/hwoz.xml',
        'odm/etc/camera/pdafvalidation.xml',
        'odm/etc/camera/portrait/VideoBokehShape.xml',
        'odm/etc/camera/portrait/portraitModeConfig.xml',
        'odm/etc/camera/powermonitor/config.xml',
        'odm/etc/camera/ppconfig.xml',
        'odm/etc/camera/relight/relight.xml',
        'odm/etc/camera/scenedetection/sdconfig.xml',
        'odm/etc/camera/scenerecognition/SceneRecognitionConfig.xml',
        'odm/etc/camera/smartae/imx219/SmartAE.xml',
        'odm/etc/camera/smartae/imx319/SmartAE.xml',
        'odm/etc/camera/smartae/imx386/SmartAE.xml',
        'odm/etc/camera/videostabilization/config.xml',
        'odm/etc/camera/videostabilization/param_vdh.xml',
        'odm/etc/camera/watermark/param.xml',
    ): blob_fixup()
        .binary_regex_replace(b'gb2312', b'iso-8859-1')
        .binary_regex_replace(b'GB2312', b'iso-8859-1')
        .binary_regex_replace(b'L-R-Ev', b'LREv')
        .binary_regex_replace(rb'<\?xml version="1\.0"\?>', b'<?xml version="1.0" encoding="iso-8859-1"?>')
        .binary_regex_replace(b'---->', b'-->'),
    'odm/etc/display/effect/algorithm/hdr_engine.xml': blob_fixup()
        .binary_regex_replace(b'gb2312', b'iso-8859-1')
        .binary_regex_replace(b'subverison', b'subversion')
        .binary_regex_replace(b'--->', b'-->')
        .binary_regex_replace(b't->', b't -->')
        .binary_regex_replace(b'r->', b'r -->'),
    (
        'odm/lib64/libarcsoft_beautyshot.so',
        'odm/lib64/libmrc_cg_beauty.so',
        'odm/lib64/libvidhance.so',
    ): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    (
        'odm/lib64/hwcam/hwcam.kirin970.BLANC.p.IMX319.so',
        'odm/lib64/hwcam/hwcam.kirin970.BLANC.p.IMX386HYBIRD.so',
        'odm/lib64/hwcam/hwcam.kirin970.BLANC.s.IMX319.so',
        'odm/lib64/hwcam/hwcam.kirin970.BLANC.s.IMX386HYBIRD.so',
        'odm/lib64/hwcam/hwcam.kirin970.m.BLANC.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v29.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'blanc',
    'huawei',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'kirin970-common', module.vendor
    )
    utils.run()
