# routes/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db
import math

# Blueprint baru untuk admin dengan prefix /admin
bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
def dashboard():
    """Halaman dasbor untuk Super Admin dengan hak akses penuh."""
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    total_siswa = db.execute('SELECT COUNT(id) FROM siswa').fetchone()[0]
    
    siswa_list = db.execute(
        '''
        SELECT id, nama, asal_sekolah, nama_ortu, hubungan_wali, url_slug, bobot_anak,
        (SELECT COUNT(*) FROM hasil_tes WHERE siswa_id = siswa.id) as tes_diselesaikan
        FROM siswa ORDER BY id DESC LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()
    
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
    """Fungsi untuk menghapus data siswa secara massal."""
    selected_ids = request.form.getlist('selected_ids')
    if not selected_ids:
        flash('Tidak ada siswa yang dipilih untuk dihapus.', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    db = get_db()
    try:
        placeholders = ','.join('?' for _ in selected_ids)
        db.execute(f'DELETE FROM hasil_tes WHERE siswa_id IN ({placeholders})', selected_ids)
        db.execute(f'DELETE FROM siswa WHERE id IN ({placeholders})', selected_ids)
        db.commit()
        flash(f'{len(selected_ids)} data siswa berhasil dihapus secara permanen.', 'success')
    except db.Error as e:
        db.rollback()
        flash(f'Terjadi kesalahan saat menghapus data: {e}', 'error')
    
    return redirect(url_for('admin.dashboard'))
