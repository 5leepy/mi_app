// admin_bulk_delete.js
// Fungsionalitas Hapus Massal Siswa untuk Super Admin Dashboard

let deleteModeActive = false;

// Aktif/nonaktifkan mode hapus massal
function toggleDeleteMode() {
    deleteModeActive = !deleteModeActive;
    const btn = document.getElementById('toggleDeleteModeBtn');
    const deleteCols = document.querySelectorAll('.delete-col');
    const deleteContainer = document.getElementById('deleteActionContainer');
    if (deleteModeActive) {
        btn.textContent = 'Batalkan Mode Hapus';
        btn.classList.add('bg-yellow-200');
        deleteContainer.classList.remove('hidden');
        deleteCols.forEach(col => col.classList.remove('hidden'));
    } else {
        btn.textContent = 'Aktifkan Mode Hapus';
        btn.classList.remove('bg-yellow-200');
        deleteContainer.classList.add('hidden');
        document.querySelectorAll('.row-checkbox').forEach(cb => cb.checked = false);
        document.getElementById('selectAll').checked = false;
        updateSelectedCount();
    }
}

// Centang/uncentang semua baris sekaligus
function toggleAllCheckboxes(source) {
    document.querySelectorAll('.row-checkbox').forEach(checkbox => checkbox.checked = source.checked);
    updateSelectedCount();
}

// Update jumlah siswa yang dipilih
function updateSelectedCount() {
    const count = document.querySelectorAll('.row-checkbox:checked').length;
    document.getElementById('selectedCount').textContent = `${count} siswa dipilih`;
}

// Event listener: update jumlah terpilih saat checkbox berubah
document.querySelectorAll('.row-checkbox').forEach(cb => cb.addEventListener('change', updateSelectedCount));
