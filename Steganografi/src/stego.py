"""Inti steganografi: LSB 1 bit per channel dengan posisi diacak oleh seed."""

import numpy as np
from PIL import Image

from utils import (
    HEADER_BITS,
    bits_ke_bytes,
    buat_header,
    baca_header,
    bytes_ke_bits,
)


class StegoError(Exception):
    """Error yang pesannya aman ditampilkan langsung ke pengguna."""


def _muat_gambar(path):
    """Buka gambar dan paksa ke mode RGB (3 channel, 8 bit)."""
    try:
        return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)
    except FileNotFoundError:
        raise StegoError(f"File gambar tidak ditemukan: {path}")


def _urutan_posisi(jumlah: int, seed: int) -> np.ndarray:
    """Permutasi acak 0..jumlah-1. Seed yang sama -> urutan yang sama."""
    return np.random.default_rng(seed).permutation(jumlah)


def encode(path_cover, data: bytes, tipe: int, seed: int, path_output):
    """Sisipkan data ke cover, simpan sebagai PNG. Return (kapasitas, terpakai) dalam byte."""
    piksel = _muat_gambar(path_cover)
    bentuk = piksel.shape
    datar = piksel.flatten()                      # 1 nilai = 1 channel warna

    paket = buat_header(tipe, len(data)) + data   # header + pesan
    bits = bytes_ke_bits(paket)

    if len(bits) > datar.size:
        raise StegoError(
            f"Kapasitas tidak cukup: butuh {len(paket)} byte, "
            f"cover hanya muat {datar.size // 8} byte."
        )

    posisi = _urutan_posisi(datar.size, seed)[: len(bits)]
    datar[posisi] = (datar[posisi] & 0xFE) | bits  # ganti LSB dengan bit pesan

    Image.fromarray(datar.reshape(bentuk), "RGB").save(path_output, format="PNG")
    return datar.size // 8, len(paket)


def decode(path_stego, seed: int):
    """Ambil pesan dari stego-image. Return (tipe, data)."""
    datar = _muat_gambar(path_stego).flatten()
    posisi = _urutan_posisi(datar.size, seed)

    # 1) Baca header (72 bit pertama sesuai urutan acak)
    bits_header = datar[posisi[:HEADER_BITS]] & 1
    hasil = baca_header(bits_ke_bytes(bits_header))
    if hasil is None:
        raise StegoError("Seed salah atau gambar tidak berisi pesan.")
    tipe, ukuran = hasil

    # 2) Baca data sebanyak 'ukuran' byte
    total_bit = HEADER_BITS + ukuran * 8
    if total_bit > datar.size:
        raise StegoError("Seed salah atau gambar tidak berisi pesan.")
    bits_data = datar[posisi[HEADER_BITS:total_bit]] & 1
    return tipe, bits_ke_bytes(bits_data)
