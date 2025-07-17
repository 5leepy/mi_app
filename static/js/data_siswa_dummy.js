// data_siswa_dummy.js
// Fungsi untuk mengisi form data siswa dengan data dummy secara acak

function fillDummyData() {
    const firstNames = ["Adi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hadi", "Indah", "Joko"];
    const lastNames = ["Prasetyo", "Wibowo", "Lestari", "Nugroho", "Susanto", "Wijaya", "Kusuma", "Halim"];
    const cities = ["Surabaya", "Jakarta", "Bandung", "Medan", "Semarang", "Yogyakarta"];
    const schools = ["Tunas Bangsa", "Pelita Harapan", "Ceria", "Negeri 1", "Bintang Kecil"];
    const kelasOptions = ["A", "B"];

    const getRandom = (arr) => arr[Math.floor(Math.random() * arr.length)];

    const today = new Date();
    const currentYear = today.getFullYear();
    const birthYear = currentYear - (Math.floor(Math.random() * 4) + 5); // Usia 5-8 tahun
    const birthMonth = Math.floor(Math.random() * 12);
    const birthDay = Math.floor(Math.random() * 28) + 1;
    const birthDate = new Date(birthYear, birthMonth, birthDay);
    const birthDateString = birthDate.toISOString().split('T')[0];

    document.getElementById('nama').value = `${getRandom(firstNames)} ${getRandom(lastNames)}`;
    document.getElementById('tempat_lahir').value = getRandom(cities);
    document.getElementById('tanggal_lahir').value = birthDateString;
    document.getElementById('asal_sekolah').value = getRandom(schools);
    document.getElementById('kelas').value = getRandom(kelasOptions);
    document.getElementById('jenjang').value = "TK";
    document.getElementById('kota').value = getRandom(cities);
}
