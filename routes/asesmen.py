# routes/asesmen.py

from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from database import get_db
from utils.intelligence import INTELLIGENCE_NAMES_ORDERED, get_intelligence_detail
from utils.skoring import hitung_skor_gabungan
from datetime import datetime, date
import os
import math
import secrets

# Nama blueprint diubah menjadi 'asesmen'
bp = Blueprint('asesmen', __name__)

# --- FUNGSI BANTUAN (Tidak ada perubahan) ---
def get_activity_recommendations(top_intelligences_set, activities_data):
    scored_activities = []
    for activity in activities_data:
        score = 0
        for tag in activity.get("kecerdasan_primer", []):
            if tag in top_intelligences_set: score += 3
        for tag in activity.get("kecerdasan_sekunder", []):
            if tag in top_intelligences_set: score += 1
        if score > 0:
            activity['score'] = score
            scored_activities.append(activity)
    return sorted(scored_activities, key=lambda x: x['score'], reverse=True)

def generate_kode_siswa(s, siswa_id):
    tahun_test = datetime.today().strftime('%y')
    bulan_tanggal = datetime.today().strftime('%m%d')
    kota_kode = s['kota'][:3].upper() if s['kota'] else 'XXX'
    sekolah_kode = s['asal_sekolah'][0].upper() if s['asal_sekolah'] else 'X'
    tahun_lahir = s['tanggal_lahir'][:4] if s['tanggal_lahir'] else '0000'
    return f"R{tahun_test}-{kota_kode}-{sekolah_kode}{bulan_tanggal}-{tahun_lahir[2:]}{siswa_id:03}"

def proses_skor_form(form, siswa_id, sumber, db):
    for key, value in form.items():
        if key.startswith('bobot_anak_persen'): continue
        try:
            parts = key.split('_')
            kecerdasan, pertanyaan_index, nilai = parts[0], int(parts[2]), int(value)
            db.execute('''
                INSERT INTO hasil_tes (siswa_id, sumber, kecerdasan, pertanyaan_index, nilai)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(siswa_id, sumber, kecerdasan, pertanyaan_index) DO UPDATE SET
                nilai = excluded.nilai
            ''', (siswa_id, sumber, kecerdasan, pertanyaan_index, nilai))
        except (ValueError, IndexError): continue
    db.commit()

# --- RUTE UTAMA & MANAJEMEN KASUS ---

@bp.route('/')
def index():
    # Halaman utama sekarang mengarah ke dasbor asesor
    return redirect(url_for('asesmen.asesor_dashboard'))

