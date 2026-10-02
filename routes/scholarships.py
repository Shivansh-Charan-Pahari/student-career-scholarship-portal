"""
Scholarships Discovery & Decision Support Routes
Handles catalog search, multi-criteria filtering, backend pagination,
and detailed explainable eligibility breakdowns.
"""

from flask import Blueprint, render_template, request, session
from models import db, User, Scholarship, SavedOpportunity, Application
from services.eligibility_service import EligibilityService

scholarships_bp = Blueprint('scholarships', __name__)

@scholarships_bp.route('/scholarships')
def list_scholarships():
    user = None
    profile = None
    saved_ids = set()

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            profile = user.profile
            saved_items = SavedOpportunity.query.filter_by(user_id=user.id, opportunity_type='scholarship').all()
            saved_ids = {s.opportunity_id for s in saved_items}

    # Query Parameters
    search = request.args.get('search', '').strip()
    branch = request.args.get('branch', '').strip()
    category = request.args.get('category', '').strip()
    max_income = request.args.get('max_income', '').strip()
    min_cgpa = request.args.get('min_cgpa', '').strip()
    sort_by = request.args.get('sort', 'newest')

    query = Scholarship.query.filter_by(is_active=True)

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Scholarship.name.ilike(search_fmt)) |
            (Scholarship.provider.ilike(search_fmt)) |
            (Scholarship.description.ilike(search_fmt)) |
            (Scholarship.eligible_branches.ilike(search_fmt))
        )

    if branch and branch != 'All':
        query = query.filter(
            (Scholarship.eligible_branches.ilike(f"%{branch}%")) |
            (Scholarship.eligible_branches.ilike("%All%"))
        )

    if category and category != 'All':
        query = query.filter(
            (Scholarship.eligible_categories.ilike(f"%{category}%")) |
            (Scholarship.eligible_categories.ilike("%All%"))
        )

    if max_income:
        try:
            inc_val = float(max_income)
            query = query.filter((Scholarship.maximum_income <= inc_val) | (Scholarship.maximum_income == 0))
        except (ValueError, TypeError):
            pass

    if min_cgpa:
        try:
            cgpa_val = float(min_cgpa)
            query = query.filter(Scholarship.minimum_cgpa <= cgpa_val)
        except (ValueError, TypeError):
            pass

    scholarships_raw = query.all()

    # Calculate match score & explainability for logged-in students
    scholarships_data = []
    for s in scholarships_raw:
        is_saved = s.id in saved_ids
        if profile:
            el_res = EligibilityService.calculate_scholarship_match(profile, s)
            scholarships_data.append({
                'item': s,
                'match_score': el_res['score'],
                'eligible': el_res['eligible'],
                'reasons': el_res['reasons'],
                'missing_requirements': el_res['missing_requirements'],
                'breakdown': el_res['breakdown'],
                'explanation': el_res['explanation_summary'],
                'is_saved': is_saved
            })
        else:
            scholarships_data.append({
                'item': s,
                'match_score': None,
                'eligible': None,
                'reasons': [],
                'missing_requirements': [],
                'breakdown': {},
                'explanation': '',
                'is_saved': is_saved
            })

    # Sorting
    if sort_by == 'match_score' and profile:
        scholarships_data.sort(key=lambda x: (x['eligible'], x['match_score'] or 0), reverse=True)
    elif sort_by == 'amount':
        scholarships_data.sort(key=lambda x: x['item'].amount_numeric or 0, reverse=True)
    elif sort_by == 'deadline':
        scholarships_data.sort(key=lambda x: x['item'].deadline or '9999-99-99')
    else: # newest
        scholarships_data.sort(key=lambda x: x['item'].id, reverse=True)

    all_categories = ['All', 'General', 'OBC', 'SC', 'ST', 'EWS']
    all_branches = ['All', 'Computer Science', 'Information Technology', 'Electronics & Comm (ECE)', 'Electrical (EEE)', 'Mechanical', 'Civil', 'Data Science', 'AI & ML']

    return render_template(
        'student/scholarships.html',
        scholarships=scholarships_data,
        user=user,
        profile=profile,
        search=search,
        selected_branch=branch,
        selected_category=category,
        sort_by=sort_by,
        all_categories=all_categories,
        all_branches=all_branches,
        total_count=len(scholarships_data)
    )


@scholarships_bp.route('/scholarship/<int:scholarship_id>')
def scholarship_detail(scholarship_id):
    scholarship = db.session.get(Scholarship, scholarship_id)
    if not scholarship:
        from flask import abort
        abort(404)

    user = None
    profile = None
    eligibility = None
    is_saved = False
    is_applied = False

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            profile = user.profile
            eligibility = EligibilityService.calculate_scholarship_match(profile, scholarship)
            is_saved = SavedOpportunity.query.filter_by(
                user_id=user.id, opportunity_type='scholarship', opportunity_id=scholarship.id
            ).first() is not None
            is_applied = Application.query.filter_by(
                user_id=user.id, opportunity_type='scholarship', opportunity_id=scholarship.id
            ).first() is not None

    return render_template(
        'student/scholarship_detail.html',
        scholarship=scholarship,
        user=user,
        profile=profile,
        eligibility=eligibility,
        is_saved=is_saved,
        is_applied=is_applied
    )
