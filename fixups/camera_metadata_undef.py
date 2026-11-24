# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
"""Undefine stale Android 10 camera_metadata_section_* exports in hwcam.kirin970.m.BLANC.so."""

import hashlib
import struct
from pathlib import Path

EXPECTED_SHA256 = "8bff2924bcac0eca6334218603e4a9918d88e97508ef9d321524ed8468a7344d"
EXPECTED_OUTPUT_SHA256 = "c303f535caf1ce9961f119a0645ef73e5a9aa1f244c9b63348fb4b9a488a86ae"
TARGET_SYMBOLS = (
    b"camera_metadata_section_bounds",
    b"camera_metadata_section_names",
)
EXPECTED_TABLE_SIZE = 256


def patch_camera_metadata_undef(data: bytes) -> bytes:
    """Rewrite stale 256-byte section tables in .dynsym to SHN_UNDEF."""
    digest = hashlib.sha256(data).hexdigest()
    if digest == EXPECTED_OUTPUT_SHA256:
        return data
    if digest != EXPECTED_SHA256:
        raise ValueError(
            "BLA hwcam.kirin970.m.BLANC.so input SHA-256 mismatch; review the binary before patching"
        )
    if len(data) < 64 or data[:6] != b"\x7fELF\x02\x01" or data[18:20] != b"\xb7\x00":
        raise ValueError("hwcam.kirin970.m.BLANC.so must be little-endian AArch64 ELF64")

    buf = bytearray(data)
    (e_shoff,) = struct.unpack_from("<Q", buf, 40)
    e_shentsize, e_shnum = struct.unpack_from("<HH", buf, 58)
    if e_shoff == 0 or e_shoff + e_shentsize * e_shnum > len(buf):
        raise ValueError("Invalid ELF64 section header table")

    dynsym_sec = None
    for idx in range(e_shnum):
        sh = e_shoff + idx * e_shentsize
        (sh_type,) = struct.unpack_from("<I", buf, sh + 4)
        if sh_type == 11:  # SHT_DYNSYM
            dynsym_sec = sh
            break
    if dynsym_sec is None:
        raise ValueError("Missing SHT_DYNSYM in hwcam.kirin970.m.BLANC.so")

    dynsym_off, dynsym_sz = struct.unpack_from("<QQ", buf, dynsym_sec + 24)
    sh_link, = struct.unpack_from("<I", buf, dynsym_sec + 40)
    sh_entsize, = struct.unpack_from("<Q", buf, dynsym_sec + 56)
    if sh_entsize < 24 or sh_link >= e_shnum:
        raise ValueError("Invalid SHT_DYNSYM metadata")

    str_sh = e_shoff + sh_link * e_shentsize
    dynstr_off, dynstr_sz = struct.unpack_from("<QQ", buf, str_sh + 24)
    if dynstr_off + dynstr_sz > len(buf) or dynsym_off + dynsym_sz > len(buf):
        raise ValueError("Out-of-bounds .dynsym/.dynstr in hwcam.kirin970.m.BLANC.so")

    seen = set()
    targets = set(TARGET_SYMBOLS)
    count = dynsym_sz // sh_entsize
    for sym_idx in range(count):
        ent = dynsym_off + sym_idx * sh_entsize
        st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from(
            "<IBBHQQ", buf, ent
        )
        if st_name >= dynstr_sz:
            continue
        nul = buf.find(b"\x00", dynstr_off + st_name, dynstr_off + dynstr_sz)
        if nul < 0:
            continue
        name = bytes(buf[dynstr_off + st_name : nul])
        if name in targets:
            if st_shndx == 0 or st_size != EXPECTED_TABLE_SIZE:
                raise ValueError(
                    f"Unexpected dynsym state for {name!r}: shndx={st_shndx}, size={st_size}"
                )
            struct.pack_into("<IBBHQQ", buf, ent, st_name, st_info, st_other, 0, 0, 0)
            seen.add(name)

    if seen != targets:
        raise ValueError(f"Missing target dynsym entries: {sorted(targets - seen)}")
    return bytes(buf)


def blob_fixup(ctx, file, file_path, *args, **kwargs):
    destination = Path(file_path)
    original = destination.read_bytes()
    patched = patch_camera_metadata_undef(original)
    destination.write_bytes(patched)
    print(
        "BLA hwcam.kirin970.m.BLANC.so camera_metadata SHN_UNDEF fixup SHA-256: "
        + EXPECTED_SHA256
        + " -> "
        + hashlib.sha256(patched).hexdigest()
    )
