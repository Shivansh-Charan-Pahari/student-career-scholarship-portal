/**
 * Applications Tracker JavaScript Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initApplicationStatusUpdater();
});

function initApplicationStatusUpdater() {
  const updateButtons = document.querySelectorAll('.btn-update-app-status');
  updateButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const appId = btn.getAttribute('data-id');
      const currentStatus = btn.getAttribute('data-status');
      const notes = btn.getAttribute('data-notes') || '';

      document.getElementById('modalAppId').value = appId;
      document.getElementById('modalAppStatus').value = currentStatus;
      document.getElementById('modalAppNotes').value = notes;

      openModal('updateStatusModal');
    });
  });
}
