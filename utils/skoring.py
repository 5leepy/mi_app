
# =====================================
# utils/skoring.py
#
# Utility untuk konversi dan perhitungan skor observasi & wawancara MI
# - skala_observasi: konversi skor mentah observasi anak ke skala 1-5
# - skala_wawancara: konversi skor mentah wawancara ortu ke skala 1-5
# - hitung_skor_gabungan: hitung skor gabungan anak+ortu dengan bobot dinamis
# =====================================

def skala_observasi(score):
    """
    Konversi skor mentah observasi anak (3-9) ke skala 1-5.
    Jika input tidak valid, kembalikan 1.0.
    """
    try:
        score = int(score)
    except (ValueError, TypeError):
        return 1.0
    tabel = {3: 1.0, 4: 2.0, 5: 3.0, 6: 3.7, 7: 4.2, 8: 4.6, 9: 5.0}
    return tabel.get(score, 1.0)

def skala_wawancara(score):
    """
    Konversi skor mentah wawancara ortu (0-4) ke skala 1-5.
    Jika input tidak valid, kembalikan 1.0.
    """
    try:
        score = int(score)
    except (ValueError, TypeError):
        return 1.0
    tabel = {0: 1.0, 1: 2.5, 2: 3.5, 3: 4.3, 4: 5.0}
    return tabel.get(score, 1.0)

def hitung_skor_gabungan(data, bobot_anak=0.7):
    """
    Hitung skor gabungan anak & ortu dengan bobot dinamis.
    - data: dict {kecerdasan: {'anak': skor, 'ortu': skor}}
    - bobot_anak: proporsi skor anak (0.0-1.0), sisanya untuk ortu
    Return: dict {kecerdasan: {'anak', 'ortu', 'gabungan'}}
    """
    hasil = {}
    bobot_ortu = 1.0 - bobot_anak

    for kec, sumber in data.items():
        skor_anak = skala_observasi(sumber.get('anak', 3))
        skor_ortu = skala_wawancara(sumber.get('ortu', 0))
        # Gabungan = (anak * bobot_anak) + (ortu * bobot_ortu)
        skor_gabungan = round((skor_anak * bobot_anak) + (skor_ortu * bobot_ortu), 2)
        hasil[kec] = {
            'anak': skor_anak,
            'ortu': skor_ortu,
            'gabungan': skor_gabungan
        }
    return hasil
