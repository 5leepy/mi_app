import sqlite3

# =====================================
# cek_hasil.py
#
# Script sederhana untuk mengecek hasil tes siswa dari database SQLite.
#
# Langkah:
# 1. Ubah variabel siswa_id sesuai ID siswa yang ingin dicek.
# 2. Jalankan script ini untuk menampilkan hasil tes dari tabel 'hasil_tes'.
# =====================================

# Path ke database SQLite
conn = sqlite3.connect("mi_app.sqlite")
cursor = conn.cursor()

# ID siswa yang ingin dicek (ubah sesuai kebutuhan)
siswa_id = 10

# Query hasil tes untuk siswa tertentu
cursor.execute("SELECT * FROM hasil_tes WHERE siswa_id = ?", (siswa_id,))
data = cursor.fetchall()

# Tampilkan hasil query
for row in data:
    print(row)

# Tutup koneksi database
conn.close()
