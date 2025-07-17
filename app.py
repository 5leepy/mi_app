
# =============================
# app.py
#
# Entry point aplikasi Flask utama.
# Mengatur konfigurasi, blueprint, filter Jinja, dan context processor.
# =============================

from flask import Flask
from config import SECRET_KEY
from database import init_app
from utils.filters import ALL_FILTERS
from datetime import datetime
from utils.data_loader import load_all_data

def create_app():
    """
    Membuat dan mengkonfigurasi instance aplikasi Flask.
    - Mengatur SECRET_KEY dan data MI ke konfigurasi app
    - Inisialisasi database
    - Mendaftarkan filter Jinja custom
    - Mendaftarkan blueprint routes
    - Menyediakan context processor untuk tahun berjalan
    """
    app = Flask(__name__)
    # Set SECRET_KEY dan data MI ke konfigurasi Flask
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MI_DATA'] = load_all_data()

    # Inisialisasi database (register db ke app)
    init_app(app)

    # Daftarkan semua custom filter Jinja
    for name, func in ALL_FILTERS.items():
        app.jinja_env.filters[name] = func

    # Daftarkan blueprint routes utama
    from routes.asesmen import bp as asesmen_bp
    app.register_blueprint(asesmen_bp)

    from routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    # Inject variabel 'current_year' ke semua template
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    return app


# Membuat instance aplikasi Flask
app = create_app()


# Menjalankan aplikasi jika file ini dieksekusi langsung
if __name__ == '__main__':
    app.run(debug=True)
