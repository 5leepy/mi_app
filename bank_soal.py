# bank_soal.py

BANK_SOAL = {
    "Linguistik": {
        "TK": {
            "anak": [
                {"aktivitas": "Tebak Kata dari Deskripsi", "rubrik": {1: "Sulit Menebak", 2: "Perlu Petunjuk/Waktu", 3: "Tepat & Cepat"}},
                {"aktivitas": "Melanjutkan Cerita Berantai", "rubrik": {1: "Sulit Melanjutkan", 2: "Relevan tapi Sederhana", 3: "Kalimat Relevan & Runtut"}},
                {"aktivitas": "Mengulang Kalimat", "rubrik": {1: "Sulit Mengulang", 2: "Ada Kesalahan/Kurang Jelas", 3: "Akurat & Jelas"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda suka mendengarkan cerita atau dongeng? Seberapa sering dia meminta Anda membacakan buku?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda suka berbicara, bercerita, atau bertanya banyak hal?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda mudah menghafal lagu atau sajak anak-anak?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Bagaimana kemampuan anak Anda dalam memahami instruksi atau petunjuk verbal yang kompleks?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    },
    "Logis-Matematis": {
        "TK": {
            "anak": [
                {"aktivitas": "Melanjutkan Pola Gambar", "rubrik": {1: "Sulit Melanjutkan", 2: "Ada Kesalahan/Ragu", 3: "Tepat & Cepat"}},
                {"aktivitas": "Menghitung Objek", "rubrik": {1: "Banyak Kesalahan", 2: "Beberapa Kesalahan", 3: "Benar Semua"}},
                {"aktivitas": "Membandingkan Jumlah", "rubrik": {1: "Tidak Tepat", 2: "Ragu/Perlu Mengulang", 3: "Tepat"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda suka menghitung benda-benda di sekitarnya? Sampai berapa ia bisa menghitung?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda tertarik pada pola, seperti pola warna atau bentuk?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda suka memecahkan teka-teki sederhana, puzzle angka, atau mencari tahu bagaimana sesuatu bekerja?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda sering bertanya 'mengapa' atau 'bagaimana'?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    },
    "Spasial": {
        "TK": {
            "anak": [
                {"aktivitas": "Menggambar Sesuai Instruksi", "rubrik": {1: "Coretan/Sulit Membentuk", 2: "Ada Bagian Kurang/Tidak Sesuai", 3: "Gambar Jelas & Sesuai Instruksi"}},
                {"aktivitas": "Menyelesaikan Puzzle", "rubrik": {1: "Sulit Menyelesaikan", 2: "Butuh Bantuan/Waktu Lama", 3: "Mandiri & Cepat"}},
                {"aktivitas": "Menemukan Benda Tersembunyi", "rubrik": {1: "Tidak Menemukan", 2: "Perlu Bimbingan/Waktu", 3: "Menemukan dengan Cepat"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda suka menggambar, melukis, atau mewarnai? Seberapa detail atau kreatif gambarnya?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda suka bermain balok, Lego, atau mainan konstruksi lainnya?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda mudah menemukan jalan di tempat baru atau mengingat arah?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda menikmati permainan puzzle atau menemukan perbedaan pada gambar?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    },
    "Kinestetik": {
        "TK": {
            "anak": [
                {"aktivitas": "Menirukan Gerakan Hewan", "rubrik": {1: "Tidak Melakukan/Sulit", 2: "Gerakan Kurang Jelas", 3: "Gerakan Jelas & Mirip"}},
                {"aktivitas": "Membuat Bentuk dari Plastisin", "rubrik": {1: "Hanya Meremas", 2: "Bentuk Kurang Jelas", 3: "Bentuk Jelas & Sesuai"}},
                {"aktivitas": "Melakukan Gerakan Sesuai Instruksi", "rubrik": {1: "Sulit Mengikuti", 2: "Ada Kesalahan/Lambat", 3: "Melakukan Semua dengan Tepat"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda sangat aktif secara fisik?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda memiliki koordinasi mata-tangan yang baik?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda suka menari atau meniru gerakan dari televisi/orang lain?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda terampil dalam aktivitas yang melibatkan tangan seperti bermain plastisin atau menggunting?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    },
    
}
BANK_SOAL.update({
    "Musikal": {
        "TK": {
            "anak": [
                {"aktivitas": "Menyanyikan Lagu Favorit", "rubrik": {1: "Tidak Mau Bernyanyi", 2: "Nada/Ritme Kurang Tepat", 3: "Nada & Ritme Cukup Tepat"}},
                {"aktivitas": "Mengenali Suara Binatang", "rubrik": {1: "Sulit Mengidentifikasi", 2: "Ada Kesalahan/Ragu", 3: "Mengidentifikasi Semua dengan Benar"}},
                {"aktivitas": "Mengikuti Pola Ketukan", "rubrik": {1: "Sulit Mengikuti", 2: "Tidak Konsisten", 3: "Mengikuti Pola dengan Akurat"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda suka bernyanyi atau bersenandung, bahkan saat sendirian?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda peka terhadap irama musik?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda bisa membedakan berbagai jenis suara?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda menunjukkan minat pada alat musik atau mencoba membuat suara musikal?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    },
    "Interpersonal": {
        "TK": {
            "anak": [
                {"aktivitas": "Mengenali Ekspresi Wajah", "rubrik": {1: "Sulit Mengidentifikasi", 2: "Ada Kesalahan/Ragu", 3: "Mengidentifikasi Semua dengan Tepat"}},
                {"aktivitas": "Sketsa Skenario Sosial", "rubrik": {1: "Tidak Peduli", 2: "Jawaban Kurang Optimal", 3: "Jawaban Empati/Solusi Positif"}},
                {"aktivitas": "Bermain Peran Sederhana", "rubrik": {1: "Sulit Berinteraksi", 2: "Perlu Bimbingan", 3: "Berinteraksi Aktif & Sesuai Peran"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda mudah berteman atau berinteraksi dengan anak-anak lain?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Bagaimana anak Anda bereaksi ketika melihat orang lain sedih/marah?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda suka bermain kelompok atau berbagi mainan?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda cenderung menjadi pemimpin atau pengikut dalam permainan?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    }
})
BANK_SOAL.update({
    "Intrapersonal": {
        "TK": {
            "anak": [
                {"aktivitas": "Memilih Kegiatan Kesukaan", "rubrik": {1: "Sulit Memilih", 2: "Alasan Sederhana", 3: "Memilih & Memberi Alasan Jelas"}},
                {"aktivitas": "Mengungkapkan Perasaan", "rubrik": {1: "Sulit Mengungkapkan", 2: "Kurang Jelas", 3: "Mengungkapkan Jelas & Memberi Alasan"}},
                {"aktivitas": "Apa yang Membuatmu Bangga?", "rubrik": {1: "Tidak Ada", 2: "Sederhana", 3: "Pengalaman Membanggakan"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda suka bermain sendiri dan fokus pada aktivitasnya?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda bisa mengungkapkan perasaannya sendiri?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda tahu apa yang ia suka dan tidak suka?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda memiliki cita-cita atau keinginan yang kuat?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    },
    "Naturalis": {
        "TK": {
            "anak": [
                {"aktivitas": "Mengidentifikasi Hewan", "rubrik": {1: "Sulit Mengidentifikasi", 2: "Ada Kesalahan/Ragu", 3: "Mengidentifikasi Sebagian Besar"}},
                {"aktivitas": "Mengelompokkan Benda Hidup dan Mati", "rubrik": {1: "Sulit Mengelompokkan", 2: "Beberapa Kesalahan", 3: "Mengelompokkan dengan Tepat"}},
                {"aktivitas": "Mengenali Suara Alam", "rubrik": {1: "Sulit Mengidentifikasi", 2: "Ada Kesalahan/Ragu", 3: "Mengidentifikasi Semua dengan Benar"}}
            ],
            "ortu": [
                {"pertanyaan": "Apakah anak Anda suka berada di luar ruangan, seperti di taman atau kebun?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda tertarik pada hewan atau tumbuhan?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda suka bertanya tentang fenomena alam?", "rubrik": {0: "Tidak", 1: "Ya"}},
                {"pertanyaan": "Apakah anak Anda menunjukkan kepedulian terhadap lingkungan atau makhluk hidup?", "rubrik": {0: "Tidak", 1: "Ya"}}
            ],
            "max_anak_score": 9,
            "max_ortu_score": 4
        }
    }
})