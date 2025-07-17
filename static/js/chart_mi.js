// static/js/chart_mi.js

document.addEventListener('DOMContentLoaded', function () {
    // Ambil data dari <canvas>
    const canvas = document.getElementById("miChart");
    if (!canvas) return;

    const labelsFull = JSON.parse(canvas.dataset.labels);
    
    // Untuk Radar Chart, label penuh lebih baik agar tidak terlalu sempit
    // const shortLabels = labelsFull.map(label => {
    //   const singkat = {
    //     "Linguistik": "Ling", "Logis-Matematis": "Log", "Spasial": "Spa",
    //     "Kinestetik": "Kin", "Musikal": "Mus", "Interpersonal": "Inter",
    //     "Intrapersonal": "Intra", "Naturalis": "Nat"
    //   };
    //   return singkat[label] || label;
    // });

    const dataAnak = JSON.parse(canvas.dataset.anak).map(x => x * 20);
    const dataOrtu = JSON.parse(canvas.dataset.ortu).map(x => x * 20);
    const dataGabungan = JSON.parse(canvas.dataset.gabungan).map(x => x * 20);

    const ctx = canvas.getContext("2d");
    
    // Hancurkan chart lama jika ada untuk mencegah duplikasi
    if (window.miChart instanceof Chart) {
        window.miChart.destroy();
    }

    // Buat chart baru dengan tipe 'radar'
    window.miChart = new Chart(ctx, {
      type: "radar", // *** PERUBAHAN UTAMA DI SINI ***
      data: {
        labels: labelsFull, // Menggunakan label penuh untuk kejelasan
        datasets: [
          {
            label: "Nilai Anak",
            data: dataAnak,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            pointBackgroundColor: "rgba(54, 162, 235, 1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 2,
            hidden: true, // Sembunyikan secara default
          },
          {
            label: "Nilai Orang Tua",
            data: dataOrtu,
            backgroundColor: "rgba(255, 206, 86, 0.2)",
            borderColor: "rgba(255, 206, 86, 1)",
            pointBackgroundColor: "rgba(255, 206, 86, 1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(255, 206, 86, 1)",
            borderWidth: 2,
            hidden: true, // Sembunyikan secara default
          },
          {
            label: "Nilai Gabungan",
            data: dataGabungan,
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            pointBackgroundColor: "rgba(75, 192, 192, 1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
            hidden: false, // Tampilkan data gabungan secara default
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { 
            display: false,
          },
          tooltip: {
            enabled: true,
            callbacks: {
              label: function(context) {
                const value = context.raw;
                return context.dataset.label + ': ' + Math.round(value) + '%';
              }
            }
          },
          // Datalabels seringkali terlalu ramai untuk radar chart, jadi kita nonaktifkan
          datalabels: {
            display: false,
          },
        },
        // Konfigurasi skala untuk radar chart menggunakan 'r'
        scales: {
          r: {
            angleLines: {
              display: true
            },
            suggestedMin: 0,
            suggestedMax: 100,
            pointLabels: {
              font: {
                size: 10
              },
              color: '#333'
            },
            ticks: {
              backdropColor: 'rgba(255, 255, 255, 0.75)',
              stepSize: 20
            }
          }
        }
      },
      // Hapus plugin annotation karena tidak relevan untuk radar chart
      // plugins: [ChartDataLabels, window['chartjs-plugin-annotation']]
    });

    // Fungsi untuk checkbox tetap sama, tetapi kita atur ulang status awalnya
    const toggleMap = [
      ["toggleAnak", 1],
      ["toggleOrtu", 0],
      ["toggleGabungan", 2]
    ];

    toggleMap.forEach(([checkboxId, datasetIndex]) => {
      const checkbox = document.getElementById(checkboxId);
      if (!checkbox) return;

      // Atur status checkbox sesuai dengan data yang ditampilkan/disembunyikan
      checkbox.checked = !window.miChart.data.datasets[datasetIndex].hidden;

      checkbox.addEventListener("change", function () {
        window.miChart.data.datasets[datasetIndex].hidden = !this.checked;
        window.miChart.update();
      });
    });
});
