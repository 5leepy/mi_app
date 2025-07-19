import json

# Nama file yang akan dibersihkan
NAMA_FILE = 'data/bank_soal.json'

print(f"Membaca file {NAMA_FILE}...")

# Buka dan baca data dari file JSON
with open(NAMA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Loop melalui setiap jenis kecerdasan (Linguistik, dll.)
for kecerdasan, detail in data.items():
    # Hapus 'max_ortu_score' jika ada
    if 'max_ortu_score' in detail:
        del detail['max_ortu_score']
        print(f"  - Menghapus 'max_ortu_score' dari [{kecerdasan}]")

    # Loop melalui setiap jenjang (TK, SD, dll.) di dalam kecerdasan
    for jenjang, jenjang_detail in detail.items():
        # Pastikan jenjang_detail adalah dictionary (bukan list 'ortu')
        if isinstance(jenjang_detail, dict):
            # Hapus 'max_anak_score' jika ada
            if 'max_anak_score' in jenjang_detail:
                del jenjang_detail['max_anak_score']
                print(f"  - Menghapus 'max_anak_score' dari [{kecerdasan}][{jenjang}]")

# Tulis kembali data yang sudah bersih ke file yang sama
with open(NAMA_FILE, 'w', encoding='utf-8') as f:
    # indent=2 agar file tetap rapi dan mudah dibaca
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nSelesai! File {NAMA_FILE} telah dibersihkan.")
