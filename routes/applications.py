"""
Application Tracker & Lifecycle Management Routes
Handles pipeline stage transitions, application logging, interview tracking, and notes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Application
from utils.auth_helpers import login_required
from services.application_service import ApplicationService, VALID_STATUSES

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/applications')
@login_required
def list_applications():
    user = db.session.get(User, session['user_id'])
    status_filter = request.args.get('status', 'All')

    query = Application.query.filter_by(user_id=user.id)
    if status_filter != 'All':
        query = query.filter_by(status=status_filter)

    apps = query.order_by(Application.created_at.desc()).all()
    analytics = ApplicationService.get_user_application_analytics(user.id)

    pipeline_stages = ['Saved', 'Applied', 'Under Review', 'Shortlisted', 'Interview', 'Accepted', 'Rejected']

    return render_template(
        'student/applications.html',
        user=user,
        applications=apps,
        status_counts=analytics['status_counts'],
        selected_status=status_filter,
        pipeline_stages=pipeline_stages,
        analytics=analytics
    )


@applications_bp.route('/applications/create', methods=['POST'])
@login_required
def create_application():
    user_id = session['user_id']
    opp_type = request.form.get('opportunity_type', 'scholarship')
    try:
        opp_id = int(request.form.get('opportunity_id', 0))
    except (ValueError, TypeError):
        opp_id = 0

    status = request.form.get('status', 'Applied')
    notes = request.form.get('notes', '')
    deadline = request.form.get('deadline', '')
    interview_date = request.form.get('interview_date', '')

    success, msg, _ = ApplicationService.create_or_update_application(
        user_id, opp_type, opp_id, status, notes, deadline, interview_date
    )
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('applications.list_applications'))


@applications_bp.route('/applications/update-status', methods=['POST'])
@login_required
def update_status():
    try:
        app_id = int(request.form.get('application_id', 0))
    except (ValueError, TypeError):
        app_id = 0

    new_status = request.form.get('status', 'Applied')
    notes = request.form.get('notes', '')

    success, msg, _ = ApplicationService.update_application_status(
        app_id, session['user_id'], new_status, notes
    )
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('applications.list_applications'))


@applications_bp.route('/applications/delete/<int:app_id>', methods=['POST'])
@login_required
def delete_application(app_id):
    success, msg = ApplicationService.delete_application(app_id, session['user_id'])
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('applications.list_applications'))
