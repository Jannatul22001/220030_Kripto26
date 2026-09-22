# Program Vigenere Cipher (C++)

Program ini buat tugas praktikum Kriptografi, bahasannya tentang **Vigenere Cipher**. Beda sama Hill Cipher yang kuncinya matriks, kunci Vigenere ini berupa kata atau kalimat biasa.

## Alur Program

Programnya sekali jalan langsung selesai (tidak ada menu berulang seperti Hill Cipher), urutannya begini:

1. Program tanya dulu mau mode **Enkripsi (E)** atau **Dekripsi (D)**.
2. Terus diminta masukin teksnya:
   - kalau mode Enkripsi, yang diminta itu **plaintext**.
   - kalau mode Dekripsi, yang diminta itu **ciphertext**.
3. Setelah itu diminta masukin **kuncinya** (boleh satu kata, boleh kalimat, spasi juga boleh, nanti otomatis dibuang sama program).
4. Teks & kuncinya dibersihkan dulu sama program: yang bukan huruf (spasi, angka, tanda baca) dibuang, terus semua huruf dijadikan huruf besar.
5. Bagian intinya, tiap huruf di teks itu digeser sesuai huruf kunci yang sepadan (huruf ke-1 pakai kunci huruf ke-1, huruf ke-2 pakai kunci huruf ke-2, dst), pakai aturan A=0, B=1, ..., Z=25.
   - Kalau kuncinya lebih **pendek** dari teks, kuncinya otomatis **diulang** dari awal lagi sampai panjangnya cukup.
   - Kalau kuncinya lebih **panjang** dari teks, kuncinya otomatis **dipotong** sepanjang teks aja (sisanya tidak dipakai).
   - Ini semua kejadian otomatis gara-gara satu baris kode pakai operator modulo (`%`), jadi tidak perlu bikin kondisi "kalau lebih pendek..." / "kalau lebih panjang..." secara terpisah.
6. Terakhir program nampilin: teks yang sudah dibersihkan, kunci yang benar-benar dipakai (setelah diulang/dipotong), dan hasil akhirnya (ciphertext kalau enkripsi, plaintext kalau dekripsi).

## Cara Menjalankan

```
g++ vigenerecipher.cpp -o vigenerecipher
./vigenerecipher
```

## Catatan

- Kunci tidak boleh kosong / tidak ada hurufnya sama sekali, kalau kosong program bakal kasih pesan error dan langsung berhenti.
- Karena programnya sekali jalan, kalau mau coba mode lain (misal habis enkripsi mau coba dekripsi), tinggal jalankan lagi program-nya dari awal.

## Screenshot Program Berjalan

Contoh dijalankan 2 kali: yang pertama buat enkripsi `OMEGA` dengan kunci `LUL`, yang kedua buat dekripsi hasil enkripsi tadi (untuk buktiin hasilnya balik lagi ke teks aslinya):

![Screenshot program berjalan](screenshot/screenshot_running.png)
