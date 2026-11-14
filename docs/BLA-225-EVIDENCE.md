# BLA-L29 `.225` source evidence

These are offline observations from the owner's stock capture, reviewed on
2026-11-14. Firmware files stay outside source control. Paths below are relative
to the engineering workspace, not inputs shipped by this device repository.
The owner identifies the running release as EMUI 12 `.225`; its complete
displayed identity remains under investigation.

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

No compilation, boot or hardware success is established by these changes.

SPDX-FileCopyrightText: The LineageOS Project

SPDX-License-Identifier: Apache-2.0
