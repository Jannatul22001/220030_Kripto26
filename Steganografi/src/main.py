"""Menu CLI steganografi LSB + seed."""

from pathlib import Path

from stego import StegoError, decode, encode
from utils import TIPE_GAMBAR, TIPE_TEKS

ROOT = Path(__file__).resolve().parent.parent
COVER = ROOT / "input" / "covergambar.png"
SECRET_DIR = ROOT / "input" / "secret"
STEGO = ROOT / "output" / "stego.png"
EXTRACTED_DIR = ROOT / "output" / "extracted"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def tampil(path: Path) -> str:
    """Path relatif terhadap folder proyek, supaya rapi di layar."""
    return path.relative_to(ROOT).as_posix()


def minta_seed() -> int:
    while True:
        teks = input("Masukkan seed (bilangan bulat positif): ").strip()
        if teks.isdigit():
            return int(teks)
        print("[!] Seed harus berupa angka bulat positif, contoh: 1234")


def menu_encode():
    print("\nJenis pesan:")
    print("1) Ketik teks langsung")
    print("2) Teks dari file .txt")
    print("3) Gambar PNG")
    pilihan = input("Pilih: ").strip()

    if pilihan == "1":
        teks = input("Masukkan teks: ")
        if not teks:
            print("[!] Teks tidak boleh kosong.")
            return
        data, tipe = teks.encode("utf-8"), TIPE_TEKS
    elif pilihan == "2":
        nama = input("Nama file .txt di input/secret/ [pesan.txt]: ").strip() or "pesan.txt"
        path = SECRET_DIR / nama
        if not path.is_file():
            print(f"[!] File tidak ditemukan: {tampil(path)}")
            return
        try:
            teks = path.read_text(encoding="utf-8-sig").rstrip("\r\n")
        except UnicodeDecodeError:
            print("[!] File harus berupa teks UTF-8.")
            return
        if not teks:
            print("[!] Isi file kosong.")
            return
        print(f"[OK] Teks dibaca dari {tampil(path)} ({len(teks)} karakter)")
        data, tipe = teks.encode("utf-8"), TIPE_TEKS
    elif pilihan == "3":
        nama = input("Nama file PNG di input/secret/ [rahasia.png]: ").strip() or "rahasia.png"
        path = SECRET_DIR / nama
        if not path.is_file():
            print(f"[!] File tidak ditemukan: {tampil(path)}")
            return
        data, tipe = path.read_bytes(), TIPE_GAMBAR
        if not data.startswith(PNG_SIGNATURE):
            print("[!] File bukan PNG yang valid.")
            return
    else:
        print("[!] Pilihan tidak valid.")
        return

    seed = minta_seed()
    STEGO.parent.mkdir(parents=True, exist_ok=True)
    kapasitas, _ = encode(COVER, data, tipe, seed, STEGO)

    print(f"\n[OK] Kapasitas cover : {kapasitas:,} byte")
    print(f"[OK] Ukuran pesan    : {len(data):,} byte (+9 byte header)")
    print(f"[OK] Tersimpan di    : {tampil(STEGO)}")


def menu_decode():
    if not STEGO.is_file():
        print(f"[!] File stego tidak ditemukan: {tampil(STEGO)}. Lakukan encode dulu.")
        return

    seed = minta_seed()
    tipe, data = decode(STEGO, seed)
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    if tipe == TIPE_TEKS:
        hasil = EXTRACTED_DIR / "teks_hasil.txt"
        hasil.write_bytes(data)
        print("\n[OK] Tipe pesan   : Teks")
        print(f"[OK] Isi pesan    : {data.decode('utf-8', errors='replace')}")
    elif tipe == TIPE_GAMBAR:
        hasil = EXTRACTED_DIR / "gambar_hasil.png"
        hasil.write_bytes(data)
        print("\n[OK] Tipe pesan   : Gambar PNG")
    else:
        raise StegoError("Seed salah atau gambar tidak berisi pesan.")
    print(f"[OK] Tersimpan di : {tampil(hasil)}")


def main():
    while True:
        print("\n=== STEGANOGRAFI LSB + SEED ===")
        print("1. Encode (sembunyikan pesan)")
        print("2. Decode (ambil pesan)")
        print("3. Keluar")
        pilihan = input("Pilih: ").strip()
        try:
            if pilihan == "1":
                menu_encode()
            elif pilihan == "2":
                menu_decode()
            elif pilihan == "3":
                print("Sampai jumpa!")
                break
            else:
                print("[!] Pilihan tidak valid.")
        except StegoError as e:
            print(f"[X] {e}")


if __name__ == "__main__":
    main()