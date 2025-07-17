
# =====================================
# database.py
#
# Modul utilitas database untuk aplikasi Flask:
# - Koneksi dan penutupan database SQLite
# - Inisialisasi tabel dari schema.sql
# - Integrasi dengan Flask CLI
# =====================================

import sqlite3
from flask import g
from config import DATABASE


# ---------------------------
# Fungsi koneksi database
# ---------------------------

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ---------------------------
# Fungsi inisialisasi tabel database
# ---------------------------

def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())
    print("[DEBUG] Database diinisialisasi dengan schema.sql")


# ---------------------------
# Fungsi untuk integrasi database dengan Flask app
# ---------------------------

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# ---------------------------
# Perintah CLI untuk inisialisasi database
# ---------------------------

import click
from flask import current_app

@click.command('init-db')
def init_db_command():
    """
    Clear data dan buat tabel baru (reset database).
    Jalankan perintah ini melalui Flask CLI: flask init-db
    """
    init_db()
    click.echo('Database berhasil diinisialisasi.')
