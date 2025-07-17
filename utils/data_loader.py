
# =====================================
# utils/data_loader.py
#
# Fungsi untuk memuat data JSON profil MI dan aktivitas dari folder /data
# =====================================

import json
import os

def load_all_data():
    """
    Memuat semua file JSON dari folder /data dan mengembalikannya dalam dictionary.
    - File yang dimuat: mi_profiles_up.json, mi_profiles_low.json, mi_aktivitas_tk.json
    - Path folder /data dicari relatif dari root proyek
    """
    # Cari folder 'data' relatif dari file ini (naik 1 level ke root)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_folder = os.path.join(base_dir, 'data')

    try:
        with open(os.path.join(data_folder, 'mi_profiles_up.json'), 'r', encoding='utf-8') as f:
            profiles_up = json.load(f)

        with open(os.path.join(data_folder, 'mi_profiles_low.json'), 'r', encoding='utf-8') as f:
            profiles_low = json.load(f)

        with open(os.path.join(data_folder, 'mi_aktivitas_tk.json'), 'r', encoding='utf-8') as f:
            activities = json.load(f)

        print("[INFO] Data JSON (profil dan aktivitas) berhasil dimuat ke memori.")

        # Kembalikan semua data dalam satu dictionary
        return {
            'profiles_up': profiles_up,
            'profiles_low': profiles_low,
            'activities': activities
        }

    except FileNotFoundError as e:
        print(f"[ERROR] File JSON tidak ditemukan. Pastikan folder 'data' ada di root proyek. Error: {e}")
        raise