
// =====================================
// static/js/chart_mi.js
//
// Script untuk menampilkan radar chart MI (Multiple Intelligences)
// pada halaman hasil asesmen menggunakan Chart.js
// =====================================

document.addEventListener('DOMContentLoaded', function () {
    // Ambil elemen <canvas> chart
    const canvas = document.getElementById("miChart");
    if (!canvas) return;

    // Ambil data label dan nilai dari atribut data-* pada canvas
    const labelsFull = JSON.parse(canvas.dataset.labels);
    // Data skor dikali 20 agar skala 1-5 menjadi 0-100 (persen)
    const dataAnak = JSON.parse(canvas.dataset.anak).map(x => x * 20);
    const dataOrtu = JSON.parse(canvas.dataset.ortu).map(x => x * 20);
    const dataGabungan = JSON.parse(canvas.dataset.gabungan).map(x => x * 20);

    const ctx = canvas.getContext("2d");

    // Hancurkan chart lama jika ada (untuk mencegah duplikasi saat reload)
    if (window.miChart instanceof Chart) {
        window.miChart.destroy();
    }

    // Inisialisasi radar chart baru
    window.miChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels: labelsFull, // Label kategori MI
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
          legend: { display: false }, // Sembunyikan legend
          tooltip: {
            enabled: true,
            callbacks: {
              label: function(context) {
                const value = context.raw;
                return context.dataset.label + ': ' + Math.round(value) + '%';
              }
            }
          },
          datalabels: { display: false }, // Nonaktifkan datalabels agar chart tidak ramai
        },
        // Skala radar chart
        scales: {
          r: {
            angleLines: { display: true },
            suggestedMin: 0,
            suggestedMax: 100,
            pointLabels: {
              font: { size: 10 },
              color: '#333'
            },
            ticks: {
              backdropColor: 'rgba(255, 255, 255, 0.75)',
              stepSize: 20
            }
          }
        }
      },
    });

    // Inisialisasi checkbox untuk toggle dataset
    const toggleMap = [
      ["toggleAnak", 1],
      ["toggleOrtu", 0],
      ["toggleGabungan", 2]
    ];

    toggleMap.forEach(([checkboxId, datasetIndex]) => {
      const checkbox = document.getElementById(checkboxId);
      if (!checkbox) return;
      // Atur status awal checkbox sesuai dataset
      checkbox.checked = !window.miChart.data.datasets[datasetIndex].hidden;
      checkbox.addEventListener("change", function () {
        window.miChart.data.datasets[datasetIndex].hidden = !this.checked;
        window.miChart.update();
      });
    });
});
