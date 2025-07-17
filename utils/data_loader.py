# utils/data_loader.py
import json
import os

def load_all_data():
    """
    Memuat semua file JSON dari folder /data dan mengembalikannya 
    dalam sebuah dictionary.
    """
    # Menggunakan path relatif dari file ini untuk menemukan folder 'data'
    # ../ akan naik satu level dari /utils ke root folder proyek
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
        
        # Mengembalikan semua data dalam satu dictionary
        return {
            'profiles_up': profiles_up,
            'profiles_low': profiles_low,
            'activities': activities
        }

    except FileNotFoundError as e:
        print(f"[ERROR] File JSON tidak ditemukan. Pastikan folder 'data' ada di root proyek. Error: {e}")
        raise