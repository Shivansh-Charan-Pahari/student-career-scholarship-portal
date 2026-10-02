/**
 * Student Dashboard Charts & Widgets Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initApplicationChart();
});

function initApplicationChart() {
  const chartCanvas = document.getElementById('applicationStatusChart');
  if (!chartCanvas || typeof Chart === 'undefined') return;

  const applied = parseInt(chartCanvas.getAttribute('data-applied') || 0);
  const underReview = parseInt(chartCanvas.getAttribute('data-under-review') || 0);
  const shortlisted = parseInt(chartCanvas.getAttribute('data-shortlisted') || 0);
  const accepted = parseInt(chartCanvas.getAttribute('data-accepted') || 0);
  const rejected = parseInt(chartCanvas.getAttribute('data-rejected') || 0);

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#94a3b8' : '#64748b';

  new Chart(chartCanvas, {
    type: 'doughnut',
    data: {
      labels: ['Applied', 'Under Review', 'Shortlisted', 'Accepted', 'Rejected'],
      datasets: [{
        data: [applied, underReview, shortlisted, accepted, rejected],
        backgroundColor: [
          '#6366f1', // Indigo
          '#f59e0b', // Amber
          '#06b6d4', // Cyan
          '#10b981', // Emerald
          '#f43f5e'  // Rose
        ],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: textColor,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
            boxWidth: 12,
            padding: 15
          }
        },
        tooltip: {
          backgroundColor: '#0f172a',
          titleFont: { family: "'Outfit', sans-serif", size: 13 },
          bodyFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
          padding: 10,
          cornerRadius: 8
        }
      },
      cutout: '70%'
    }
  });
}
