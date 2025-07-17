# config.py

import os

# Gunakan nilai default jika tidak ada variabel lingkungan
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mi_app.sqlite")