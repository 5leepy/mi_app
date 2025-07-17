# utils/intelligence.py

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))  # agar bisa import bank_soal

from bank_soal import BANK_SOAL as INTELLIGENCE_DETAILS

INTELLIGENCE_NAMES_ORDERED = list(INTELLIGENCE_DETAILS.keys())

def get_intelligence_detail(kecerdasan, jenjang):
    """
    Mengambil detail kecerdasan untuk jenjang tertentu.
    Data 'ortu' dan 'max_ortu_score' kini diambil langsung dari tingkat kecerdasan,
    bukan dari dalam jenjang.
    """
    detail = INTELLIGENCE_DETAILS.get(kecerdasan, {})
    
    # Ambil data anak dari jenjang spesifik
    anak_data = detail.get(jenjang, {}).get("anak", [])
    max_anak_score = detail.get(jenjang, {}).get("max_anak_score", 0)

    # Ambil data ortu dan max_ortu_score langsung dari tingkat kecerdasan
    ortu_data = detail.get("ortu", [])
    max_ortu_score = detail.get("max_ortu_score", 0)

    return {
        "anak": anak_data,
        "ortu": ortu_data,
        "max_anak_score": max_anak_score,
        "max_ortu_score": max_ortu_score
    }

