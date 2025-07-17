
# =====================================
# utils/intelligence.py
#
# Utility untuk manajemen data kecerdasan (Multiple Intelligences)
# - Mengambil detail kecerdasan dari bank_soal
# - Mendukung urutan dan akses data anak/ortu per jenjang
# =====================================


import os
import sys
# Agar bisa import bank_soal dari root project
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))


# Import data bank soal kecerdasan
from bank_soal import BANK_SOAL as INTELLIGENCE_DETAILS


# Daftar nama kecerdasan (sesuai urutan di bank_soal)
INTELLIGENCE_NAMES_ORDERED = list(INTELLIGENCE_DETAILS.keys())

def get_intelligence_detail(kecerdasan, jenjang):
    """
    Ambil detail kecerdasan untuk jenjang tertentu.
    - Data 'anak' & 'max_anak_score' diambil dari jenjang (misal: 'TK')
    - Data 'ortu' & 'max_ortu_score' diambil langsung dari tingkat kecerdasan
    """
    detail = INTELLIGENCE_DETAILS.get(kecerdasan, {})

    # Data anak (per jenjang)
    anak_data = detail.get(jenjang, {}).get("anak", [])
    max_anak_score = detail.get(jenjang, {}).get("max_anak_score", 0)

    # Data ortu (langsung dari tingkat kecerdasan)
    ortu_data = detail.get("ortu", [])
    max_ortu_score = detail.get("max_ortu_score", 0)

    return {
        "anak": anak_data,
        "ortu": ortu_data,
        "max_anak_score": max_anak_score,
        "max_ortu_score": max_ortu_score
    }

