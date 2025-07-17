# utils/filters.py

from datetime import datetime
from dateutil.relativedelta import relativedelta
import markdown2 # <-- Impor library yang baru diinstal

def usia(tanggal_lahir_str):
    """
    Menghitung usia dari string tanggal lahir (YYYY-MM-DD)
    dan mengembalikannya dalam format 'X tahun Y bulan'.
    """
    if not tanggal_lahir_str:
        return "-"
    try:
        tanggal_lahir = datetime.strptime(tanggal_lahir_str, "%Y-%m-%d")
        hari_ini = datetime.today()
        selisih = relativedelta(hari_ini, tanggal_lahir)
        return f"{selisih.years} tahun {selisih.months} bulan"
    except (ValueError, TypeError):
        return "-"

def markdown_filter(text):
    """
    Mengubah teks dengan sintaks Markdown (seperti **bold**) dan
    baris baru menjadi format HTML yang benar.
    """
    if text is None:
        return ''
    # Menggunakan markdown2 untuk konversi.
    # 'break-on-newline' akan mengubah baris baru menjadi <br>
    return markdown2.markdown(text, extras=["break-on-newline"])

# Dictionary untuk mendaftarkan semua filter agar mudah diimpor
ALL_FILTERS = {
    'usia': usia,
    'markdown': markdown_filter, # <-- Gunakan filter markdown yang baru
}
