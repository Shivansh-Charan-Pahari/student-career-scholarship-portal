"""
REST API Controller Layer
Provides uniform JSON REST endpoints with structured response payloads,
error codes, and validation.
"""

from flask import Blueprint, request, jsonify, session
from models import db, User, Scholarship, Internship, Course, Application, SavedOpportunity, Notification
from services.eligibility_service import EligibilityService
from services.career_service import CareerService
from services.recommendation_service import RecommendationService
from services.application_service import ApplicationService
from services.notification_service import NotificationService
from services.analytics_service import AnalyticsService

api_bp = Blueprint('api', __name__, url_prefix='/api')

def api_success(data=None, message="Operation completed successfully", status_code=200):
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def api_error(code="ERROR", message="An error occurred", status_code=400):
    return jsonify({
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }), status_code


# --- SCHOLARSHIPS API ---
@api_bp.route('/scholarships', methods=['GET'])
def api_scholarships():
    items = Scholarship.query.filter_by(is_active=True).all()
    return api_success(data=[item.to_dict() for item in items], message="Scholarships fetched successfully")


@api_bp.route('/scholarships/<int:id>', methods=['GET'])
def api_scholarship_detail(id):
    sch = db.session.get(Scholarship, id)
    if not sch:
        return api_error(code="NOT_FOUND", message=f"Scholarship #{id} not found", status_code=404)
    return api_success(data=sch.to_dict())


# --- INTERNSHIPS API ---
@api_bp.route('/internships', methods=['GET'])
def api_internships():
    items = Internship.query.filter_by(is_active=True).all()
    return api_success(data=[item.to_dict() for item in items], message="Internships fetched successfully")


@api_bp.route('/internships/<int:id>', methods=['GET'])
def api_internship_detail(id):
    intern = db.session.get(Internship, id)
    if not intern:
        return api_error(code="NOT_FOUND", message=f"Internship #{id} not found", status_code=404)
    return api_success(data=intern.to_dict())


# --- COURSES API ---
@api_bp.route('/courses', methods=['GET'])
def api_courses():
    items = Course.query.filter_by(is_active=True).all()
    return api_success(data=[item.to_dict() for item in items], message="Courses fetched successfully")


@api_bp.route('/courses/<int:id>', methods=['GET'])
def api_course_detail(id):
    course = db.session.get(Course, id)
    if not course:
        return api_error(code="NOT_FOUND", message=f"Course #{id} not found", status_code=404)
    return api_success(data=course.to_dict())


# --- RECOMMENDATIONS & DASHBOARD API ---
@api_bp.route('/recommendations', methods=['GET'])
def api_recommendations():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    recs = RecommendationService.get_unified_recommendations(session['user_id'])
    return api_success(data={
        'scholarships': [{
            'id': r['scholarship'].id,
            'name': r['scholarship'].name,
            'provider': r['scholarship'].provider,
            'amount': r['scholarship'].amount,
            'match_score': r['match_score'],
            'eligible': r['eligible'],
            'reasons': r['reasons'],
            'explanation': r['explanation']
        } for r in recs['scholarships']],
        'internships': [{
            'id': r['internship'].id,
            'title': r['internship'].title,
            'company': r['internship'].company,
            'stipend': r['internship'].stipend,
            'score': r['score'],
            'matched_skills': r['matched_skills'],
            'match_explanation': r['match_explanation']
        } for r in recs['internships']],
        'courses': [{
            'id': r['course'].id,
            'name': r['course'].name,
            'platform': r['course'].platform,
            'price': r['course'].price,
            'rating': r['course'].rating,
            'is_gap_remedy': r['is_gap_remedy'],
            'reason': r['reason']
        } for r in recs['courses']],
        'priorities': recs['priorities']
    })


@api_bp.route('/dashboard', methods=['GET'])
def api_dashboard_summary():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    user = db.session.get(User, session['user_id'])
    profile = user.profile
    skills = profile.skills or [] if profile else []

    strength = AnalyticsService.calculate_profile_strength(profile, skills)
    readiness = CareerService.calculate_career_readiness(profile, skills)
    app_stats = ApplicationService.get_user_application_analytics(user.id)
    saved_count = SavedOpportunity.query.filter_by(user_id=user.id).count()

    return api_success(data={
        'user': user.to_dict(),
        'profile_strength': strength,
        'career_readiness': readiness,
        'application_analytics': app_stats,
        'saved_count': saved_count
    })


# --- ELIGIBILITY CHECK API ---
@api_bp.route('/check-eligibility', methods=['POST'])
def api_check_eligibility():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Please log in to check scholarship eligibility", status_code=401)

    data = request.get_json() or {}
    scholarship_id = data.get('scholarship_id')
    if not scholarship_id:
        return api_error(code="VALIDATION_ERROR", message="Scholarship ID is required", status_code=400)

    scholarship = db.session.get(Scholarship, scholarship_id)
    if not scholarship:
        return api_error(code="NOT_FOUND", message="Scholarship record not found", status_code=404)

    user = db.session.get(User, session['user_id'])
    result = EligibilityService.calculate_scholarship_match(user.profile, scholarship)

    return api_success(data={
        'scholarship': scholarship.to_dict(),
        'result': result
    }, message="Eligibility calculation completed")


