/**
 * Career & Skill Gap Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const roleSelect = document.getElementById('targetRoleSelect');
  if (roleSelect) {
    roleSelect.addEventListener('change', (e) => {
      const selectedRole = e.target.value;
      window.location.href = `/career?role=${encodeURIComponent(selectedRole)}`;
    });
  }
});
