# utils/intelligence.py

# Modul ini bertanggung jawab untuk mengambil detail kecerdasan
# (seperti soal observasi anak dan wawancara orang tua)
# dari data yang dimuat ke dalam aplikasi.

import os
import sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
# Baris di atas dikomentari karena kita sekarang akan mengakses data melalui
# `current_app.config`, yang merupakan cara standar Flask untuk berbagi
# data di seluruh aplikasi setelah dimuat saat startup.

# Mengimpor objek `current_app` dari Flask.
# `current_app` adalah proxy ke instance aplikasi Flask yang sedang aktif.
# Ini memungkinkan kita mengakses konfigurasi aplikasi dan data yang dimuat.
from flask import current_app

# Variabel ini akan menyimpan daftar nama-nama kecerdasan dalam urutan tertentu.
# Urutan ini penting untuk tampilan UI yang konsisten (misalnya, urutan tab).
# Variabel ini akan diinisialisasi di `app.py` setelah semua data bank soal dimuat,
# karena pada saat modul ini diimpor, `current_app` mungkin belum sepenuhnya siap.
INTELLIGENCE_NAMES_ORDERED = []

def get_intelligence_detail(kecerdasan, jenjang):
    """
    Mengambil detail spesifik untuk suatu jenis kecerdasan dan jenjang pendidikan.
    Fungsi ini akan mencari data soal observasi anak dan wawancara orang tua
    berdasarkan parameter `kecerdasan` (misalnya, 'Linguistik') dan `jenjang`
    (misalnya, 'TK').

    Args:
        kecerdasan (str): Nama jenis kecerdasan (contoh: 'Linguistik', 'Logis-Matematis').
        jenjang (str): Jenjang pendidikan (contoh: 'TK', 'SD').

    Returns:
        dict: Sebuah dictionary yang berisi data soal observasi anak (`anak`),
              data soal wawancara orang tua (`ortu`), skor maksimum untuk anak
              (`max_anak_score`), dan skor maksimum untuk orang tua (`max_ortu_score`).
              Jika data tidak ditemukan, akan mengembalikan list/nilai default kosong.
    """
    # Mengakses data bank_soal yang telah dimuat ke dalam `current_app.config['MI_DATA']`.
    # `MI_DATA` adalah dictionary yang berisi semua data JSON yang dimuat
    # (profiles_up, profiles_low, activities, dan bank_soal).
    # `bank_soal` adalah kunci untuk data bank soal asesmen.
    # Penting: `current_app` harus tersedia dalam konteks permintaan Flask
    # saat fungsi ini dipanggil (misalnya, di dalam rute).
    bank_soal_data = current_app.config['MI_DATA']['bank_soal']

    # Mengambil detail untuk jenis kecerdasan tertentu.
    # Jika kecerdasan tidak ditemukan, akan mengembalikan dictionary kosong.
    detail = bank_soal_data.get(kecerdasan, {})
    
    # Mengambil data soal observasi anak untuk jenjang spesifik.
    # Struktur: `detail[jenjang]['anak']`
    # Jika jenjang atau data anak tidak ada, mengembalikan list kosong.
    anak_data = detail.get(jenjang, {}).get("anak", [])
    # Mengambil skor maksimum untuk observasi anak di jenjang tersebut.
    max_anak_score = detail.get(jenjang, {}).get("max_anak_score", 0)

    # Mengambil data soal wawancara orang tua.
    # Berdasarkan struktur `bank_soal.json` yang baru, data `ortu` berada
    # langsung di bawah kunci kecerdasan (bukan di dalam jenjang spesifik).
    ortu_data = detail.get("ortu", [])
    # Mengambil skor maksimum untuk wawancara orang tua.
    max_ortu_score = detail.get("max_ortu_score", 0)

    # Mengembalikan semua data yang relevan dalam satu dictionary.
    return {
        "anak": anak_data,
        "ortu": ortu_data,
        "max_anak_score": max_anak_score,
        "max_ortu_score": max_ortu_score
    }