@bp.route('/dashboard')
def asesor_dashboard():
    """Halaman utama untuk asesor, menampilkan daftar kasus."""
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    total_siswa = db.execute('SELECT COUNT(id) FROM siswa').fetchone()[0]
    
    siswa_list = db.execute(
        '''
        SELECT id, nama, asal_sekolah, nama_ortu, hubungan_wali, url_slug,
        (SELECT COUNT(*) FROM hasil_tes WHERE siswa_id = siswa.id) as tes_diselesaikan
        FROM siswa ORDER BY id DESC LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()
    
    total_pages = math.ceil(total_siswa / per_page)
    
    return render_template(
        'asesor_dashboard.html', 
        siswa_list=siswa_list,
        total_siswa=total_siswa,
        current_page=page,
        total_pages=total_pages
    )

# --- (Sisa dari file ini berisi rute-rute asesmen yang sudah ada) ---
# --- (Pastikan semua url_for() di dalamnya mengarah ke 'asesmen.nama_fungsi') ---

@bp.route('/tambah-siswa', methods=['GET', 'POST'])
def tambah_siswa():
    if request.method == 'POST':
        db = get_db()
        cursor = db.execute('INSERT INTO siswa (nama, tempat_lahir, tanggal_lahir, asal_sekolah, kelas, kota, jenjang) VALUES (?, ?, ?, ?, ?, ?, ?)',(request.form['nama'], request.form['tempat_lahir'], request.form['tanggal_lahir'],request.form['asal_sekolah'], request.form['kelas'], request.form['kota'],request.form['jenjang']))
        db.commit()
        siswa_id = cursor.lastrowid
        kode_unik_cetak = generate_kode_siswa(request.form, siswa_id)
        url_slug_baru = secrets.token_urlsafe(8)
        db.execute('UPDATE siswa SET kode_unik = ?, url_slug = ? WHERE id = ?',(kode_unik_cetak, url_slug_baru, siswa_id))
        db.commit()
        flash(f"Berkas untuk siswa '{request.form['nama']}' berhasil dibuat.", "success")
        return redirect(url_for('asesmen.profil_siswa', url_slug=url_slug_baru))
    return render_template('data_siswa.html')

@bp.route('/profil/<string:url_slug>')
def profil_siswa(url_slug):
    db = get_db()
    siswa = db.execute('SELECT * FROM siswa WHERE url_slug = ?', (url_slug,)).fetchone()
    if not siswa:
        flash("Profil siswa tidak ditemukan.", "error")
        return redirect(url_for('asesmen.asesor_dashboard'))
    status = {
        'data_wali': bool(siswa['nama_ortu']),
        'observasi_anak': db.execute('SELECT 1 FROM hasil_tes WHERE siswa_id = ? AND sumber = ?', (siswa['id'], 'anak')).fetchone() is not None,
        'wawancara_wali': db.execute('SELECT 1 FROM hasil_tes WHERE siswa_id = ? AND sumber = ?', (siswa['id'], 'ortu')).fetchone() is not None
    }
    return render_template('profil_siswa.html', siswa=siswa, status=status)

@bp.route('/profil/<string:url_slug>/data-wali', methods=['GET', 'POST'])
def isi_data_wali(url_slug):
    db = get_db()
    siswa = db.execute('SELECT * FROM siswa WHERE url_slug = ?', (url_slug,)).fetchone()
    if not siswa: return redirect(url_for('asesmen.asesor_dashboard'))
    if request.method == 'POST':
        db.execute('UPDATE siswa SET nama_ortu = ?, no_hp = ?, email = ?, hubungan_wali = ? WHERE id = ?',(request.form.get('nama_ortu', ''),request.form.get('no_hp', ''),request.form.get('email', ''),request.form.get('hubungan_wali', ''),siswa['id']))
        db.commit()
        flash("Data wali berhasil disimpan.", "success")
        return redirect(url_for('asesmen.profil_siswa', url_slug=url_slug))
    return render_template('data_ortu.html', siswa=siswa)

@bp.route('/profil/<string:url_slug>/observasi-anak', methods=['GET', 'POST'])
def observasi_anak(url_slug):
    db = get_db()
    siswa = db.execute('SELECT * FROM siswa WHERE url_slug = ?', (url_slug,)).fetchone()
    if not siswa: return redirect(url_for('asesmen.asesor_dashboard'))
    if request.method == 'POST':
        proses_skor_form(request.form, siswa['id'], 'anak', db)
        flash("Data observasi anak berhasil disimpan.", "success")
        return redirect(url_for('asesmen.profil_siswa', url_slug=url_slug))
    detail = {kec: get_intelligence_detail(kec, siswa['jenjang']) for kec in INTELLIGENCE_NAMES_ORDERED}
    jawaban_lama_raw = db.execute('SELECT kecerdasan, pertanyaan_index, nilai FROM hasil_tes WHERE siswa_id = ? AND sumber = ?', (siswa['id'], 'anak')).fetchall()
    jawaban_lama = {f"{row['kecerdasan']}_anak_{row['pertanyaan_index']}": row['nilai'] for row in jawaban_lama_raw}
    return render_template('soal_anak.html', siswa=siswa, detail=detail, jawaban_lama=jawaban_lama)

@bp.route('/profil/<string:url_slug>/wawancara-wali', methods=['GET', 'POST'])
def wawancara_wali(url_slug):
    db = get_db()
    siswa = db.execute('SELECT * FROM siswa WHERE url_slug = ?', (url_slug,)).fetchone()
    if not siswa: return redirect(url_for('asesmen.asesor_dashboard'))
    if request.method == 'POST':
        proses_skor_form(request.form, siswa['id'], 'ortu', db)
        bobot_anak_persen = request.form.get('bobot_anak_persen', 70, type=int)
        bobot_anak_float = bobot_anak_persen / 100.0
        db.execute('UPDATE siswa SET bobot_anak = ? WHERE id = ?', (bobot_anak_float, siswa['id']))
        db.commit()
        flash("Data wawancara wali berhasil disimpan.", "success")
        return redirect(url_for('asesmen.profil_siswa', url_slug=url_slug))
    detail = {kec: get_intelligence_detail(kec, siswa['jenjang']) for kec in INTELLIGENCE_NAMES_ORDERED}
    jawaban_lama_raw = db.execute('SELECT kecerdasan, pertanyaan_index, nilai FROM hasil_tes WHERE siswa_id = ? AND sumber = ?', (siswa['id'], 'ortu')).fetchall()
    jawaban_lama = {f"{row['kecerdasan']}_ortu_{row['pertanyaan_index']}": row['nilai'] for row in jawaban_lama_raw}
    return render_template('soal_ortu.html', siswa=siswa, detail=detail, jawaban_lama=jawaban_lama)

@bp.route('/laporan/<string:url_slug>')
def tampil_laporan(url_slug):
    db = get_db()
    siswa = db.execute('SELECT * FROM siswa WHERE url_slug = ?', (url_slug,)).fetchone()
    if not siswa:
        flash(f"Laporan tidak ditemukan.", "error")
        return redirect(url_for('asesmen.asesor_dashboard'))
    hasil_mentah = {}
    data_tes_raw = db.execute('SELECT kecerdasan, sumber, SUM(nilai) as total_nilai FROM hasil_tes WHERE siswa_id = ? GROUP BY kecerdasan, sumber', (siswa['id'],)).fetchall()
    if not data_tes_raw:
         flash("Data tes belum lengkap untuk membuat laporan.", "warning")
         return redirect(url_for('asesmen.profil_siswa', url_slug=url_slug))
    for row in data_tes_raw:
        hasil_mentah.setdefault(row['kecerdasan'], {})[row['sumber']] = row['total_nilai']
    bobot_anak = siswa['bobot_anak'] if siswa['bobot_anak'] is not None else 0.7
    hasil_akhir = hitung_skor_gabungan(hasil_mentah, bobot_anak=bobot_anak)
    sorted_kecerdasan = sorted(hasil_akhir.items(), key=lambda item: item[1]['gabungan'], reverse=True)
    top_3_intelligences, bottom_2_intelligences = sorted_kecerdasan[:3], sorted(sorted_kecerdasan[-2:], key=lambda item: item[1]['gabungan'])
    top_3_names_set, bottom_2_names_set = {item[0] for item in top_3_intelligences}, {item[0] for item in bottom_2_intelligences}
    mi_data = current_app.config['MI_DATA']
    profil_narasi, low_profile_narasi = {}, {}
    for key, profile_data in mi_data['profiles_up'].items():
        if top_3_names_set == {i for i in INTELLIGENCE_NAMES_ORDERED if i in key}:
            profil_narasi = profile_data
            break
    for key, profile_data in mi_data['profiles_low'].items():
        if bottom_2_names_set == {i for i in INTELLIGENCE_NAMES_ORDERED if i in key}:
            low_profile_narasi = profile_data
            break
    activity_recommendations = get_activity_recommendations(top_3_names_set, mi_data['activities'])
    tanggal_riset = datetime.today().strftime('%d %B %Y')
    return render_template('hasil.html', siswa=siswa, hasil=hasil_akhir, tanggal_riset=tanggal_riset, profil_narasi=profil_narasi, low_profile_narasi=low_profile_narasi, top_3=top_3_intelligences, bottom_2=bottom_2_intelligences, recommendations=activity_recommendations)
