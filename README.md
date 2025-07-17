# Aplikasi Asesmen Kecerdasan Majemuk (MI-App)

**MI-App** adalah sebuah aplikasi web yang dibangun menggunakan Flask untuk memfasilitasi asesmen kecerdasan majemuk pada anak. Aplikasi ini dirancang sebagai alat bantu bagi para asesor atau psikolog profesional untuk mengumpulkan data, mengolahnya dengan parameter yang fleksibel, dan menghasilkan laporan yang komprehensif serta dipersonalisasi.

---

## Fitur Utama

- **Alur Asesmen Terpandu**: Antarmuka yang memandu asesor dari pengisian data siswa hingga wawancara orang tua.
- **Skoring Berbobot**: Asesor dapat mengatur bobot penilaian antara hasil observasi anak dan wawancara orang tua untuk setiap sesi tes, memberikan fleksibilitas diagnostik.
- **Laporan Naratif Dinamis**: Menghasilkan analisis profil, gaya belajar, dan rekomendasi aktivitas yang sangat personal berdasarkan kombinasi kecerdasan dominan dan area pengembangan anak. Semua narasi dimuat dari file JSON.
- **Visualisasi Data Interaktif**: Laporan akhir dilengkapi dengan grafik radar interaktif (Chart.js) untuk memvisualisasikan skor dengan jelas.
- **URL Laporan yang Aman**: Setiap laporan hasil memiliki URL unik yang acak dan aman (`/laporan/<kode-akses>`), ideal untuk dibagikan tanpa mengekspos struktur data internal.
- **Dasbor Admin Fungsional**: Halaman admin (`/admin`) untuk melihat seluruh riwayat asesmen, lengkap dengan paginasi, pencarian, dan fitur hapus massal (*bulk delete*).

---

## Struktur Proyek

Proyek ini memiliki struktur yang modular untuk memisahkan logika, data, dan tampilan.

- **`data/`**: Berisi data JSON untuk profil naratif dan rekomendasi aktivitas.
- **`routes/`**: Mengelola rute dan logika utama aplikasi (`main.py`).
- **`static/`**: Menyimpan file statis seperti JavaScript (`chart_mi.js`) dan gambar.
- **`templates/`**: Berisi semua file template HTML yang digunakan oleh Jinja2.
- **`utils/`**: Kumpulan modul bantuan untuk skoring, filter, dan pemuatan data.
- **`app.py`**: Titik masuk utama dan pabrik aplikasi Flask.
- **`config.py`**: Menyimpan konfigurasi aplikasi, seperti `SECRET_KEY`.
- **`database.py`**: Mengelola koneksi dan inisialisasi database.
- **`requirements.txt`**: Daftar semua dependensi Python yang dibutuhkan proyek.
- **`schema.sql`**: Skema SQL untuk membuat struktur tabel di database SQLite.
- **`README.md`**: File dokumentasi yang sedang Anda baca.

---

## Instalasi dan Menjalankan

### 1. Persiapan Awal

- Pastikan Anda memiliki Python 3 terinstal.
- Disarankan untuk menggunakan *virtual environment*.

```bash
# Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv

# Aktifkan virtual environment
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

2. Instalasi Dependensi
Install semua pustaka Python yang dibutuhkan melalui file requirements.txt.

pip install -r requirements.txt

3. Inisialisasi Database
Sebelum menjalankan aplikasi untuk pertama kali, inisialisasi database menggunakan perintah Flask CLI yang telah disediakan. Perintah ini akan membuat file mi_app.sqlite dan tabel-tabel di dalamnya sesuai dengan schema.sql.

flask --app app.py init-db

Jika berhasil, akan muncul pesan: Database berhasil diinisialisasi.

4. Menjalankan Aplikasi
Jalankan server pengembangan Flask.

flask --app app.py run

Aplikasi sekarang dapat diakses melalui browser di alamat https://www.google.com/search?q=http://127.0.0.1:5000/

Alur Kerja Aplikasi
Mulai Asesmen: Dari halaman utama, asesor memulai sesi baru.

Formulir Data: Asesor mengisi data siswa, lalu data orang tua.

Sesi Observasi & Wawancara: Asesor mengisi skor berdasarkan observasi anak dan wawancara orang tua. Di halaman wawancara, asesor dapat mengatur bobot skor sesuai pertimbangan profesional.

Halaman Laporan: Setelah selesai, aplikasi akan mengarahkan ke URL laporan yang unik (misal: /laporan/aK7b-Z9pX). Halaman ini menampilkan analisis lengkap dan siap untuk dicetak atau dibagikan.

Dasbor Admin: Asesor dapat mengunjungi /admin untuk melihat semua riwayat laporan, mencari data, dan melakukan manajemen data.

Konfigurasi untuk Produksi
Untuk penggunaan di lingkungan produksi (bukan pengembangan), sangat penting untuk mengatur SECRET_KEY yang aman.

SECRET_KEY: Kunci ini digunakan untuk mengamankan sesi pengguna. Atur kunci ini sebagai environment variable.

Contoh (di Linux/macOS):

export SECRET_KEY='kunci_rahasia_yang_sangat_panjang_dan_acak'
flask --app app.py run
