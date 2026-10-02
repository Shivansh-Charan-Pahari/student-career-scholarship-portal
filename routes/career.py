"""
Career Intelligence & Dynamic Roadmap Routes
Handles multi-role simulations, skill gap analysis, and tailored milestone roadmaps.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from utils.auth_helpers import login_required
from services.auth_service import AuthService
from services.career_service import CareerService, ROADMAP_DEFINITIONS
from services.recommendation_service import RecommendationService

career_bp = Blueprint('career', __name__)

@career_bp.route('/career')
@login_required
def career_view():
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)
    skills = profile.skills or []

    selected_role = request.args.get('role')
    if selected_role:
        # Transient profile copy for interactive role simulation
        sim_profile = type('ProfileSim', (), {
            'preferred_role': selected_role,
            'career_goal': selected_role,
            'cgpa': profile.cgpa,
            'skills': skills,
            'projects': profile.projects,
            'certifications': profile.certifications,
            'resume_url': profile.resume_url,
            'github_url': profile.github_url,
            'linkedin_url': profile.linkedin_url,
            'bio': profile.bio,
            'headline': profile.headline
        })()
        career_data = CareerService.calculate_career_readiness(sim_profile, skills)
    else:
        career_data = CareerService.calculate_career_readiness(profile, skills)

    recommendations = RecommendationService.get_unified_recommendations(user.id)

    return render_template(
        'student/career.html',
        user=user,
        profile=profile,
        skills=skills,
        career=career_data,
        recommendations=recommendations,
        selected_role=selected_role or career_data['target_role']
    )


@career_bp.route('/roadmap')
@login_required
def roadmap_view():
    user = db.session.get(User, session['user_id'])
    profile = AuthService.get_or_create_profile(user)

    selected_role = request.args.get('role') or profile.preferred_role or profile.career_goal or "Full Stack Developer"
    roadmap_data = CareerService.get_roadmap_for_role(selected_role, user.id)

    return render_template(
        'student/roadmap.html',
        user=user,
        profile=profile,
        stages=roadmap_data['stages'],
        completed_count=roadmap_data['completed_count'],
        total_stages=roadmap_data['total_stages'],
        progress_percent=roadmap_data['progress_percent'],
        selected_role=roadmap_data['role'],
        all_roles=roadmap_data['all_available_roles']
    )


@career_bp.route('/roadmap/toggle', methods=['POST'])
@login_required
def toggle_roadmap_item():
    stage_id = request.form.get('stage_id')
    career_role = request.form.get('career_role', 'Full Stack Developer')
    user_id = session['user_id']

    if not stage_id:
        return redirect(url_for('career.roadmap_view', role=career_role))

    result = CareerService.toggle_stage_progress(user_id, stage_id, career_role)
    status_str = "completed" if result['completed'] else "marked pending"
    flash(f"Stage {stage_id} {status_str} (Progress: {result['progress_percent']}%)", "success")
    return redirect(url_for('career.roadmap_view', role=career_role))
