# utils/skoring.py

def skala_observasi(score):
    """Mengubah skor mentah observasi anak menjadi skor skala 1-5."""
    # Pastikan input adalah integer
    try:
        score = int(score)
    except (ValueError, TypeError):
        return 1.0
        
    tabel = {3: 1.0, 4: 2.0, 5: 3.0, 6: 3.7, 7: 4.2, 8: 4.6, 9: 5.0}
    return tabel.get(score, 1.0)

def skala_wawancara(score):
    """Mengubah skor mentah wawancara ortu menjadi skor skala 1-5."""
    # Pastikan input adalah integer
    try:
        score = int(score)
    except (ValueError, TypeError):
        return 1.0

    tabel = {0: 1.0, 1: 2.5, 2: 3.5, 3: 4.3, 4: 5.0}
    return tabel.get(score, 1.0)

def hitung_skor_gabungan(data, bobot_anak=0.7):
    """
    Menghitung skor gabungan dengan bobot yang bisa disesuaikan.
    bobot_anak adalah persentase dari 0.0 hingga 1.0.
    """
    hasil = {}
    bobot_ortu = 1.0 - bobot_anak # Bobot ortu dihitung otomatis

    for kec, sumber in data.items():
        skor_anak = skala_observasi(sumber.get('anak', 3))
        skor_ortu = skala_wawancara(sumber.get('ortu', 0))
        
        # Perhitungan skor gabungan dengan bobot dinamis
        skor_gabungan = round((skor_anak * bobot_anak) + (skor_ortu * bobot_ortu), 2)
        
        hasil[kec] = {
            'anak': skor_anak,
            'ortu': skor_ortu,
            'gabungan': skor_gabungan
        }
    return hasil
