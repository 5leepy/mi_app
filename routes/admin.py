# routes/admin.py

# Blueprint baru untuk admin dengan prefix /admin
# Modul ini berisi rute-rute dan logika untuk fungsionalitas admin,
# seperti dasbor manajemen siswa dan fitur-fitur khusus admin.

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from database import get_db
import math
import os # Impor modul os untuk path file

# Blueprint baru untuk admin dengan prefix /admin
bp = Blueprint('admin', __name__, url_prefix='/admin')

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
        (SELECT COUNT(*) FROM hasil_tes WHERE siswa_id = siswa.id) as tes_diselesaikan
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


# --- Rute Baru untuk Ekspor File JSON (Backup) ---
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

