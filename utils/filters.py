

# Custom Jinja filters untuk aplikasi Flask

from datetime import datetime
from dateutil.relativedelta import relativedelta
import markdown2

def usia(tanggal_lahir_str):
    """
    Hitung usia dari string tanggal lahir (YYYY-MM-DD),
    hasil: 'X tahun Y bulan'.
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
    Konversi teks markdown (termasuk baris baru) ke HTML.
    """
    if text is None:
        return ''
    return markdown2.markdown(text, extras=["break-on-newline"])

# Daftar filter custom yang siap didaftarkan ke Jinja
ALL_FILTERS = {
    'usia': usia,
    'markdown': markdown_filter,
}
