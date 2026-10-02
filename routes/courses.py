"""
Courses & Skill-Building Catalog Routes
Handles courses directory, platform filters, proficiency level filters, and price selectors.
"""

from flask import Blueprint, render_template, request, session
from models import db, User, Course, SavedOpportunity

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses')
def list_courses():
    user = None
    saved_ids = set()

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            saved_items = SavedOpportunity.query.filter_by(user_id=user.id, opportunity_type='course').all()
            saved_ids = {s.opportunity_id for s in saved_items}

    search = request.args.get('search', '').strip()
    level = request.args.get('level', '').strip()
    platform = request.args.get('platform', '').strip()
    price_type = request.args.get('price', '').strip()

    query = Course.query.filter_by(is_active=True)

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Course.name.ilike(search_fmt)) |
            (Course.platform.ilike(search_fmt)) |
            (Course.skill.ilike(search_fmt)) |
            (Course.description.ilike(search_fmt))
        )

    if level and level != 'All':
        query = query.filter(Course.level.ilike(f"%{level}%"))

    if platform and platform != 'All':
        query = query.filter(Course.platform.ilike(f"%{platform}%"))

    if price_type == 'Free':
        query = query.filter(Course.price.ilike('%Free%'))
    elif price_type == 'Paid':
        query = query.filter(~Course.price.ilike('%Free%'))

    courses_list = query.order_by(Course.rating.desc(), Course.id.desc()).all()

    all_levels = ['All', 'Beginner', 'Intermediate', 'Advanced']
    all_platforms = ['All', 'Coursera', 'edX', 'Udemy', 'NPTEL', 'FreeCodeCamp', 'YouTube/Harvard CS50']

    return render_template(
        'student/courses.html',
        courses=courses_list,
        user=user,
        saved_ids=saved_ids,
        search=search,
        selected_level=level,
        selected_platform=platform,
        selected_price=price_type,
        all_levels=all_levels,
        all_platforms=all_platforms,
        total_count=len(courses_list)
    )
