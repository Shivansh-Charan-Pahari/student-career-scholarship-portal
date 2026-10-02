"""
Internships Catalog & Opportunity Discovery Routes
Handles search, domain, work mode, and location filtering with match metrics.
"""

from flask import Blueprint, render_template, request, session
from models import db, User, Internship, SavedOpportunity, Application

internships_bp = Blueprint('internships', __name__)

@internships_bp.route('/internships')
def list_internships():
    user = None
    saved_ids = set()
    applied_ids = set()

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            saved_items = SavedOpportunity.query.filter_by(user_id=user.id, opportunity_type='internship').all()
            saved_ids = {s.opportunity_id for s in saved_items}
            applied_items = Application.query.filter_by(user_id=user.id, opportunity_type='internship').all()
            applied_ids = {a.opportunity_id for a in applied_items}

    # Query Filters
    search = request.args.get('search', '').strip()
    domain = request.args.get('domain', '').strip()
    work_mode = request.args.get('work_mode', '').strip()
    location = request.args.get('location', '').strip()

    query = Internship.query.filter_by(is_active=True)

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Internship.title.ilike(search_fmt)) |
            (Internship.company.ilike(search_fmt)) |
            (Internship.description.ilike(search_fmt)) |
            (Internship.required_skills.ilike(search_fmt)) |
            (Internship.location.ilike(search_fmt))
        )

    if domain and domain != 'All':
        query = query.filter(Internship.domain.ilike(f"%{domain}%"))

    if work_mode and work_mode != 'All':
        query = query.filter(Internship.work_mode.ilike(f"%{work_mode}%"))

    if location and location != 'All':
        query = query.filter(Internship.location.ilike(f"%{location}%"))

    internships_list = query.order_by(Internship.id.desc()).all()

    all_domains = [
        'All', 'Web Development', 'Software Development', 'Python', 'Data Science',
        'AI/ML', 'Cybersecurity', 'Cloud Computing', 'Mobile Development', 'UI/UX Design', 'Embedded Systems'
    ]
    all_work_modes = ['All', 'Remote', 'Hybrid', 'On-site']

    return render_template(
        'student/internships.html',
        internships=internships_list,
        user=user,
        saved_ids=saved_ids,
        applied_ids=applied_ids,
        search=search,
        selected_domain=domain,
        selected_work_mode=work_mode,
        all_domains=all_domains,
        all_work_modes=all_work_modes,
        total_count=len(internships_list)
    )


@internships_bp.route('/internship/<int:internship_id>')
def internship_detail(internship_id):
    internship = db.session.get(Internship, internship_id)
    if not internship:
        from flask import abort
        abort(404)

    user = None
    is_saved = False
    is_applied = False

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            is_saved = SavedOpportunity.query.filter_by(
                user_id=user.id, opportunity_type='internship', opportunity_id=internship.id
            ).first() is not None
            is_applied = Application.query.filter_by(
                user_id=user.id, opportunity_type='internship', opportunity_id=internship.id
            ).first() is not None

    return render_template(
        'student/internship_detail.html',
        internship=internship,
        user=user,
        is_saved=is_saved,
        is_applied=is_applied
    )
