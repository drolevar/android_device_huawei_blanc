# Huawei Mate 10 Pro (`blanc`) — LineageOS 24 source preparation

**Status: source preparation, not a build- or boot-validated ROM.** The target
handset is BLA-L29 on EMUI 12 `.225`, with an unlocked bootloader and working
TWRP reported by its owner on 2026-11-09. A private stock capture now supplies
the [measured geometry, init and extraction evidence](docs/BLA-225-EVIDENCE.md).
Stock images and proprietary binary bytes are not included in this repository.

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
| Partition layout | Super capacity reconciled to 5771362304 bytes from BLA stock LP metadata; common fstab still needs review | Complete partition/OTA layout review; see [capture evidence](docs/BLA-225-EVIDENCE.md) |
| Boot packaging | Common/hardware trees describe split kernel, normal ramdisk, recovery ramdisk, and recovery vendor images | Header inspection of the exact stock and working recovery images, including AVB/footer limits |
| Camera and ODM init | Stock `BLANC` camera argument and BLA L29/L09 modem counts applied; donor permissions retained | Platform groups, libraries, calibration/configuration paths and runtime validation |
| Device blobs | `proprietary-files.txt` selects 1119 stock BLA ODM inputs with raw and applicable fixed-output hashes; offline extraction and makefile generation checked | Complete ELF dependency, platform compatibility and runtime audit; see selection exclusions in the evidence document |
| Shared vendor blobs | Common tree contains its own donor extraction recipe and fixups | Verify each common blob against the same BLA firmware; a common SoC does not prove binary equivalence |
| Metadata and encryption | Common fstab maps `patch` to `/metadata` and marks it formattable | Confirm partition ownership and encryption/keymaster requirements before enabling that layout |
| VINTF and policy | Stock vendor reports target level 3; donor common source used level 5 and legacy HALs | Reconcile against the selected Lineage 24 matrices, vendor interfaces, and SELinux policy; stock manifests are excluded from this blob list |

The donor sizes, mount rules, and init services remain visible for review;
they are **not instructions to repartition, format, or flash the handset**.
Do not replace BKL strings wholesale with BLA: filenames, camera modules,
calibration, and regional modem configuration can differ structurally.

## Next device-specific work

1. Complete the private stock `.225` evidence review, including the complete
   displayed firmware identity, boot-image headers, fstab and encryption. Keep
   raw captures outside public Git.
2. Audit remaining donor init permissions, omitted stock init actions, platform
   groups and native dependencies. The BLA list and inherited fixups are a
   source candidate, not proof that every stock component should ship or works.
3. Generate and integrate `vendor/huawei/blanc` and `vendor/huawei/kirin970-common` privately
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

## Host regression checks

From this device repository, with the selected extract-utils checkout supplied
explicitly for an isolated worktree:

```sh
PYTHONPATH=/absolute/android/root/tools/extract-utils python3 -B -m unittest discover -s tests -v
```

These tests use synthetic XML and host-built ELF fixtures. They require `cc`,
`readelf` and extract-utils' selected `patchelf` prebuilt; they do not access a
handset or read proprietary firmware. They check XML repairs, generated media/NFC
copy rules, media source priority, GPS module naming, default extraction policy
and the retained native dependency replacements.

SPDX-FileCopyrightText: The LineageOS Project

SPDX-License-Identifier: Apache-2.0
