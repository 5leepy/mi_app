# utils/data_loader.py

# Modul ini bertanggung jawab untuk memuat semua data konfigurasi
# aplikasi dari file-file JSON yang terletak di folder 'data/'.
# Data ini akan disimpan di memori aplikasi untuk akses cepat.

import json
import os

def _load_all_data_from_files():
    """
    Fungsi internal untuk memuat semua file JSON dari folder 'data/'
    dan mengembalikannya dalam sebuah dictionary tunggal.
    Ini memastikan semua data master aplikasi tersedia saat startup.
    """
    # Menentukan jalur absolut ke folder 'data/'
    # `os.path.dirname(__file__)` memberikan direktori tempat file ini berada (`utils/`)
    # `os.path.abspath(...)` mengubahnya menjadi jalur absolut
    # `'..'` naik satu level ke direktori root proyek (`mi_app/`)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_folder = os.path.join(base_dir, 'data')

    try:
        # Memuat data profil kecerdasan menonjol dari mi_profiles_up.json
        with open(os.path.join(data_folder, 'mi_profiles_up.json'), 'r', encoding='utf-8') as f:
            profiles_up = json.load(f)

        # Memuat data profil kecerdasan area pengembangan dari mi_profiles_low.json
        with open(os.path.join(data_folder, 'mi_profiles_low.json'), 'r', encoding='utf-8') as f:
            profiles_low = json.load(f)

        # Memuat data rekomendasi aktivitas untuk TK dari mi_aktivitas_tk.json
        with open(os.path.join(data_folder, 'mi_aktivitas_tk.json'), 'r', encoding='utf-8') as f:
            activities = json.load(f)

        # Memuat data bank soal dari bank_soal.json (INI PERUBAHAN UTAMA)
        # File ini sekarang berisi semua pertanyaan asesmen dan rubriknya.
        with open(os.path.join(data_folder, 'bank_soal.json'), 'r', encoding='utf-8') as f:
            bank_soal_data = json.load(f)
        
        # Log informasi bahwa data berhasil dimuat
        print("[INFO] Data JSON (profil, aktivitas, dan bank soal) berhasil dimuat ke memori.")
        
        # Mengembalikan semua data yang dimuat dalam satu dictionary.
        # Dictionary ini akan diakses melalui `current_app.config['MI_DATA']`.
        return {
            'profiles_up': profiles_up,
            'profiles_low': profiles_low,
            'activities': activities,
            'bank_soal': bank_soal_data # Menyertakan data bank soal yang baru dimuat
        }

    except FileNotFoundError as e:
        # Menangani kasus jika ada file JSON yang tidak ditemukan
        print(f"[ERROR] File JSON tidak ditemukan. Pastikan folder 'data' ada di root proyek. Error: {e}")
        # Meneruskan exception agar aplikasi tidak berjalan tanpa data penting
        raise
    except json.JSONDecodeError as e:
        # Menangani kasus jika format file JSON tidak valid
        print(f"[ERROR] Format file JSON tidak valid. Error: {e}")
        raise

def load_all_data():
    """
    Fungsi publik yang dipanggil oleh `app.py` untuk memuat semua data.
    Ini berfungsi sebagai wrapper untuk fungsi internal `_load_all_data_from_files`.
    """
    return _load_all_data_from_files()
