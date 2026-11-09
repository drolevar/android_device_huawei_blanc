# Huawei Mate 10 Pro (`blanc`) — LineageOS 24 source preparation

**Status: source preparation, not a build- or boot-validated ROM.** The target
handset is BLA-L29 on EMUI 12 `.225`, with an unlocked bootloader and working
TWRP reported by its owner on 2026-11-09. No current partition capture, stock
image set, or proprietary binary extraction is included in this repository.

## Source ancestry and checkout

`blanc-lineage-24.0` starts from the existing Blanc adaptation
[`8653804c7244686825faad09f7f1561c1663a513`](https://github.com/drolevar/android_device_huawei_blanc/commit/8653804c7244686825faad09f7f1561c1663a513).
That adaptation preserves the Berkeley device tree history, including the
[LineageOS Gerrit 495229](https://review.lineageos.org/c/LineageOS/android_device_huawei_berkeley/+/495229)
donor work. Existing authorship and licenses are retained. BLA-L09 remains a
declared SKU inherited from that adaptation, not a tested handset.

Use the pinned source plan and setup tool in
[`drolevar/lineage_manifest`, branch `blanc-lineage-24.0`](https://github.com/drolevar/lineage_manifest/tree/blanc-lineage-24.0/huawei).
It selects this repository together with the Kirin 970 common, Huawei hardware,
and kernel forks. `lineage.dependencies` records component relationships;
Lineage roomservice's default organization cannot select these personal forks.
Do not rely on roomservice to discover or replace the pinned manifest projects.

This preparation removes the inherited EMUI 10 `.202` build fingerprint and
description. A new `.225` identity must come from an actual stock capture, not
from editing the version number in an older fingerprint. Vendor product and
BoardConfig imports are required so that missing BLA proprietary files fail
configuration explicitly.

## Donor assumptions that still need replacing

| Area | Existing source | Evidence needed before an image build |
| --- | --- | --- |
| Partition layout | `BOARD_SUPER_PARTITION_SIZE = 4848615424` comes from Berkeley; common fstab expects logical partitions | BLA `.225` by-name map, capacities, stock fstab, and logical-partition metadata if present |
| Boot packaging | Common/hardware trees describe split kernel, normal ramdisk, recovery ramdisk, and recovery vendor images | Header inspection of the exact stock and working recovery images, including AVB/footer limits |
| Camera and ODM init | `init/init.hisi.odm.rc` still contains `CameraDaemon ... BKL` and BKL SKU conditions | BLA service arguments, SKU properties, libraries, calibration/configuration paths |
| Device blobs | `proprietary-files.txt` is a BKL-AL00 `.263` donor list, with BKL/BKLY/BERK entries | Complete, hash-recorded BLA-L29 `.225` extraction and ELF dependency audit |
| Shared vendor blobs | Common tree contains its own donor extraction recipe and fixups | Verify each common blob against the same BLA firmware; a common SoC does not prove binary equivalence |
| Metadata and encryption | Common fstab maps `patch` to `/metadata` and marks it formattable | Confirm partition ownership and encryption/keymaster requirements before enabling that layout |
| VINTF and policy | Common tree uses target FCM level 5 and legacy HALs | Check against the selected Lineage 24 matrices, vendor interfaces, and SELinux policy |

The donor sizes, mount rules, and init services remain visible for review;
they are **not instructions to repartition, format, or flash the handset**.
Do not replace BKL strings wholesale with BLA: filenames, camera modules,
calibration, and regional modem configuration can differ structurally.

## Next device-specific work

1. Obtain a read-only inventory from stock `.225` and the working recovery.
   Record the complete firmware identifiers, kernel release/configuration,
   partition names and sizes, boot-image headers, VINTF manifests, fstab,
   encryption properties, and file hashes. Keep raw captures outside public Git.
2. Replace the donor blob list and ODM init using that inventory. Retain source
   attribution for any donor fixup, but apply a binary patch only to a verified
   input hash and after checking its dependencies.
3. Generate `vendor/huawei/blanc` and `vendor/huawei/kirin970-common` privately
   with the extract-utils version recorded in the resolved source lock.
   Missing files, wrong architecture,
   unresolved ELF dependencies, and unreviewed donor entries are build blockers.
4. Review all partition and boot-image constants together with fstab and OTA
   releasetools. A successful compilation alone cannot validate this mapping.
5. Resolve the source compatibility work listed in the manifest preparation
   notes, then configure with `source build/envsetup.sh` and
   `breakfast blanc userdebug` in the complete source checkout.

No full Lineage 24 source sync, Android compilation, device boot, hardware test,
or official LineageOS charter qualification is asserted by this branch.

SPDX-FileCopyrightText: The LineageOS Project

SPDX-License-Identifier: Apache-2.0
