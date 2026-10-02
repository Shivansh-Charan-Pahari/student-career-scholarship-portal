/**
 * Global JavaScript utilities for Student Career & Scholarship Portal
 * - Dark Mode persistence
 * - Mobile Navigation Toggle
 * - Toast Notification System
 * - Global Modal Controls
 * - Instant Search with Auto-Complete
 * - Universal Save/Bookmark API Trigger
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initMobileNav();
  initToasts();
  initGlobalSearch();
  initSaveButtons();
  initTabNavs();
});

/* --- THEME TOGGLE (DARK / LIGHT MODE) --- */
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const savedTheme = localStorage.getItem('portal_theme') || 'light';
  
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('portal_theme', newTheme);
      updateThemeIcon(newTheme);
      showToast('Theme Updated', `Switched to ${newTheme} mode`, 'info');
    });
  }
}

function updateThemeIcon(theme) {
  const themeIcon = document.getElementById('theme-icon');
  if (!themeIcon) return;
  if (theme === 'dark') {
    themeIcon.className = 'fas fa-sun';
  } else {
    themeIcon.className = 'fas fa-moon';
  }
}

/* --- MOBILE NAVIGATION TOGGLE --- */
function initMobileNav() {
  const toggleBtn = document.getElementById('mobile-nav-toggle');
  const navLinks = document.getElementById('nav-links');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }
}

/* --- TOAST NOTIFICATIONS --- */
function initToasts() {
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(t => {
    setTimeout(() => {
      t.style.opacity = '0';
      setTimeout(() => t.remove(), 300);
    }, 4500);
  });
}

function showToast(title, message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = {
    success: 'fa-check-circle',
    danger: 'fa-exclamation-circle',
    warning: 'fa-exclamation-triangle',
    info: 'fa-info-circle'
  };

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fas ${icons[type] || icons.info} toast-icon"></i>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

/* --- GLOBAL MODAL CONTROLS --- */
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
}

// Close when clicking outside modal box
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('show');
    document.body.style.overflow = '';
  }
});

/* --- GLOBAL SEARCH AUTO-COMPLETE --- */
function initGlobalSearch() {
  const searchInput = document.getElementById('global-search-input');
  const dropdown = document.getElementById('global-search-dropdown');
  if (!searchInput || !dropdown) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    const q = e.target.value.trim();
    clearTimeout(debounceTimer);

    if (q.length < 2) {
      dropdown.classList.remove('show');
      dropdown.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        
        if (data.success) {
          renderSearchResults(data.results, dropdown);
        }
      } catch (err) {
        console.error('Search error:', err);
      }
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('show');
    }
  });
}

function renderSearchResults(results, container) {
  const hasScholarships = results.scholarships && results.scholarships.length > 0;
  const hasInternships = results.internships && results.internships.length > 0;
  const hasCourses = results.courses && results.courses.length > 0;

  if (!hasScholarships && !hasInternships && !hasCourses) {
    container.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">No matching opportunities found.</div>';
    container.classList.add('show');
    return;
  }

  let html = '';

  if (hasScholarships) {
    html += '<div class="search-result-group"><div class="search-result-heading">Scholarships</div>';
    results.scholarships.forEach(item => {
      html += `
        <a href="${item.url}" class="search-result-item">
          <div>
            <strong>${item.title}</strong>
            <div style="font-size: 0.75rem; color: var(--text-muted);">${item.subtitle}</div>
          </div>
          <span class="badge badge-primary">${item.badge}</span>
        </a>
      `;
    });
    html += '</div>';
  }

  if (hasInternships) {
    html += '<div class="search-result-group"><div class="search-result-heading">Internships</div>';
    results.internships.forEach(item => {
      html += `
        <a href="${item.url}" class="search-result-item">
          <div>
            <strong>${item.title}</strong>
            <div style="font-size: 0.75rem; color: var(--text-muted);">${item.subtitle}</div>
          </div>
          <span class="badge badge-success">${item.badge}</span>
        </a>
      `;
    });
    html += '</div>';
  }

  if (hasCourses) {
    html += '<div class="search-result-group"><div class="search-result-heading">Courses</div>';
    results.courses.forEach(item => {
      html += `
        <a href="${item.url}" class="search-result-item">
          <div>
            <strong>${item.title}</strong>
            <div style="font-size: 0.75rem; color: var(--text-muted);">${item.subtitle}</div>
          </div>
          <span class="badge badge-info">${item.badge}</span>
        </a>
      `;
    });
    html += '</div>';
  }

  container.innerHTML = html;
  container.classList.add('show');
}

/* --- UNIVERSAL SAVE / BOOKMARK BUTTONS --- */
function initSaveButtons() {
  document.addEventListener('click', async (e) => {
    const saveBtn = e.target.closest('.btn-save-opp');
    if (!saveBtn) return;

    e.preventDefault();
    const oppType = saveBtn.getAttribute('data-type');
    const oppId = saveBtn.getAttribute('data-id');
    const isSaved = saveBtn.getAttribute('data-saved') === 'true';

    try {
      if (isSaved) {
        // Remove
        const res = await fetch('/api/remove-saved', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opportunity_type: oppType, opportunity_id: oppId })
        });
        const data = await res.json();
        if (data.success) {
          saveBtn.setAttribute('data-saved', 'false');
          saveBtn.innerHTML = '<i class="far fa-bookmark"></i> Save';
          saveBtn.classList.remove('btn-primary');
          saveBtn.classList.add('btn-secondary');
          showToast('Bookmark Removed', `${oppType.capitalize()} removed from saved items.`, 'info');
        } else {
          showToast('Notice', data.message, 'warning');
        }
      } else {
        // Add
        const res = await fetch('/api/save-opportunity', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opportunity_type: oppType, opportunity_id: oppId })
        });
        const data = await res.json();
        if (data.success) {
          saveBtn.setAttribute('data-saved', 'true');
          saveBtn.innerHTML = '<i class="fas fa-bookmark"></i> Saved';
          saveBtn.classList.remove('btn-secondary');
          saveBtn.classList.add('btn-primary');
          showToast('Opportunity Saved!', `Saved to your bookmarks.`, 'success');
        } else {
          if (res.status === 401) {
            window.location.href = '/login';
          } else {
            showToast('Notice', data.message, 'warning');
          }
        }
      }
    } catch (err) {
      console.error('Save error:', err);
      showToast('Error', 'Unable to update bookmark right now.', 'danger');
    }
  });
}

/* --- TAB NAVIGATION HELPER --- */
function initTabNavs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const container = btn.closest('.tab-wrapper') || document;

      container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
}

String.prototype.capitalize = function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
};
