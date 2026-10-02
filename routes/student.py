"""
Student Portal Routes
Handles student dashboard, profile editing, skills, projects, certifications,
saved opportunities, notifications, and analytics.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, StudentProfile, Skill, Project, Certification, Scholarship, SavedOpportunity, Notification
from utils.auth_helpers import login_required
from services.auth_service import AuthService
from services.analytics_service import AnalyticsService
from services.career_service import CareerService
from services.recommendation_service import RecommendationService
from services.eligibility_service import EligibilityService
from services.application_service import ApplicationService
from services.notification_service import NotificationService

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    user = db.session.get(User, session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    profile = AuthService.get_or_create_profile(user)
    skills = profile.skills or []

    # Calculate Profile Strength
    profile_strength = AnalyticsService.calculate_profile_strength(profile, skills)

    # Calculate Career Readiness
    career_readiness = CareerService.calculate_career_readiness(profile, skills)

    # Get Unified Recommendations & Priority Action Center
    recommendations_data = RecommendationService.get_unified_recommendations(user.id)

    # Get Application Statistics
    app_analytics = ApplicationService.get_user_application_analytics(user.id)

    # Saved Count
    saved_count = SavedOpportunity.query.filter_by(user_id=user.id).count()

    # Eligible Scholarships Count
    all_scholarships = Scholarship.query.filter_by(is_active=True).all()
    eligible_count = sum(1 for s in all_scholarships if EligibilityService.calculate_scholarship_match(profile, s)['eligible'])

    # Deadlines
    upcoming_deadlines = RecommendationService.get_upcoming_deadlines()

    # Roadmap Progress
    roadmap_info = CareerService.get_roadmap_for_role(profile.preferred_role or profile.career_goal or "Full Stack Developer", user.id)

    return render_template(
        'student/dashboard.html',
        user=user,
        profile=profile,
        completion=profile_strength,
        career=career_readiness,
        app_stats=app_analytics,
        app_analytics=app_analytics,
        saved_count=saved_count,
        eligible_count=eligible_count,
        recommendations=recommendations_data,
        upcoming_deadlines=upcoming_deadlines,
        roadmap_percent=roadmap_info['progress_percent'],
        roadmap_info=roadmap_info
    )


@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    if request.method == 'POST':
        success, msg, _ = AuthService.update_profile(user, request.form)
        if success:
            flash(msg, 'success')
        else:
            flash(msg, 'danger')
        return redirect(url_for('student.profile'))

    skills = profile.skills or []
    projects = profile.projects or []
    certifications = profile.certifications or []
    profile_strength = AnalyticsService.calculate_profile_strength(profile, skills)

    return render_template(
        'student/profile.html',
        user=user,
        profile=profile,
        skills=skills,
        projects=projects,
        certifications=certifications,
        completion=profile_strength
    )


# --- SKILLS MANAGEMENT ---
@student_bp.route('/profile/skill/add', methods=['POST'])
@login_required
def add_skill():
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    name = request.form.get('name', '').strip()
    level = request.form.get('level', 'Intermediate').strip()
    category = request.form.get('category', 'Technical').strip()

    success, msg, _ = AuthService.add_or_update_skill(profile, name, level, category)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('student.profile'))


@student_bp.route('/profile/skill/delete/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    success, msg = AuthService.delete_skill(profile, skill_id)
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('student.profile'))


# --- PROJECTS MANAGEMENT ---
@student_bp.route('/profile/project/add', methods=['POST'])
@login_required
def add_project():
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    technologies = request.form.get('technologies', '').strip()
    github_link = request.form.get('github_link', '').strip()
    live_link = request.form.get('live_link', '').strip()

    success, msg, _ = AuthService.add_project(profile, title, description, technologies, github_link, live_link)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('student.profile'))


@student_bp.route('/profile/project/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    success, msg = AuthService.delete_project(profile, project_id)
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('student.profile'))


# --- CERTIFICATIONS MANAGEMENT ---
@student_bp.route('/profile/certification/add', methods=['POST'])
@login_required
def add_certification():
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    name = request.form.get('name', '').strip()
    issuer = request.form.get('issuer', '').strip()
    issue_date = request.form.get('issue_date', '').strip()
    credential_url = request.form.get('credential_url', '').strip()
    credential_id = request.form.get('credential_id', '').strip()

    success, msg, _ = AuthService.add_certification(profile, name, issuer, issue_date, credential_url, credential_id)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('student.profile'))


@student_bp.route('/profile/certification/delete/<int:cert_id>', methods=['POST'])
@login_required
def delete_certification(cert_id):
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    success, msg = AuthService.delete_certification(profile, cert_id)
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('student.profile'))


# --- SAVED OPPORTUNITIES ---
@student_bp.route('/saved')
@login_required
def saved():
    user = db.session.get(User, session['user_id'])
    saved_items = SavedOpportunity.query.filter_by(user_id=user.id).order_by(SavedOpportunity.created_at.desc()).all()

    scholarships = []
    internships = []
    courses = []

    for item in saved_items:
        opp = item.get_opportunity()
        if opp:
            if item.opportunity_type == 'scholarship':
                scholarships.append({'item_id': item.id, 'data': opp})
            elif item.opportunity_type == 'internship':
                internships.append({'item_id': item.id, 'data': opp})
            elif item.opportunity_type == 'course':
                courses.append({'item_id': item.id, 'data': opp})

    return render_template(
        'student/saved.html',
        user=user,
        scholarships=scholarships,
        internships=internships,
        courses=courses,
        total_saved=len(saved_items)
    )


# --- NOTIFICATIONS ---
@student_bp.route('/notifications')
@login_required
def notifications():
    user = db.session.get(User, session['user_id'])
    notifs = NotificationService.get_user_notifications(user.id)
    unread_count = NotificationService.get_unread_count(user.id)

    return render_template(
        'student/notifications.html',
        user=user,
        notifications=notifs,
        unread_count=unread_count
    )
