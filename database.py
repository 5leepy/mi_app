# database.py

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
# Fungsi inisialisasi tabel
# ---------------------------

def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())
    print("[DEBUG] Database diinisialisasi dengan schema.sql")

# ---------------------------
# Fungsi init_app Flask
# ---------------------------

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# ---------------------------
# CLI Command untuk init db
# ---------------------------

import click
from flask import current_app

@click.command('init-db')
def init_db_command():
    """Clear data dan buat tabel baru."""
    init_db()
    click.echo('Database berhasil diinisialisasi.')
