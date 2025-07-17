import sqlite3

# Ganti dengan path ke database Anda
conn = sqlite3.connect("mi_app.sqlite")
cursor = conn.cursor()

# Ganti dengan ID siswa yang ingin Anda cek
siswa_id = 10

# Jalankan query
cursor.execute("SELECT * FROM hasil_tes WHERE siswa_id = ?", (siswa_id,))
data = cursor.fetchall()

# Tampilkan hasil
for row in data:
    print(row)

# Tutup koneksi\conn.close()
