# utils/intelligence.py

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))  # agar bisa import bank_soal

from bank_soal import BANK_SOAL as INTELLIGENCE_DETAILS

INTELLIGENCE_NAMES_ORDERED = list(INTELLIGENCE_DETAILS.keys())

def get_intelligence_detail(kecerdasan, jenjang):
    return INTELLIGENCE_DETAILS.get(kecerdasan, {}).get(jenjang, {})