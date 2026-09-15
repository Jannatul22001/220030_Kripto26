"""
PROGRAM HILL CIPHER (Python, modular)
--------------------------------------
Fitur:
  1. Enkripsi   -> input: plaintext + kunci (ukuran matriks n x n bebas)
  2. Dekripsi   -> input: ciphertext + kunci (ukuran matriks n x n bebas)
  3. Cari Kunci -> input: plaintext + ciphertext (ukuran kunci n x n ditentukan)
  4. Keluar

Kunci diinput sebagai n*n bilangan bulat (boleh negatif/berapa saja),
dipisahkan spasi atau baris baru; otomatis dinormalisasi mod 26.
"""

from itertools import combinations

MOD = 26


# ======================================================
#                  FUNGSI UTILITAS DASAR
# ======================================================

def mod_pos(a, m=MOD):
    """Memastikan hasil modulo selalu positif (0..25)."""
    return ((a % m) + m) % m


def mod_inverse(a, m=MOD):
    """Mencari invers modular dari sebuah bilangan (brute force, cukup cepat untuk mod 26)."""
    a = mod_pos(a, m)
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1  # tidak memiliki invers (a dan m tidak koprima)


def clean_text(s):
    """Menyisakan huruf saja, diubah ke huruf kapital."""
    return ''.join(ch.upper() for ch in s if ch.isalpha())


def text_to_numbers(s):
    return [ord(c) - ord('A') for c in s]


def numbers_to_text(nums):
    return ''.join(chr(ord('A') + mod_pos(x)) for x in nums)


def print_matrix(mat):
    for row in mat:
        print(' '.join(f'{x:4d}' for x in row))


# ======================================================
#                OPERASI MATRIKS (MOD 26)
# ======================================================

def determinant(mat, n):
    """Determinan matriks n x n (ekspansi kofaktor baris pertama), hasil mod 26."""
    if n == 1:
        return mod_pos(mat[0][0])
    if n == 2:
        return mod_pos(mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0])

    det = 0
    for col in range(n):
        minor = [row[:col] + row[col + 1:] for row in mat[1:]]
        sign = 1 if col % 2 == 0 else -1
        det = mod_pos(det + sign * mat[0][col] * determinant(minor, n - 1))
    return det


def cofactor_matrix(mat, n):
    """Matriks kofaktor (untuk membentuk adjoin)."""
    cof = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            minor = [row[:c] + row[c + 1:] for i, row in enumerate(mat) if i != r]
            sign = 1 if (r + c) % 2 == 0 else -1
            minor_det = 1 if n - 1 == 0 else determinant(minor, n - 1)
            cof[r][c] = mod_pos(sign * minor_det)
    return cof


def transpose(mat, n):
    return [[mat[j][i] for j in range(n)] for i in range(n)]


def inverse_matrix_mod(mat, n):
    """Invers matriks mod 26. Mengembalikan None jika determinan tidak koprima dengan 26."""
    det = determinant(mat, n)
    det_inv = mod_inverse(det)
    if det_inv == -1:
        return None
    adj = transpose(cofactor_matrix(mat, n), n)
    return [[mod_pos(adj[i][j] * det_inv) for j in range(n)] for i in range(n)]


def multiply_matrix(A, B, n, m, p):
    """Perkalian matriks A (n x m) dengan B (m x p), hasil mod 26."""
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            s = 0
            for k in range(m):
                s += A[i][k] * B[k][j]
            C[i][j] = mod_pos(s)
    return C


# ======================================================
#                  INPUT KUNCI DARI USER
# ======================================================

def input_ukuran_matriks():
    while True:
        teks = input("Masukkan ukuran matriks kunci n (kunci akan berukuran n x n, n >= 2): ")
        try:
            n = int(teks)
            if n >= 2:
                return n
        except ValueError:
            pass
        print("Ukuran tidak valid, coba lagi.")


