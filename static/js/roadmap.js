/**
 * Interactive Career Roadmap JavaScript
 * Allows students to check off stages and saves progress to database asynchronously
 */

document.addEventListener('DOMContentLoaded', () => {
  initRoadmapCheckboxes();
});

function initRoadmapCheckboxes() {
  const checkboxes = document.querySelectorAll('.roadmap-checkbox');
  
  checkboxes.forEach(cb => {
    cb.addEventListener('change', async (e) => {
      const stageId = e.target.getAttribute('data-stage-id');
      const careerRole = e.target.getAttribute('data-career-role') || 'Full Stack Developer';
      const isChecked = e.target.checked;
      const nodeElement = document.getElementById(`stage-node-${stageId}`);

      try {
        const res = await fetch('/api/roadmap-progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            stage_id: stageId,
            career_role: careerRole,
            completed: isChecked
          })
        });

        const json = await res.json();
        if (json.success) {
          const data = json.data || json;
          // Update visual node style
          if (nodeElement) {
            if (isChecked) {
              nodeElement.classList.add('completed');
            } else {
              nodeElement.classList.remove('completed');
            }
          }

          // Update Progress Bar and Text
          const progressBar = document.getElementById('roadmapProgressBar');
          const progressPercentText = document.getElementById('roadmapProgressPercent');
          const completedCountText = document.getElementById('roadmapCompletedCount');

          if (progressBar && data.progress_percent !== undefined) {
            progressBar.style.width = `${data.progress_percent}%`;
          }
          if (progressPercentText && data.progress_percent !== undefined) {
            progressPercentText.textContent = `${data.progress_percent}%`;
          }
          if (completedCountText && data.completed_count !== undefined) {
            completedCountText.textContent = data.completed_count;
          }

          showToast(
            isChecked ? 'Milestone Completed!' : 'Milestone Updated',
            `Stage ${stageId} progress saved to database.`,
            isChecked ? 'success' : 'info'
          );
        } else {
          e.target.checked = !isChecked; // Revert
          showToast('Error', json.error?.message || json.message || 'Failed to update stage progress', 'danger');
        }
      } catch (err) {
        console.error('Roadmap update error:', err);
        e.target.checked = !isChecked;
        showToast('Error', 'Unable to reach server.', 'danger');
      }
    });
  });
}
