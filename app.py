# app.py

from flask import Flask
from config import SECRET_KEY
from database import init_app
from utils.filters import ALL_FILTERS
from datetime import datetime
from utils.data_loader import load_all_data

def create_app():
    """Membuat dan mengkonfigurasi instance aplikasi Flask."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MI_DATA'] = load_all_data()

    init_app(app)

    for name, func in ALL_FILTERS.items():
        app.jinja_env.filters[name] = func

    # --- PERUBAHAN: Mendaftarkan blueprint baru ---
    from routes.asesmen import bp as asesmen_bp
    app.register_blueprint(asesmen_bp)

    from routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