def input_key_matrix(n):
    """
    Kunci diinput sebagai n*n bilangan bulat (bebas nilainya: negatif, > 25, dsb),
    dipisahkan spasi atau baris baru. Setiap nilai otomatis dinormalisasi mod 26.
    """
    print(f"Masukkan {n * n} bilangan bulat untuk kunci, dipisahkan spasi")
    print(f"(boleh satu baris, atau {n} bilangan per baris untuk tiap baris matriks).")
    print("Contoh 2x2: 6 24 1 13")

    nilai = []
    while len(nilai) < n * n:
        baris = input()
        for tok in baris.split():
            try:
                nilai.append(int(tok))
            except ValueError:
                print(f"'{tok}' bukan bilangan bulat, diabaikan.")
    nilai = nilai[:n * n]  # buang token kelebihan bila ada

    key = [[mod_pos(nilai[i * n + j]) for j in range(n)] for i in range(n)]
    print("Kunci dalam bentuk matriks (setelah dinormalisasi mod 26):")
    print_matrix(key)
    return key


# ======================================================
#              FUNGSI UTAMA: ENKRIPSI / DEKRIPSI
# ======================================================

def hill_encrypt(plaintext_raw, key, n):
    """Mengembalikan (ciphertext, plaintext_setelah_dibersihkan_dan_padding)."""
    plaintext = clean_text(plaintext_raw)
    while len(plaintext) % n != 0:
        plaintext += 'X'  # padding

    nums = text_to_numbers(plaintext)
    ciphertext = ''
    for i in range(0, len(nums), n):
        block = [[nums[i + j]] for j in range(n)]
        hasil = multiply_matrix(key, block, n, n, 1)
        ciphertext += ''.join(chr(ord('A') + hasil[j][0]) for j in range(n))
    return ciphertext, plaintext


def hill_decrypt(ciphertext_raw, key, n):
    """Mengembalikan (plaintext, kode_error). kode_error None jika berhasil,
    'panjang' jika panjang ciphertext bukan kelipatan n, 'invers' jika kunci tidak invertible."""
    ciphertext = clean_text(ciphertext_raw)
    if len(ciphertext) % n != 0:
        return None, "panjang"

    key_inv = inverse_matrix_mod(key, n)
    if key_inv is None:
        return None, "invers"

    nums = text_to_numbers(ciphertext)
    plaintext = ''
    for i in range(0, len(nums), n):
        block = [[nums[i + j]] for j in range(n)]
        hasil = multiply_matrix(key_inv, block, n, n, 1)
        plaintext += ''.join(chr(ord('A') + hasil[j][0]) for j in range(n))
    return plaintext, None


def hill_find_key(plaintext_raw, ciphertext_raw, n):
    """
    Mencari kunci K dari pasangan plaintext & ciphertext yang diketahui: K = C * P^-1 (mod 26).
    - Jika plaintext/ciphertext kurang panjang atau tidak sama panjang, otomatis di-padding
      dengan huruf dummy 'X' di akhir.
    - Mencoba SEMUA kombinasi n blok dari blok-blok yang tersedia sampai menemukan satu
      kombinasi yang matriks plaintext-nya invertible mod 26.
    Mengembalikan matriks kunci, atau None jika tidak ada kombinasi yang berhasil.
    """
    plain = clean_text(plaintext_raw)
    cipher = clean_text(ciphertext_raw)

    target_len = max(len(plain), len(cipher), n * n)
    if target_len % n != 0:
        target_len += n - (target_len % n)

    dipadding = len(plain) < target_len or len(cipher) < target_len
    plain = plain.ljust(target_len, 'X')
    cipher = cipher.ljust(target_len, 'X')

    if dipadding:
        print("Catatan: plaintext/ciphertext ditambah huruf dummy 'X' di akhir agar")
        print(f"panjangnya menjadi {target_len} huruf (kelipatan {n}).")
        print(f"Plaintext dipakai  : {plain}")
        print(f"Ciphertext dipakai : {cipher}")

    p_num = text_to_numbers(plain)
    c_num = text_to_numbers(cipher)
    total_blok = target_len // n

    blok_p = [p_num[i * n:(i + 1) * n] for i in range(total_blok)]
    blok_c = [c_num[i * n:(i + 1) * n] for i in range(total_blok)]

    # Coba semua kombinasi n blok dari total_blok yang tersedia
    for combo in combinations(range(total_blok), n):
        P = [[blok_p[b][row] for b in combo] for row in range(n)]
        C = [[blok_c[b][row] for b in combo] for row in range(n)]

        P_inv = inverse_matrix_mod(P, n)
        if P_inv is not None:
            K = multiply_matrix(C, P_inv, n, n, n)
            return K

    print(f"Sudah dicoba semua kombinasi blok yang mungkin (dari {total_blok} blok tersedia),")
    print(f"tapi tidak ada kombinasi {n} blok plaintext yang membentuk matriks invertible mod 26.")
    print("Ini bukan berarti kuncinya salah, hanya berarti huruf-huruf pada plaintext")
    print("yang diberikan belum cukup 'beragam' untuk metode ini. Coba pasangan plaintext-")
    print("ciphertext yang lebih panjang atau lebih variatif hurufnya.")
    return None


