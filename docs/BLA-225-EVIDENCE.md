# BLA-L29 `.225` source evidence

These are offline observations from the owner's stock capture, reviewed on
2026-11-14. Firmware files stay outside source control. Paths below are relative
to the engineering workspace, not inputs shipped by this device repository.
The separately approved stock-Android reboot verifies
`BLA-L29 12.0.0.225(C432E4R1P1)` in `ro.huawei.build.display.id`.

## Product launch API

Normal Android reports `ro.product.first_api_level=26`, SDK 29 and VNDK 29.
The blanc product overrides the common donor's `PRODUCT_SHIPPING_API_LEVEL=29`
with the measured **26**. The common `BOARD_SHIPPING_API_LEVEL` declaration is
left separate; no measured stock board-first-API property is available.
Current Android SDK, vendor VNDK selection, patch declarations and kernel
interfaces are unchanged by this product identity correction.

Private capture: `private/baselines/20261114-stock-android-final/properties.txt`,
SHA-256 `54d3713bbf8ac5dcf6fa3e484ab31a9f0811ffe6296c2c4a4a42bca66ba1bc5b`.
Use the real configured product values to validate inheritance after sync.

## Super capacity and ODM init

`firmware/current/logical-images/metadata.json` reports both
`block_devices[super].size` and `super_device.total_size` as **5771362304** bytes.
`super_device.used_size` is 5769265152 bytes and is not the partition capacity.
Only `BOARD_SUPER_PARTITION_SIZE` is reconciled here; this does not validate
dynamic group sizing, fstab, encryption, metadata or OTA layout.

The entire super copy through TWRP has the owner-recorded SHA-256
`40700e7f8162cb3736817775c0eb6694ced405e2d25655165e513b535d521535`.
The JSON metadata SHA-256 is
`be6d559af278d5e9a29514a5771c8245d299ea453695add84504de357d4fb690`.

Under `firmware/current/original-filesystems/odm/etc/init/`:

| File | Observation | SHA-256 |
| --- | --- | --- |
| `init.hisi.odm.rc` | `CameraDaemon /vendor/bin/CameraDaemon kirin970 BLANC` | `62a7eb491357491a5da3f379343a9f692377e890c6ebfbf1a9b24fa7fd575652` |
| `init.odm.L29.rc` | SKU `BLA-L29` sets `ro.odm.config.modem_number` to `2` | `0917306190fa4e8e285944bb58c7ae346b8b12fc983c5e9451cbeb80b45e4b45` |
| `init.odm.L09.rc` | SKU `BLA-L09` sets `ro.odm.config.modem_number` to `1` | `18c1ff842b4fedd9bbc8b6503580ddca0f277e7a75ca102fd297948529c7eb83` |

The source init adopts those arguments and SKU actions, removes the BKL-L04
symlink action, and retains the donor permission setup pending a separate audit.
Stock CameraDaemon also requests group `dsm`; this change does not add that
unverified platform group. This is a deliberate difference from stock, not a
claim of equivalent access or working camera/modem behavior. L09 is represented
in the captured files; no L09 handset was tested.

`hw_product/etc/prop/local.prop` in the same original-filesystems view contains
`ro.comp.hl.product_base_version.real=BLA-LGRP2-OVS 102.0.0.225`.
`version/etc/meta.prop` contains
`ro.comp.hl.product_cust_version.real=BLA-L29-CUST 102.0.0.4(C432)`.
Neither string is substituted into a fabricated build fingerprint.

## ODM extraction candidate

The original BKL device recipe at `f205195` lists 994 files; only 148 exist in
this BLA original-filesystems view (846 absent). The replacement selects **1119
regular stock ODM files** by their actual paths, not by renaming donor entries.
Each entry in `proprietary-files.txt` pins the raw SHA-1 expected by extract-utils;
126 entries additionally pin the observed fixed-output SHA-1. Original donor
ancestry and copyright remain in Git history and the extraction script.

Selection includes audio (93), camera data (243), declared L09/L29 carrier data
(714), display (12), firmware (15), GPS configs (4), media/NFC (5), regular
native files/GPS daemon (21), `phone.prop` (1), SWS (6), TA (4) and thermal (1).
This captures available alternatives, including BA09 audio and multiple display,
sensor, touchscreen and TA variants; presence is not evidence of installed
hardware or a reason to advertise another SKU. L29 and L09 are the only declared
SKUs. The five camera HAL filenames are the actual `BLANC` IMX319/IMX386HYBIRD
and `m.BLANC` files in stock `odm/lib64/hwcam/`.

The selection deliberately excludes:

- `odm/etc/init/*` and `odm/etc/vintf/*`: source owns init and SKU manifests.
  Stock init also contains identity actions and an IR HAL service override;
  those were not imported wholesale.
- Stock `etc/permissions`, build/local properties and SELinux contexts: product
  source owns features, identity and policy; do not copy stock platform policy
  into the new platform. `phone.prop` is retained because Huawei libinit parses
  this device radio/connectivity database.
- `cust/`, `special_cust/`, A09/AL00/TL00 carrier directories, README files and
  absolute compatibility symlinks. These are unreviewed regional overlays,
  undeclared SKUs, documentation or links requiring separate integration.
