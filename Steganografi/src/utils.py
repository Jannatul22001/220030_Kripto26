"""Fungsi bantu: konversi byte <-> bit dan pembuatan/pembacaan header."""

import struct
import numpy as np

MAGIC = b"STEG"          # penanda bahwa gambar berisi pesan kita
TIPE_TEKS = 0
TIPE_GAMBAR = 1
HEADER_BYTES = 9         # 4 (magic) + 1 (tipe) + 4 (ukuran data)
HEADER_BITS = HEADER_BYTES * 8


def bytes_ke_bits(data: bytes) -> np.ndarray:
    """Ubah bytes menjadi array bit (0/1), MSB lebih dulu."""
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))


def bits_ke_bytes(bits: np.ndarray) -> bytes:
    """Ubah array bit (0/1) kembali menjadi bytes."""
    return np.packbits(bits).tobytes()


def buat_header(tipe: int, ukuran: int) -> bytes:
    """Header = MAGIC (4 byte) + TIPE (1 byte) + UKURAN (4 byte, big-endian)."""
    return MAGIC + struct.pack(">BI", tipe, ukuran)


def baca_header(header: bytes):
    """Kembalikan (tipe, ukuran), atau None jika MAGIC tidak cocok."""
    if header[:4] != MAGIC:
        return None
    tipe, ukuran = struct.unpack(">BI", header[4:])
    return tipe, ukuran