# ======================================================
#                  MENU-MENU (MODULAR)
# ======================================================

def menu_enkripsi():
    print("\n--- ENKRIPSI ---")
    n = input_ukuran_matriks()
    key = input_key_matrix(n)

    if inverse_matrix_mod(key, n) is None:
        print("Peringatan: determinan kunci tidak koprima dengan 26.")
        print("Ciphertext tetap bisa dihasilkan, tetapi TIDAK BISA didekripsi kembali dengan kunci ini.")

    plaintext_raw = input("Masukkan plaintext: ")
    ciphertext, plaintext_padded = hill_encrypt(plaintext_raw, key, n)

    print(f"\nPlaintext (dibersihkan & padding jika perlu): {plaintext_padded}")
    print(f"Ciphertext hasil enkripsi   : {ciphertext}")


def menu_dekripsi():
    print("\n--- DEKRIPSI ---")
    n = input_ukuran_matriks()
    key = input_key_matrix(n)

    ciphertext_raw = input("Masukkan ciphertext: ")
    plaintext, error = hill_decrypt(ciphertext_raw, key, n)

    if error == "panjang":
        print(f"Panjang ciphertext (setelah dibersihkan) harus kelipatan {n}.")
        return
    if error == "invers":
        print("Kunci tidak memiliki invers mod 26 (determinan tidak koprima dengan 26).")
        print("Dekripsi tidak dapat dilakukan dengan kunci ini.")
        return

    print(f"\nCiphertext (dibersihkan): {clean_text(ciphertext_raw)}")
    print(f"Plaintext hasil dekripsi : {plaintext}")


def menu_cari_kunci():
    print("\n--- CARI KUNCI ---")
    n = input_ukuran_matriks()

    plaintext_raw = input("Masukkan plaintext yang diketahui  : ")
    ciphertext_raw = input("Masukkan ciphertext yang diketahui : ")

    key = hill_find_key(plaintext_raw, ciphertext_raw, n)
    if key is not None:
        print(f"\nKunci ditemukan (matriks {n}x{n}):")
        print_matrix(key)
        key_str = ''.join(chr(ord('A') + key[i][j]) for i in range(n) for j in range(n))
        print(f"Kunci dalam bentuk string: {key_str}")


# ======================================================
#                        MAIN
# ======================================================

def main():
    while True:
        print("\n===================================")
        print("        PROGRAM HILL CIPHER")
        print("===================================")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Cari Kunci")
        print("4. Keluar")

        pilihan_teks = input("Pilih menu (1-4): ")
        try:
            pilihan = int(pilihan_teks)
        except ValueError:
            print("Input tidak valid.")
            continue

        if pilihan == 1:
            menu_enkripsi()
        elif pilihan == 2:
            menu_dekripsi()
        elif pilihan == 3:
            menu_cari_kunci()
        elif pilihan == 4:
            print("\nProgram selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid, silakan pilih 1-4.")


if __name__ == "__main__":
    main()