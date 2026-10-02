/**
 * Scholarships Client Script:
 * - Live Eligibility Engine Modal Trigger via AJAX
 * - Comprehensive Match Score & Criteria Breakdown Display
 */

document.addEventListener('DOMContentLoaded', () => {
  initEligibilityModalTrigger();
});

function initEligibilityModalTrigger() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.btn-check-eligibility');
    if (!btn) return;

    e.preventDefault();
    const schId = btn.getAttribute('data-id');
    const modal = document.getElementById('eligibilityModal');
    if (!modal) return;

    // Show loading state in modal
    const modalContent = document.getElementById('eligibilityModalContent');
    modalContent.innerHTML = `
      <div style="text-align: center; padding: 2.5rem;">
        <i class="fas fa-spinner fa-spin fa-2x" style="color: var(--primary-600); margin-bottom: 1rem;"></i>
        <p style="font-weight: 600; color: var(--text-main);">Evaluating your academic profile against eligibility criteria...</p>
      </div>
    `;
    openModal('eligibilityModal');

    try {
      const res = await fetch('/api/check-eligibility', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scholarship_id: schId })
      });

      const data = await res.json();
      if (!data.success) {
        modalContent.innerHTML = `
          <div style="text-align: center; padding: 2rem;">
            <i class="fas fa-exclamation-triangle fa-2x" style="color: var(--accent-amber); margin-bottom: 1rem;"></i>
            <p style="font-weight: 600;">${data.message}</p>
            ${res.status === 401 ? '<a href="/login" class="btn btn-primary" style="margin-top: 1rem;">Log In to Check</a>' : ''}
          </div>
        `;
        return;
      }

      renderEligibilityResult(data.scholarship, data.result, modalContent);

    } catch (err) {
      console.error('Eligibility fetch error:', err);
      modalContent.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
          <i class="fas fa-times-circle fa-2x" style="color: var(--accent-rose); margin-bottom: 1rem;"></i>
          <p>Unable to verify eligibility at this moment. Please try again.</p>
        </div>
      `;
    }
  });
}

function renderEligibilityResult(scholarship, result, container) {
  const isEligible = result.eligible;
  const score = result.score;
  const scoreColorClass = score >= 80 ? 'score-high' : (score >= 60 ? 'score-medium' : 'score-low');
  
  let reasonsHtml = result.reasons.map(r => {
    const isSuccess = r.startsWith('CGPA Requirement Met') || r.startsWith('Income Limit Met') || r.startsWith('Branch Eligible') || r.startsWith('Category Eligible') || r.startsWith('Open to') || r.startsWith('No ');
    const iconClass = isSuccess ? 'fa-check-circle' : 'fa-times-circle';
    const colorStyle = isSuccess ? 'color: var(--accent-emerald);' : 'color: var(--accent-rose);';
    return `
      <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 1px solid var(--border-subtle); font-size: 0.9rem;">
        <i class="fas ${iconClass}" style="${colorStyle} font-size: 1.1rem; margin-top: 2px;"></i>
        <span>${r}</span>
      </div>
    `;
  }).join('');

  let missingHtml = '';
  if (result.missing_requirements && result.missing_requirements.length > 0) {
    missingHtml = `
      <div style="margin-top: 1.25rem; background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: var(--radius-md); padding: 1rem;">
        <div style="font-weight: 700; color: var(--accent-rose); font-size: 0.875rem; margin-bottom: 0.5rem;">
          <i class="fas fa-exclamation-circle"></i> Unmet Criteria
        </div>
        <ul style="padding-left: 1.25rem; font-size: 0.85rem; color: var(--text-main); list-style: disc;">
          ${result.missing_requirements.map(m => `<li>${m}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  container.innerHTML = `
    <div>
      <div style="text-align: center; margin-bottom: 1.5rem;">
        <div class="empty-state-icon" style="background-color: ${isEligible ? '#d1fae5' : '#ffe4e6'}; color: ${isEligible ? '#059669' : '#e11d48'};">
          <i class="fas ${isEligible ? 'fa-check-circle' : 'fa-info-circle'}"></i>
        </div>
        <h3 style="font-size: 1.4rem; margin-bottom: 0.35rem;">
          ${isEligible ? 'You Are Eligible!' : 'Eligibility Status: Requirements Incomplete'}
        </h3>
        <p style="font-size: 0.9rem; color: var(--text-muted);">${scholarship.name} (${scholarship.provider})</p>
      </div>

      <!-- Match Score Progress -->
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <span style="font-weight: 700; font-size: 0.95rem;">Recommendation Match Score</span>
          <span class="match-score-pill ${scoreColorClass}" style="font-size: 0.9rem;">${score}% Match</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill ${score >= 80 ? 'success' : ''}" style="width: ${score}%;"></div>
        </div>
        <p style="font-size: 0.775rem; color: var(--text-dim); margin-top: 0.35rem;">
          Calculated based on your CGPA (35%), Family Income (25%), Academic Branch (20%), Category (10%), and Past Academic Board Records (10%).
        </p>
      </div>

      <!-- Criteria Breakdown -->
      <h4 style="font-size: 1rem; margin-bottom: 0.75rem; color: var(--text-main);">
        <i class="fas fa-list-check" style="color: var(--primary-500); margin-right: 0.4rem;"></i>
        Detailed Criteria Evaluation
      </h4>
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 0.5rem 1rem;">
        ${reasonsHtml}
      </div>

      ${missingHtml}

      <!-- Action Buttons -->
      <div style="display: flex; gap: 0.75rem; margin-top: 1.5rem; justify-content: flex-end;">
        <a href="/scholarship/${scholarship.id}" class="btn btn-secondary btn-sm">View Full Details</a>
        <form action="/applications/create" method="POST" style="display: inline;">
          <input type="hidden" name="opportunity_type" value="scholarship">
          <input type="hidden" name="opportunity_id" value="${scholarship.id}">
          <input type="hidden" name="status" value="Applied">
          <button type="submit" class="btn btn-primary btn-sm">
            <i class="fas fa-paper-plane"></i> Track Application
          </button>
        </form>
      </div>
    </div>
  `;
}
