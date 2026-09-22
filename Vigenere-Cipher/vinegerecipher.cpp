#include <iostream>
#include <string>
#include <cctype>
using namespace std;

string bersihkan(string s)
{
    string hasil = "";
    for (char c : s)
    {
        if (isalpha(c))
            hasil += toupper(c);
    }
    return hasil;
}

int main()
{
    cout << "=== VIGENERE CIPHER ===\n";
    cout << "Pilih mode (E = Enkripsi, D = Dekripsi): ";
    char pilihan;
    cin >> pilihan;
    pilihan = toupper(pilihan);
    cin.ignore();

    string teks, kunciAsli;
    cout << (pilihan == 'E' ? "Masukkan plaintext : " : "Masukkan ciphertext: ");
    getline(cin, teks);
    cout << "Masukkan kunci (kata/kalimat): ";
    getline(cin, kunciAsli);

    string t = bersihkan(teks);
    string k = bersihkan(kunciAsli);

    if (k.empty())
    {
        cout << "Kunci tidak boleh kosong (harus ada hurufnya)!\n";
        return 0;
    }

    string hasil = "";
    string kunciDipakai = "";
    for (int i = 0; i < (int)t.size(); i++)
    {
        int p = t[i] - 'A';
        int kk = k[i % k.size()] - 'A';
        int c = (pilihan == 'E') ? (p + kk) % 26 : (p - kk + 26) % 26;
        hasil += (char)('A' + c);
        kunciDipakai += k[i % k.size()];
    }

    cout << "\nTeks dibersihkan   : " << t << "\n";
    cout << "Kunci yang dipakai : " << kunciDipakai << "\n";
    cout << (pilihan == 'E' ? "Hasil ciphertext   : " : "Hasil plaintext    : ") << hasil << "\n";

    return 0;
}