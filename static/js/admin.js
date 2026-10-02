/**
 * Administrator Panel Charts and CRUD Modals Client Script
 */

document.addEventListener('DOMContentLoaded', () => {
  initAdminCharts();
  initAdminModals();
});

function initAdminCharts() {
  if (typeof Chart === 'undefined') return;

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#94a3b8' : '#64748b';

  // 1. Applications Funnel Chart
  const appCanvas = document.getElementById('adminAppStatusChart');
  if (appCanvas) {
    const rawData = JSON.parse(appCanvas.getAttribute('data-chart') || '{}');
    new Chart(appCanvas, {
      type: 'doughnut',
      data: {
        labels: Object.keys(rawData),
        datasets: [{
          data: Object.values(rawData),
          backgroundColor: ['#6366f1', '#f59e0b', '#06b6d4', '#10b981', '#f43f5e', '#a855f7'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: textColor, boxWidth: 12, padding: 12, font: { family: "'Plus Jakarta Sans', sans-serif" } }
          }
        },
        cutout: '65%'
      }
    });
  }

  // 2. Internship Domains Bar Chart
  const domainCanvas = document.getElementById('adminDomainChart');
  if (domainCanvas) {
    const rawData = JSON.parse(domainCanvas.getAttribute('data-chart') || '{}');
    new Chart(domainCanvas, {
      type: 'bar',
      data: {
        labels: Object.keys(rawData),
        datasets: [{
          label: 'Internships',
          data: Object.values(rawData),
          backgroundColor: '#4f46e5',
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            ticks: { color: textColor, maxRotation: 45, minRotation: 30, font: { size: 10 } },
            grid: { display: false }
          },
          y: {
            ticks: { color: textColor, precision: 0 },
            grid: { color: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)' }
          }
        }
      }
    });
  }

  // 3. Student Category Distribution Chart
  const catCanvas = document.getElementById('adminCategoryChart');
  if (catCanvas) {
    const rawData = JSON.parse(catCanvas.getAttribute('data-chart') || '{}');
    new Chart(catCanvas, {
      type: 'pie',
      data: {
        labels: Object.keys(rawData),
        datasets: [{
          data: Object.values(rawData),
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: textColor, boxWidth: 12, padding: 12 }
          }
        }
      }
    });
  }
}

function initAdminModals() {
  // Scholarship Edit Modal Trigger
  document.querySelectorAll('.btn-edit-scholarship').forEach(btn => {
    btn.addEventListener('click', () => {
      const data = JSON.parse(btn.getAttribute('data-item'));
      document.getElementById('editSchForm').action = `/admin/scholarship/edit/${data.id}`;
      document.getElementById('editSchName').value = data.name;
      document.getElementById('editSchProvider').value = data.provider;
      document.getElementById('editSchAmount').value = data.amount;
      document.getElementById('editSchAmountNum').value = data.amount_numeric || 0;
      document.getElementById('editSchDeadline').value = data.deadline;
      document.getElementById('editSchCgpa').value = data.minimum_cgpa || 0;
      document.getElementById('editSchIncome').value = data.maximum_income || 0;
      document.getElementById('editSchBranches').value = data.eligible_branches || 'All';
      document.getElementById('editSchCategories').value = data.eligible_categories || 'All';
      document.getElementById('editSchDocs').value = data.required_documents || '';
      document.getElementById('editSchUrl').value = data.application_url || '#';
      document.getElementById('editSchDesc').value = data.description;
      openModal('editScholarshipModal');
    });
  });

  // Internship Edit Modal Trigger
  document.querySelectorAll('.btn-edit-internship').forEach(btn => {
    btn.addEventListener('click', () => {
      const data = JSON.parse(btn.getAttribute('data-item'));
      document.getElementById('editInternForm').action = `/admin/internship/edit/${data.id}`;
      document.getElementById('editInternCompany').value = data.company;
      document.getElementById('editInternTitle').value = data.title;
      document.getElementById('editInternDomain').value = data.domain;
      document.getElementById('editInternWorkMode').value = data.work_mode;
      document.getElementById('editInternLocation').value = data.location;
      document.getElementById('editInternDuration').value = data.duration;
      document.getElementById('editInternStipend').value = data.stipend;
      document.getElementById('editInternSkills').value = Array.isArray(data.required_skills) ? data.required_skills.join(', ') : data.required_skills;
      document.getElementById('editInternDeadline').value = data.deadline;
      document.getElementById('editInternUrl').value = data.application_url || '#';
      document.getElementById('editInternDesc').value = data.description;
      openModal('editInternshipModal');
    });
  });

  // Course Edit Modal Trigger
  document.querySelectorAll('.btn-edit-course').forEach(btn => {
    btn.addEventListener('click', () => {
      const data = JSON.parse(btn.getAttribute('data-item'));
      document.getElementById('editCourseForm').action = `/admin/course/edit/${data.id}`;
      document.getElementById('editCourseName').value = data.name;
      document.getElementById('editCoursePlatform').value = data.platform;
      document.getElementById('editCourseSkill').value = data.skill;
      document.getElementById('editCourseLevel').value = data.level;
      document.getElementById('editCourseDuration').value = data.duration;
      document.getElementById('editCoursePrice').value = data.price;
      document.getElementById('editCourseRating').value = data.rating;
      document.getElementById('editCourseUrl').value = data.course_url || '#';
      document.getElementById('editCourseDesc').value = data.description;
      openModal('editCourseModal');
    });
  });

  // Universal Delete Confirmation Trigger
  document.querySelectorAll('.btn-delete-confirm').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const form = btn.closest('form');
      const itemName = btn.getAttribute('data-name') || 'this item';
      
      document.getElementById('deleteConfirmText').textContent = `Are you sure you want to permanently delete "${itemName}"? This action cannot be undone.`;
      document.getElementById('deleteConfirmBtn').onclick = () => {
        form.submit();
      };
      openModal('deleteConfirmModal');
    });
  });
}
