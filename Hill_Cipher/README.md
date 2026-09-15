# Program Hill Cipher (Python)

Program ini dibuat untuk tugas praktikum Kriptografi, membahas cipher klasik **Hill Cipher**. Programnya bisa dipakai untuk 3 hal: enkripsi, dekripsi, dan mencari kunci kalau plaintext & ciphertext-nya sudah diketahui.

## Alur Program

Waktu program dijalankan, yang pertama muncul adalah menu utama:

```
1. Enkripsi
2. Dekripsi
3. Cari Kunci
4. Keluar
```

Jadi user tinggal pilih mau ngapain dulu (1-4). Setelah satu proses selesai, menu ini akan muncul lagi terus sampai user pilih 4 (Keluar).

### 1. Kalau pilih Enkripsi

1. Diminta masukin ukuran matriks kunci dulu, misal `2` untuk matriks 2x2.
2. Terus diminta masukin kunci matriksnya, dalam bentuk angka yang dipisah spasi (boleh ditulis satu baris sekaligus, atau per baris matriks, terserah). Contoh untuk matriks 2x2: `3 3 2 5`.
3. Program bakal cek dulu apakah kuncinya bisa di-invers mod 26 atau tidak (kalau tidak, tetap dilanjut tapi diberi peringatan karena nanti ciphertext-nya tidak akan bisa didekripsi lagi).
4. Terakhir diminta masukin plaintext-nya (teks yang mau dienkripsi). Teks otomatis dibersihkan (spasi/simbol dibuang, semua jadi huruf besar) dan kalau panjangnya belum kelipatan ukuran matriks, otomatis ditambah huruf `X` di belakang.
5. Hasil ciphertext-nya ditampilkan.

### 2. Kalau pilih Dekripsi

Alurnya kebalikan dari enkripsi:

1. Masukin ukuran matriks kunci.
2. Masukin kunci (format sama, angka dipisah spasi).
3. Masukin ciphertext yang mau didekripsi.
4. Program menghitung invers kunci mod 26, lalu dipakai untuk balikin ciphertext jadi plaintext.
5. Kalau kuncinya ternyata tidak punya invers (determinannya tidak koprima sama 26), program kasih tahu dekripsi tidak bisa dilakukan.

### 3. Kalau pilih Cari Kunci

Ini buat kasus dimana kita tahu sepasang plaintext dan ciphertext-nya, tapi kuncinya belum tahu.

1. Masukin ukuran matriks kunci yang diinginkan.
2. Masukin plaintext yang diketahui.
3. Masukin ciphertext yang diketahui (yang berhubungan dengan plaintext di atas).
4. Program bakal pecah teksnya jadi blok-blok, lalu coba semua kombinasi blok yang mungkin sampai nemu satu kombinasi yang bisa dipakai untuk hitung kuncinya (soalnya tidak semua kombinasi blok bisa dipakai — kalau matriksnya "singular"/tidak punya invers mod 26, ya tidak bisa dipakai, jadi dicoba kombinasi lain).
5. Kalau plaintext/ciphertext-nya kepanjangan atau kependekan, otomatis ditambah huruf `X` di belakang biar pas jadi blok yang lengkap.
6. Kalau memang tidak ada satupun kombinasi yang berhasil (karena hurufnya kurang variatif), program kasih tahu dan minta coba plaintext-ciphertext lain yang lebih panjang/variatif.

### 4. Keluar

Ya tinggal keluar dari program.

## Cara Menjalankan

```
python3 hill_cipher.py
```

## Catatan

- Kunci dimasukkan dalam bentuk **angka**, bukan huruf, dan boleh bilangan berapa saja (negatif, lebih dari 25, dll) karena nanti otomatis di-mod 26 sama program.
- Untuk fitur Cari Kunci, kadang ada plaintext yang emang secara matematis tidak bisa dipakai buat nemu kunci walau sudah dicoba semua kombinasi blok (misalnya karena huruf-hurufnya kurang variasi). Itu bukan salah program, tapi memang keterbatasan metodenya.

## Screenshot Program Berjalan

Contoh sesi program dari menu Enkripsi → Dekripsi → Cari Kunci → Keluar:
