# routes/admin.py

# Blueprint baru untuk admin dengan prefix /admin
# Modul ini berisi rute-rute dan logika untuk fungsionalitas admin,
# seperti dasbor manajemen siswa dan fitur-fitur khusus admin.

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from database import get_db
import math
import os # Impor modul os untuk path file
import json # Impor modul json untuk membaca/menulis JSON
import copy # Impor modul copy untuk deepcopy

# Blueprint baru untuk admin dengan prefix /admin
bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- Fungsi Bantu untuk Menyimpan Data MI ke File JSON ---
def _save_mi_data_to_files(mi_data):
    """
    Menyimpan seluruh data kecerdasan majemuk (MI_DATA) dari memori
    kembali ke file-file JSON yang sesuai di folder 'data/'.
    Ini penting setelah ada perubahan data master melalui UI.
    """
    data_folder = os.path.join(current_app.root_path, 'data')

    try:
        # Menyimpan bank_soal.json
        with open(os.path.join(data_folder, 'bank_soal.json'), 'w', encoding='utf-8') as f:
            json.dump(mi_data['bank_soal'], f, indent=2, ensure_ascii=False)
        
        # Menyimpan mi_profiles_up.json
        with open(os.path.join(data_folder, 'mi_profiles_up.json'), 'w', encoding='utf-8') as f:
            json.dump(mi_data['profiles_up'], f, indent=2, ensure_ascii=False)
            
        # Menyimpan mi_profiles_low.json
        with open(os.path.join(data_folder, 'mi_profiles_low.json'), 'w', encoding='utf-8') as f:
            json.dump(mi_data['profiles_low'], f, indent=2, ensure_ascii=False)
            
        # Menyimpan mi_aktivitas_tk.json
        with open(os.path.join(data_folder, 'mi_aktivitas_tk.json'), 'w', encoding='utf-8') as f:
            json.dump(mi_data['activities'], f, indent=2, ensure_ascii=False)
            
        print("[INFO] Data JSON berhasil disimpan kembali ke file.")
        # Memuat ulang data ke memori aplikasi agar perubahan langsung terlihat
        current_app.config['MI_DATA'] = current_app.config['MI_DATA_LOADER']()
        return True
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan data JSON ke file: {e}")
        return False

