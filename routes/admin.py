"""
Administrator Console & Governance Routes
Provides management capabilities for opportunities, students, application workflows,
and immutable audit log inspection.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, StudentProfile, Application, Scholarship, Internship, Course, AdminActionLog
from utils.auth_helpers import admin_required
from services.admin_service import AdminService
from services.analytics_service import AnalyticsService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_bp.route('/admin/')
@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    metrics = AnalyticsService.get_admin_dashboard_metrics()
    return render_template(
        'admin/dashboard.html',
        stats=metrics['kpis'],
        app_status_counts=metrics['status_counts'],
        domain_counts=metrics['domain_counts'],
        platform_counts=metrics['platform_counts'],
        cat_counts=metrics['cat_counts'],
        top_skills=metrics['top_skills'],
        recent_applications=metrics['recent_applications']
    )


# --- STUDENTS DIRECTORY ---
@admin_bp.route('/admin/students')
@admin_required
def students_list():
    search = request.args.get('search', '').strip()
    query = User.query.filter_by(role='student')

    if search:
        search_fmt = f"%{search}%"
        query = query.filter((User.name.ilike(search_fmt)) | (User.email.ilike(search_fmt)))

    students = query.order_by(User.created_at.desc()).all()
    return render_template('admin/students.html', students=students, search=search)


@admin_bp.route('/admin/student/<int:student_id>')
@admin_required
def student_detail(student_id):
    student = User.query.get_or_404(student_id)
    profile = student.profile
    apps = Application.query.filter_by(user_id=student.id).all()
    return render_template('admin/student_detail.html', student=student, profile=profile, applications=apps)


# --- SCHOLARSHIPS CRUD ---
@admin_bp.route('/admin/scholarships', methods=['GET', 'POST'])
@admin_required
def scholarships_crud():
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    if request.method == 'POST':
        success, msg, _ = AdminService.create_scholarship(admin, request.form, ip)
        flash(msg, 'success' if success else 'danger')
        return redirect(url_for('admin.scholarships_crud'))

    search = request.args.get('search', '').strip()
    query = Scholarship.query
    if search:
        search_fmt = f"%{search}%"
        query = query.filter((Scholarship.name.ilike(search_fmt)) | (Scholarship.provider.ilike(search_fmt)))

    scholarships = query.order_by(Scholarship.id.desc()).all()
    return render_template('admin/scholarships.html', scholarships=scholarships, search=search)


@admin_bp.route('/admin/scholarship/edit/<int:id>', methods=['POST'])
@admin_required
def edit_scholarship(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    success, msg, _ = AdminService.update_scholarship(admin, id, request.form, ip)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('admin.scholarships_crud'))


@admin_bp.route('/admin/scholarship/delete/<int:id>', methods=['POST'])
@admin_required
def delete_scholarship(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    success, msg = AdminService.delete_scholarship(admin, id, ip)
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('admin.scholarships_crud'))


# --- INTERNSHIPS CRUD ---
@admin_bp.route('/admin/internships', methods=['GET', 'POST'])
@admin_required
def internships_crud():
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    if request.method == 'POST':
        success, msg, _ = AdminService.create_internship(admin, request.form, ip)
        flash(msg, 'success' if success else 'danger')
        return redirect(url_for('admin.internships_crud'))

    search = request.args.get('search', '').strip()
    query = Internship.query
    if search:
        search_fmt = f"%{search}%"
        query = query.filter((Internship.title.ilike(search_fmt)) | (Internship.company.ilike(search_fmt)))

    internships = query.order_by(Internship.id.desc()).all()
    return render_template('admin/internships.html', internships=internships, search=search)


@admin_bp.route('/admin/internship/edit/<int:id>', methods=['POST'])
@admin_required
def edit_internship(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    success, msg, _ = AdminService.update_internship(admin, id, request.form, ip)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('admin.internships_crud'))


@admin_bp.route('/admin/internship/delete/<int:id>', methods=['POST'])
@admin_required
def delete_internship(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    success, msg = AdminService.delete_internship(admin, id, ip)
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('admin.internships_crud'))


# --- COURSES CRUD ---
@admin_bp.route('/admin/courses', methods=['GET', 'POST'])
@admin_required
def courses_crud():
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    if request.method == 'POST':
        success, msg, _ = AdminService.create_course(admin, request.form, ip)
        flash(msg, 'success' if success else 'danger')
        return redirect(url_for('admin.courses_crud'))

    search = request.args.get('search', '').strip()
    query = Course.query
    if search:
        search_fmt = f"%{search}%"
        query = query.filter((Course.name.ilike(search_fmt)) | (Course.skill.ilike(search_fmt)))

    courses = query.order_by(Course.id.desc()).all()
    return render_template('admin/courses.html', courses=courses, search=search)


@admin_bp.route('/admin/course/edit/<int:id>', methods=['POST'])
@admin_required
def edit_course(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    success, msg, _ = AdminService.update_course(admin, id, request.form, ip)
    flash(msg, 'success' if success else 'danger')
    return redirect(url_for('admin.courses_crud'))


@admin_bp.route('/admin/course/delete/<int:id>', methods=['POST'])
@admin_required
def delete_course(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'

    success, msg = AdminService.delete_course(admin, id, ip)
    flash(msg, 'info' if success else 'danger')
    return redirect(url_for('admin.courses_crud'))


# --- APPLICATIONS MANAGEMENT ---
@admin_bp.route('/admin/applications')
@admin_required
def applications_manage():
    status_filter = request.args.get('status', 'All')
    type_filter = request.args.get('type', 'All')

    query = Application.query
    if status_filter != 'All':
        query = query.filter_by(status=status_filter)
    if type_filter != 'All':
        query = query.filter_by(opportunity_type=type_filter)

    applications = query.order_by(Application.created_at.desc()).all()
    return render_template(
        'admin/applications.html',
        applications=applications,
        selected_status=status_filter,
        selected_type=type_filter
    )


@admin_bp.route('/admin/application/update-status/<int:id>', methods=['POST'])
@admin_required
def update_application_status_admin(id):
    admin = db.session.get(User, session['user_id'])
    ip = request.remote_addr or '127.0.0.1'
    new_status = request.form.get('status', 'Applied')
    notes = request.form.get('notes', '')

    success, msg, _ = AdminService.update_application_status(admin, id, new_status, notes, ip)
    flash(msg, 'success' if success else 'danger')
    return redirect(request.referrer or url_for('admin.applications_manage'))


# --- AUDIT LOGS ---
@admin_bp.route('/admin/audit-logs')
@admin_required
def audit_logs():
    search = request.args.get('search', '').strip()
    entity = request.args.get('entity', 'All').strip()
    page = request.args.get('page', 1, type=int)

    pagination = AdminService.get_audit_logs(search=search, entity=entity, page=page, per_page=20)
    entities = ['All', 'Scholarship', 'Internship', 'Course', 'Application', 'User']

    return render_template(
        'admin/audit_logs.html',
        pagination=pagination,
        logs=pagination.items,
        search=search,
        selected_entity=entity,
        entities=entities
    )
