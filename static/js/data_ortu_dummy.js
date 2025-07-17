// data_ortu_dummy.js
// Fungsi untuk mengisi form data orang tua/wali dengan data dummy secara acak

function fillDummyData() {
    const parentFirstNames = ["Agus", "Bambang", "Siti", "Sri", "Hendra", "Rina", "Tono", "Wati"];
    const parentLastNames = ["Santoso", "Wijaya", "Hartono", "Mulyani", "Gunawan", "Lestari"];
    const relations = ["Ibu", "Ayah", "Paman", "Bibi", "Kakek", "Nenek", "Guru"];

    const getRandom = (arr) => arr[Math.floor(Math.random() * arr.length)];

    const firstName = getRandom(parentFirstNames);
    const lastName = getRandom(parentLastNames);
    const fullName = `${firstName} ${lastName}`;
    const emailName = `${firstName.toLowerCase()}.${lastName.toLowerCase()}${Math.floor(Math.random() * 100)}`;

    document.getElementById('nama_ortu').value = fullName;
    document.getElementById('no_hp').value = `081${Math.floor(100000000 + Math.random() * 900000000)}`;
    document.getElementById('email').value = `${emailName}@example.com`;
    document.getElementById('hubungan_wali').value = getRandom(relations);
}