- `libMegviiUnlock.so` and `libmegface.so`: the selected extract-utils default
  prohibited-file check rejects their actual stock signatures. A first scratch
  extraction stopped there. The candidate omits them rather than requiring an
  extraction override; face unlock and any remaining dependencies are unresolved.

Media/NFC retain the donor destination remaps used by the product. Media keeps
`TRYSRCFIRST`, selecting the measured ODM file even when vendor also contains a
same-name file. NXP vendor-extension source
`hardware/nxp/nfc/vendor_extns/libnfc_vendor_extn/src/common/utils/phNxpConfig.cc`
has the default RF path `/system/vendor/libnfc-nxp_RF.conf`; the inherited
vendor-root destination is retained pending NFC runtime review. Other NFC
configs go to `vendor/etc/`.

Stock ODM `gps.default.so` and `gps47531.default.so` collide with the common
vendor modules by basename. Both use `MODULE_SUFFIX=_blanc`, preserving their
ODM install paths and stems. Both stock SONAMEs are
`gps.huaweik3v3android.so`; `FIX_SONAME` changes each to its installed filename.
No ELF-check or dependency-generation bypass is added.

## Fixup audit

The explicit camera fixup tuple contains 120 actual BLA paths: 118 declared
GB2312/gb2312 and two XML declarations lacking encoding. The inherited byte-level
repairs allow host XML parsing without transcoding stock bytes. They also fix
the six `L-R-Ev` occurrences and the malformed comment ending in
`motiondetection/mdconfig.xml`. ISO-8859-1 declaration replacement is inherited
parser compatibility behavior, not proof of correct Chinese text interpretation
or equivalent runtime camera behavior. The obsolete `--L-R-Ev` replacement was
removed because this BLA capture contains no such occurrence.

The existing HDR XML fixes remain: encoding declaration, mismatched
`subverison` closing tag, and malformed comment endings. All **243 selected XML
files** parse after extraction, including the 182 selected camera XML files.
The remaining 61 camera files are other data formats.

Only three BLA ODM libraries need the inherited
`libstdc++.so` to `libstdc++_vendor.so` DT_NEEDED replacement, confirmed with
`readelf -d` on the untouched inputs:

| Original `odm/lib64/` file | SHA-256 |
| --- | --- |
| `libarcsoft_beautyshot.so` | `0179de082b10429fb2a06db6420446c01df16cd9db34ffe0295ad0a8413a72d2` |
| `libmrc_cg_beauty.so` | `53fb2b645f1081ce7b4c5993b973e91b4509f2e7d5c4053be291e07cd218da49` |
| `libvidhance.so` | `a3b2c24f3166d02c0467f06359eb4c67b284ab3044a13137c723a54f731bc5d5` |

The three absent donor library paths are removed from the fixup tuple. Native
instruction patches in the common project are outside this device change.

## Offline verification record

Extract-utils commit: `78ba5d58c4b06712e18bb387a2a72eac8fbc8d70`, with its
selected `patchelf-0_18` (binary SHA-256
`b699cb82300dfd08ea6c895d8829b46bea970cfa737fa34188d8256ca89404e5`).
A redirected module context wrote only under ignored
`cache/blanc-225-device-audit/`, never the syncing Android checkout. The actual
DiskSource copy, hash checking, fixups and vendor makefile/Blueprint generation
completed for all 1119 entries. Every raw/fixed hash matched; all 243 XMLs parsed.
126 files changed: 120 camera XMLs, one HDR XML, three dependency replacements
and two GPS SONAME repairs. Nine source/host fixture tests pass; the BLA camera
and GPS regressions were observed failing before their configuration changes.
The workspace automation suite also passed all 64 tests.

There were no module-name or install-destination collisions against the main
task's common worktree candidate whose list SHA-256 was
`3afa1371947fdd7e935a4b598b5150b25d49b70be8cf947a7d6104ccf683febe`.
This is an observation of that candidate, not a new common source selection.
The local audit contains per-file SHA-256 manifests; their hashes are:

- `selected-originals.sha256`:
  `0690e635532aa5873721c7a4939137eb59c0f21a8c69419b1477504f616d1a4f`
- `selected-outputs.sha256`:
  `8770871add949cff38340550d3bbba23515272ac95053b516759c348fd0539ec`
- Generated device `Android.bp`:
  `d51dc603ebc7ed364ddf5c25da0bc4c59952258d2d7eef356ad991fa6df146ea`

Stock `vendor/etc/vintf/manifest.xml` declares target level **3**. Copying stock
manifests was intentionally avoided; target-platform VINTF reconciliation remains
separate. Complete ELF dependency resolution (including availability of the
renamed C++ compatibility library), SELinux, kernel compatibility, permissions
and omitted stock init actions remain unvalidated. Generating Blueprint with
ELF checks enabled does not execute Soong's ELF checks or prove compilation.
No compilation, boot or hardware success is established by these changes.

SPDX-FileCopyrightText: The LineageOS Project

SPDX-License-Identifier: Apache-2.0
