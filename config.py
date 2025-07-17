
# =====================================
# config.py
#
# Konfigurasi utama aplikasi:
# - SECRET_KEY: Kunci rahasia Flask (bisa di-set lewat environment variable)
# - DATABASE: Path absolut ke file database SQLite
# =====================================

import os

# Ambil SECRET_KEY dari environment, gunakan default jika tidak ada
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

# Path absolut ke file database SQLite
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mi_app.sqlite")