@bp.route('/')
def dashboard():
    """
    Halaman dasbor untuk Super Admin dengan hak akses penuh.
    Menampilkan daftar siswa, status asesmen, dan opsi manajemen data.
    """
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Menghitung total siswa untuk paginasi
    total_siswa = db.execute('SELECT COUNT(id) FROM siswa').fetchone()[0]
    
    # Mengambil daftar siswa dengan status tes yang diselesaikan
    siswa_list = db.execute(
        '''
        SELECT id, nama, asal_sekolah, nama_ortu, hubungan_wali, url_slug, bobot_anak,
        (SELECT COUNT(*) FROM hasil_tes WHERE siswa.id = hasil_tes.siswa_id) as tes_diselesaikan
        FROM siswa ORDER BY id DESC LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()
    
    # Menghitung total halaman untuk paginasi
    total_pages = math.ceil(total_siswa / per_page)
    
    return render_template(
        'admin_super_dashboard.html', 
        siswa_list=siswa_list,
        total_siswa=total_siswa,
        current_page=page,
        total_pages=total_pages
    )

@bp.route('/bulk-delete', methods=['POST'])
def bulk_delete_siswa():
    """
    Fungsi untuk menghapus data siswa secara massal.
    Menerima daftar ID siswa yang dipilih dari formulir.
    """
    selected_ids = request.form.getlist('selected_ids')
    if not selected_ids:
        flash('Tidak ada siswa yang dipilih untuk dihapus.', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    db = get_db()
    try:
        # Membuat placeholder untuk query SQL (misalnya ?, ?, ?)
        placeholders = ','.join('?' for _ in selected_ids)
        
        # Menghapus data hasil tes yang terkait dengan siswa yang dipilih
        db.execute(f'DELETE FROM hasil_tes WHERE siswa_id IN ({placeholders})', selected_ids)
        # Menghapus data siswa itu sendiri
        db.execute(f'DELETE FROM siswa WHERE id IN ({placeholders})', selected_ids)
        db.commit() # Menyimpan perubahan ke database
        
        flash(f'{len(selected_ids)} data siswa berhasil dihapus secara permanen.', 'success')
    except db.Error as e:
        db.rollback() # Mengembalikan perubahan jika terjadi kesalahan
        flash(f'Terjadi kesalahan saat menghapus data: {e}', 'error')
    
    return redirect(url_for('admin.dashboard'))


@bp.route('/export-json/<filename>')
def export_json(filename):
    """
    Mengizinkan admin untuk mengunduh file JSON data master sebagai backup.
    Hanya mengizinkan file-file tertentu untuk diunduh demi keamanan.
    """
    # Menentukan direktori tempat file JSON disimpan (folder 'data/')
    data_folder = os.path.join(current_app.root_path, 'data')
    file_path = os.path.join(data_folder, filename)

    # Daftar file yang diizinkan untuk diunduh.
    # Ini adalah langkah keamanan penting untuk mencegah pengunduhan file sensitif.
    allowed_files = [
        'bank_soal.json',
        'mi_profiles_up.json',
        'mi_profiles_low.json',
        'mi_aktivitas_tk.json'
    ]

    # Memeriksa apakah nama file yang diminta ada dalam daftar yang diizinkan
    if filename not in allowed_files:
        flash('File tidak diizinkan untuk diunduh.', 'error')
        return redirect(url_for('admin.dashboard')) # Atau halaman error lain

    # Memeriksa apakah file benar-benar ada di server
    if not os.path.exists(file_path):
        flash(f'File {filename} tidak ditemukan di server.', 'error')
        return redirect(url_for('admin.dashboard'))

    try:
        # Mengirim file JSON sebagai lampiran (download)
        # `as_attachment=True` akan memaksa browser untuk mengunduh file
        # `download_name` mengatur nama file saat diunduh
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype='application/json')
    except Exception as e:
        flash(f'Terjadi kesalahan saat mengunduh file: {e}', 'error')
        return redirect(url_for('admin.dashboard'))

@bp.route('/bank-soal')
def bank_soal_index():
    """
    Menampilkan daftar semua jenis kecerdasan yang ada di bank soal.
    Ini adalah titik masuk untuk mengelola soal-soal asesmen.
    """
    # Mengambil data bank soal dari konfigurasi aplikasi yang sudah dimuat.
    # Data ini diakses melalui `current_app.config['MI_DATA']['bank_soal']`.
    bank_soal_data = current_app.config['MI_DATA']['bank_soal']
    
    # Mengambil semua nama kecerdasan (kunci utama) dari bank soal.
    # Ini akan menjadi daftar yang ditampilkan di halaman.
    intelligences = list(bank_soal_data.keys())
    
    # Mengirim daftar nama kecerdasan ke template HTML untuk ditampilkan.
    return render_template('admin_bank_soal_index.html', intelligences=intelligences)

@bp.route('/bank-soal/<string:intelligence_name>', methods=['GET', 'POST'])
def manage_intelligence_questions(intelligence_name):
    """
    Menampilkan detail soal untuk jenis kecerdasan tertentu,
    dibagi berdasarkan jenjang (TK, SD, dll.) dan sumber (anak/ortu).
    Juga menangani pembaruan skor maksimum.
    """
    bank_soal_data = current_app.config['MI_DATA'] # Ambil seluruh MI_DATA
    current_bank_soal = copy.deepcopy(bank_soal_data['bank_soal']) # Salinan yang bisa dimodifikasi
    
    # Mencari data untuk jenis kecerdasan yang diminta.
    intelligence_detail = current_bank_soal.get(intelligence_name)
    if not intelligence_detail:
        flash(f'Kecerdasan "{intelligence_name}" tidak ditemukan di bank soal.', 'error')
        return redirect(url_for('admin.bank_soal_index'))

    # --- Penanganan Permintaan POST (Update Skor Maksimum) ---
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        # Update max_ortu_score (global untuk kecerdasan ini)
        try:
            new_max_ortu_score = int(form_data.get('max_ortu_score', 0))
            intelligence_detail['max_ortu_score'] = new_max_ortu_score
            flash('Skor maksimum wawancara orang tua berhasil diperbarui.', 'success')
        except ValueError:
            flash('Skor maksimum wawancara orang tua harus berupa angka.', 'error')

        # Update max_anak_score per jenjang
        for jenjang_key in intelligence_detail.keys():
            if jenjang_key not in ['ortu', 'max_ortu_score']: # Pastikan itu kunci jenjang
                max_anak_score_field_name = f'max_anak_score_{jenjang_key}'
                try:
                    new_max_anak_score = int(form_data.get(max_anak_score_field_name, 0))
                    if 'max_anak_score' in intelligence_detail.get(jenjang_key, {}):
                        intelligence_detail[jenjang_key]['max_anak_score'] = new_max_anak_score
                        flash(f'Skor maksimum observasi anak untuk jenjang {jenjang_key} berhasil diperbarui.', 'success')
                except ValueError:
                    flash(f'Skor maksimum observasi anak untuk jenjang {jenjang_key} harus berupa angka.', 'error')
                except KeyError:
                    # Jika struktur max_anak_score belum ada, abaikan atau inisialisasi
                    pass
        
        # Simpan seluruh MI_DATA kembali ke file
        bank_soal_data['bank_soal'] = current_bank_soal # Update bank_soal di MI_DATA
        if _save_mi_data_to_files(bank_soal_data):
            # Redirect untuk mencegah resubmission form
            return redirect(url_for('admin.manage_intelligence_questions', intelligence_name=intelligence_name))
        else:
            flash('Gagal menyimpan perubahan skor maksimum ke file.', 'error')
            # Jika gagal simpan, tetap di halaman ini dengan pesan error

    # --- Penanganan Permintaan GET (Menampilkan Halaman) ---
    # Mengidentifikasi jenjang-jenjang yang tersedia untuk kecerdasan ini.
    available_jenjang = [
        key for key in intelligence_detail.keys() 
        if key not in ['ortu', 'max_ortu_score']
    ]
    available_jenjang.sort(key=lambda x: {'TK':0, 'SD':1, 'SMP':2, 'SMA':3}.get(x, 99))

    return render_template(
        'admin_manage_intelligence_questions.html',
        intelligence_name=intelligence_name,
        intelligence_detail=intelligence_detail, # Kirimkan intelligence_detail yang sudah di-deepcopy
        available_jenjang=available_jenjang
    )

# --- Rute Tambah/Edit Soal Individual ---
@bp.route('/bank-soal/<string:intelligence_name>/<string:jenjang>/<string:sumber>/<int:question_index>/edit', methods=['GET', 'POST'])
@bp.route('/bank-soal/<string:intelligence_name>/<string:jenjang>/<string:sumber>/add', methods=['GET', 'POST'])
def edit_add_question(intelligence_name, jenjang, sumber, question_index=None):
    """
    Menampilkan formulir untuk menambah atau mengedit soal individual.
    Menangani soal observasi anak ('anak') dan wawancara orang tua ('ortu').
    """
    mi_data = current_app.config['MI_DATA'] # Ambil seluruh MI_DATA
    
    # Pastikan kecerdasan, jenjang, dan sumber valid
    if intelligence_name not in mi_data['bank_soal']:
        flash(f'Kecerdasan "{intelligence_name}" tidak ditemukan.', 'error')
        return redirect(url_for('admin.bank_soal_index'))

    # Dapatkan salinan data bank soal untuk dimodifikasi
    current_bank_soal = copy.deepcopy(mi_data['bank_soal'])
    standard_rubrics = mi_data['standard_rubrics'] # Ambil rubrik standar

    question_data = None
    is_editing = question_index is not None

    # Tentukan di mana soal berada dalam struktur JSON
    if sumber == 'anak':
        # Pastikan struktur jenjang ada, jika tidak, inisialisasi
        if jenjang not in current_bank_soal[intelligence_name]:
            current_bank_soal[intelligence_name][jenjang] = {"anak": [], "max_anak_score": 0}
        questions_list = current_bank_soal.get(intelligence_name, {}).get(jenjang, {}).get('anak', [])
    elif sumber == 'ortu':
        # Pastikan struktur ortu ada, jika tidak, inisialisasi
        if 'ortu' not in current_bank_soal[intelligence_name]:
            current_bank_soal[intelligence_name]['ortu'] = []
            current_bank_soal[intelligence_name]['max_ortu_score'] = 0
        questions_list = current_bank_soal.get(intelligence_name, {}).get('ortu', [])
    else:
        flash('Sumber soal tidak valid.', 'error')
        return redirect(url_for('admin.manage_intelligence_questions', intelligence_name=intelligence_name))

    if is_editing:
        if 0 <= question_index < len(questions_list):
            question_data = questions_list[question_index]
        else:
            flash('Indeks soal tidak valid.', 'error')
            return redirect(url_for('admin.manage_intelligence_questions', intelligence_name=intelligence_name))
    else:
        # Inisialisasi question_data dengan struktur default kosong untuk mode 'add'
        if sumber == 'anak':
            question_data = {
                'aktivitas': '',
                'tujuan': '',
                'bahan': '',
                'instruksi': '',
                'rubrik': {'1': '', '2': '', '3': ''}, # Inisialisasi rubrik dengan kunci string
                'opsi_serupa': []
            }
        elif sumber == 'ortu':
            question_data = {
                'pertanyaan': '',
                'rubrik': {'0': '', '0.5': '', '1': ''} # Inisialisasi rubrik ortu dengan kunci string 0, 0.5, 1
            }
    
    # --- Penanganan Permintaan POST (Form Submission) ---
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        # Siapkan data soal baru/yang diperbarui
        new_question = {}
        if sumber == 'anak':
            new_question['aktivitas'] = form_data.get('aktivitas', '')
            new_question['tujuan'] = form_data.get('tujuan', '')
            new_question['bahan'] = form_data.get('bahan', '')
            new_question['instruksi'] = form_data.get('instruksi', '')
            
            # Rubrik anak (skor 1, 2, 3) - Ambil dari dropdown
            new_question['rubrik'] = {
                '1': form_data.get('rubrik_1', ''),
                '2': form_data.get('rubrik_2', ''),
                '3': form_data.get('rubrik_3', '')
            }
            
            # Opsi serupa (opsi_serupa)
            opsi_serupa_list = []
            opsi_names = request.form.getlist('opsi_serupa_name[]')
            opsi_descs = request.form.getlist('opsi_serupa_deskripsi_aktivitas[]')
            opsi_tujuans = request.form.getlist('opsi_serupa_tujuan_opsi[]')

            for i in range(len(opsi_names)):
                if opsi_names[i] and opsi_descs[i]:
                    opsi_serupa_list.append({
                        'nama': opsi_names[i],
                        'deskripsi_aktivitas': opsi_descs[i],
                        'tujuan_opsi': opsi_tujuans[i]
                    })
            new_question['opsi_serupa'] = opsi_serupa_list

        elif sumber == 'ortu':
            new_question['pertanyaan'] = form_data.get('pertanyaan', '')
            # Rubrik ortu (skor 0, 0.5, 1) - Ambil dari dropdown
            new_question['rubrik'] = {
                '0': form_data.get('rubrik_0', ''),
                '0.5': form_data.get('rubrik_0_5', ''), # Gunakan nama field yang sesuai untuk 0.5
                '1': form_data.get('rubrik_1', '')
            }
        
        # Update data di struktur bank_soal_data (yang sudah di-deepcopy)
        if is_editing:
            questions_list[question_index] = new_question
            flash('Soal berhasil diperbarui.', 'success')
        else:
            questions_list.append(new_question)
            flash('Soal baru berhasil ditambahkan.', 'success')

        # Simpan seluruh MI_DATA kembali ke file
        if sumber == 'anak':
            if jenjang not in current_bank_soal[intelligence_name]:
                current_bank_soal[intelligence_name][jenjang] = {"anak": [], "max_anak_score": 0}
            current_bank_soal[intelligence_name][jenjang]['anak'] = questions_list
            # max_anak_score akan dihitung otomatis nanti, jadi tidak perlu di sini
        elif sumber == 'ortu':
            if 'ortu' not in current_bank_soal[intelligence_name]:
                current_bank_soal[intelligence_name]['ortu'] = []
                current_bank_soal[intelligence_name]['max_ortu_score'] = 0
            current_bank_soal[intelligence_name]['ortu'] = questions_list
            # max_ortu_score akan dihitung otomatis nanti, jadi tidak perlu di sini

        mi_data['bank_soal'] = current_bank_soal # Update bank_soal di MI_DATA

        if _save_mi_data_to_files(mi_data):
            return redirect(url_for('admin.manage_intelligence_questions', 
                                     intelligence_name=intelligence_name))
        else:
            flash('Gagal menyimpan perubahan ke file.', 'error')
            question_data = new_question 
            is_editing = True
    
    # --- Penanganan Permintaan GET (Menampilkan Formulir) ---
    return render_template(
        'admin_edit_question.html',
        intelligence_name=intelligence_name,
        jenjang=jenjang,
        sumber=sumber,
        question_data=question_data,
        question_index=question_index,
        is_editing=is_editing,
        standard_rubrics=standard_rubrics # Teruskan rubrik standar ke template
    )

# --- Rute untuk Hapus Soal ---
@bp.route('/bank-soal/<string:intelligence_name>/<string:jenjang>/<string:sumber>/<int:question_index>/delete', methods=['POST'])
def delete_question(intelligence_name, jenjang, sumber, question_index):
    """
    Menghapus soal individual dari bank soal.
    """
    mi_data = current_app.config['MI_DATA']
    current_bank_soal = copy.deepcopy(mi_data['bank_soal'])

    if intelligence_name not in current_bank_soal:
        flash(f'Kecerdasan "{intelligence_name}" tidak ditemukan.', 'error')
        return redirect(url_for('admin.bank_soal_index'))

    questions_list = None
    if sumber == 'anak':
        if jenjang in current_bank_soal[intelligence_name] and 'anak' in current_bank_soal[intelligence_name][jenjang]:
            questions_list = current_bank_soal[intelligence_name][jenjang]['anak']
    elif sumber == 'ortu':
        if 'ortu' in current_bank_soal[intelligence_name]:
            questions_list = current_bank_soal[intelligence_name]['ortu']
    
    if questions_list is None:
        flash('Sumber soal atau jenjang tidak valid untuk penghapusan.', 'error')
        return redirect(url_for('admin.manage_intelligence_questions', intelligence_name=intelligence_name))

    if 0 <= question_index < len(questions_list):
        deleted_question = questions_list.pop(question_index)
        
        # Update data di struktur bank_soal_data
        if sumber == 'anak':
            current_bank_soal[intelligence_name][jenjang]['anak'] = questions_list
            # max_anak_score akan dihitung otomatis nanti
        elif sumber == 'ortu':
            current_bank_soal[intelligence_name]['ortu'] = questions_list
            # max_ortu_score akan dihitung otomatis nanti

        mi_data['bank_soal'] = current_bank_soal

        if _save_mi_data_to_files(mi_data):
            flash(f'Soal "{deleted_question.get("aktivitas") or deleted_question.get("pertanyaan")}" berhasil dihapus.', 'success')
        else:
            flash('Gagal menghapus soal dari file.', 'error')
    else:
        flash('Indeks soal tidak valid untuk penghapusan.', 'error')
    
    return redirect(url_for('admin.manage_intelligence_questions', intelligence_name=intelligence_name))

