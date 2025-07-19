# app.py

# File ini adalah titik masuk utama aplikasi Flask.
# Bertanggung jawab untuk membuat dan mengkonfigurasi instance aplikasi,
# memuat data, mendaftarkan blueprint, dan menjalankan server.

from flask import Flask
from config import SECRET_KEY # Mengimpor kunci rahasia dari konfigurasi
from database import init_app # Mengimpor fungsi inisialisasi database
from utils.filters import ALL_FILTERS # Mengimpor filter Jinja2 kustom
from datetime import datetime # Untuk mendapatkan tahun saat ini
from utils.data_loader import load_all_data # Mengimpor fungsi untuk memuat semua data JSON

# Mengimpor modul `intelligence` untuk menginisialisasi `INTELLIGENCE_NAMES_ORDERED`.
# Ini perlu diimpor setelah `app` dibuat dan `MI_DATA` dimuat.
from utils import intelligence 

def create_app():
    """
    Membuat dan mengkonfigurasi instance aplikasi Flask.
    Ini adalah 'pabrik aplikasi' (application factory) yang memungkinkan
    aplikasi dibuat dengan konfigurasi berbeda untuk pengujian atau produksi.
    """
    app = Flask(__name__)
    
    # Mengatur kunci rahasia aplikasi untuk keamanan sesi.
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Memuat semua data konfigurasi dan bank soal dari file JSON
    # ke dalam `app.config['MI_DATA']`. Data ini akan tersedia di seluruh aplikasi.
    app.config['MI_DATA'] = load_all_data()
    
    # Menyimpan referensi ke fungsi `load_all_data` di dalam konfigurasi aplikasi.
    # Ini berguna jika kita perlu memuat ulang data di memori setelah perubahan
    # (misalnya, setelah admin mengedit file JSON melalui UI).
    app.config['MI_DATA_LOADER'] = load_all_data 

    # Menginisialisasi variabel global `INTELLIGENCE_NAMES_ORDERED` di modul `intelligence`.
    # Daftar nama kecerdasan diambil dari kunci utama data bank soal yang baru dimuat.
    # Urutan ini akan digunakan untuk tampilan tab atau navigasi.
    intelligence.INTELLIGENCE_NAMES_ORDERED = list(app.config['MI_DATA']['bank_soal'].keys())
    
    # Menginisialisasi database untuk aplikasi Flask.
    # Ini akan mendaftarkan fungsi `close_db` dan perintah CLI `init-db`.
    init_app(app)

    # Mendaftarkan semua filter Jinja2 kustom yang didefinisikan di `utils/filters.py`.
    # Filter ini memungkinkan transformasi data langsung di dalam template HTML.
    for name, func in ALL_FILTERS.items():
        app.jinja_env.filters[name] = func

    # Mendaftarkan Blueprint untuk mengorganisir rute-rute aplikasi.
    # Blueprint `asesmen` menangani alur asesmen siswa.
    from routes.asesmen import bp as asesmen_bp
    app.register_blueprint(asesmen_bp)

    # Blueprint `admin` menangani fungsionalitas dasbor dan manajemen data admin.
    from routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    # Context processor untuk menyuntikkan variabel `current_year` ke semua template.
    # Ini berguna untuk menampilkan tahun saat ini di footer atau bagian lain.
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    # Mengembalikan instance aplikasi Flask yang sudah dikonfigurasi.
    return app

# Membuat instance aplikasi Flask saat modul ini diimpor.
app = create_app()

if __name__ == '__main__':
    # Menjalankan aplikasi dalam mode debug jika file ini dieksekusi langsung.
    # Mode debug menyediakan fitur seperti auto-reload dan debugger interaktif.
    app.run(debug=True)