# --- SAVED OPPORTUNITIES (BOOKMARKS) API ---
@api_bp.route('/save-opportunity', methods=['POST'])
def api_save_opportunity():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Please log in to save opportunities", status_code=401)

    data = request.get_json() or {}
    opp_type = data.get('opportunity_type')
    opp_id = data.get('opportunity_id')

    if not opp_type or not opp_id:
        return api_error(code="VALIDATION_ERROR", message="Opportunity type and ID are required", status_code=400)

    success, msg = ApplicationService.save_opportunity(session['user_id'], opp_type, int(opp_id))
    return api_success(data={'saved': True}, message=msg)


@api_bp.route('/remove-saved', methods=['POST'])
def api_remove_saved():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    data = request.get_json() or {}
    opp_type = data.get('opportunity_type', '')
    opp_id = data.get('opportunity_id', 0)
    item_id = data.get('item_id')

    success, msg = ApplicationService.remove_saved_opportunity(
        session['user_id'], opp_type=opp_type, opp_id=int(opp_id or 0), item_id=item_id
    )
    if not success:
        return api_error(code="NOT_FOUND", message=msg, status_code=404)

    return api_success(data={'saved': False}, message=msg)


# --- APPLICATION LIFECYCLE API ---
@api_bp.route('/applications', methods=['POST'])
def api_create_application():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    data = request.get_json() or {}
    opp_type = data.get('opportunity_type')
    opp_id = data.get('opportunity_id')
    status = data.get('status', 'Applied')
    notes = data.get('notes', '')
    deadline = data.get('deadline', '')
    interview_date = data.get('interview_date', '')

    if not opp_type or not opp_id:
        return api_error(code="VALIDATION_ERROR", message="Opportunity type and ID are required", status_code=400)

    success, msg, app_rec = ApplicationService.create_or_update_application(
        session['user_id'], opp_type, int(opp_id), status, notes, deadline, interview_date
    )
    return api_success(data=app_rec.to_dict() if app_rec else None, message=msg, status_code=201 if success else 400)


@api_bp.route('/update-application-status', methods=['POST'])
def api_update_application_status():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    data = request.get_json() or {}
    app_id = data.get('application_id')
    new_status = data.get('status')
    notes = data.get('notes', '')

    if not app_id or not new_status:
        return api_error(code="VALIDATION_ERROR", message="Application ID and status are required", status_code=400)

    success, msg, app_rec = ApplicationService.update_application_status(
        int(app_id), session['user_id'], new_status, notes
    )
    if not success:
        return api_error(code="NOT_FOUND", message=msg, status_code=404)

    return api_success(data=app_rec.to_dict(), message=msg)


# --- ROADMAP PROGRESS API ---
@api_bp.route('/roadmap-progress', methods=['POST'])
def api_roadmap_progress():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    data = request.get_json() or {}
    stage_id = data.get('stage_id')
    career_role = data.get('career_role', 'Full Stack Developer')
    completed = data.get('completed')

    if not stage_id:
        return api_error(code="VALIDATION_ERROR", message="Stage ID is required", status_code=400)

    result = CareerService.toggle_stage_progress(session['user_id'], str(stage_id), career_role, completed)
    return api_success(data=result, message=f"Stage {stage_id} status updated")


# --- NOTIFICATIONS API ---
@api_bp.route('/notifications', methods=['GET'])
def api_notifications():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    notifs = NotificationService.get_user_notifications(session['user_id'])
    unread = NotificationService.get_unread_count(session['user_id'])
    return api_success(data={
        'unread_count': unread,
        'notifications': [n.to_dict() for n in notifs]
    })


@api_bp.route('/notifications/mark-read', methods=['POST'])
def api_mark_notifications_read():
    if 'user_id' not in session:
        return api_error(code="UNAUTHORIZED", message="Authentication required", status_code=401)

    data = request.get_json() or {}
    notif_id = data.get('notification_id')

    NotificationService.mark_as_read(session['user_id'], notif_id)
    return api_success(message="Notifications marked as read")


# --- GLOBAL SEARCH API ---
@api_bp.route('/search', methods=['GET'])
def api_global_search():
    query = request.args.get('q', '').strip()
    if not query:
        return api_success(data={'scholarships': [], 'internships': [], 'courses': []})

    fmt = f"%{query}%"
    schs = Scholarship.query.filter_by(is_active=True).filter((Scholarship.name.ilike(fmt)) | (Scholarship.provider.ilike(fmt)) | (Scholarship.description.ilike(fmt))).limit(5).all()
    interns = Internship.query.filter_by(is_active=True).filter((Internship.title.ilike(fmt)) | (Internship.company.ilike(fmt)) | (Internship.required_skills.ilike(fmt))).limit(5).all()
    courses = Course.query.filter_by(is_active=True).filter((Course.name.ilike(fmt)) | (Course.skill.ilike(fmt)) | (Course.platform.ilike(fmt))).limit(5).all()

    return api_success(data={
        'query': query,
        'results': {
            'scholarships': [{'id': s.id, 'title': s.name, 'subtitle': s.provider, 'badge': s.amount, 'url': f'/scholarship/{s.id}'} for s in schs],
            'internships': [{'id': i.id, 'title': i.title, 'subtitle': i.company, 'badge': i.stipend, 'url': f'/internship/{i.id}'} for i in interns],
            'courses': [{'id': c.id, 'title': c.name, 'subtitle': c.platform, 'badge': c.price, 'url': '/courses'} for c in courses]
        }
    })
