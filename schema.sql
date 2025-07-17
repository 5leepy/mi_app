-- schema.sql

-- Tabel siswa
DROP TABLE IF EXISTS siswa;
CREATE TABLE siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    tempat_lahir TEXT NOT NULL,
    tanggal_lahir TEXT NOT NULL,
    asal_sekolah TEXT NOT NULL,
    kelas TEXT NOT NULL,
    kota TEXT NOT NULL,
    jenjang TEXT NOT NULL,
    nama_ortu TEXT,
    no_hp TEXT,
    email TEXT,
    hubungan_wali TEXT,
    status_cetak INTEGER NOT NULL DEFAULT 0,
    kode_unik TEXT,
    bobot_anak REAL,
    url_slug TEXT UNIQUE,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel hasil_tes (Struktur diubah untuk menyimpan jawaban individual)
DROP TABLE IF EXISTS hasil_tes;
CREATE TABLE hasil_tes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    siswa_id INTEGER NOT NULL,
    sumber TEXT NOT NULL CHECK(sumber IN ('anak', 'ortu')),
    kecerdasan TEXT NOT NULL,
    pertanyaan_index INTEGER NOT NULL, -- Menyimpan indeks pertanyaan (e.g., 0, 1, 2)
    nilai INTEGER NOT NULL,
    FOREIGN KEY (siswa_id) REFERENCES siswa(id) ON DELETE CASCADE,
    -- Mencegah jawaban ganda untuk pertanyaan yang sama
    UNIQUE(siswa_id, sumber, kecerdasan, pertanyaan_index) 
);

-- Tabel admin (opsional untuk login)
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'admin'
);
