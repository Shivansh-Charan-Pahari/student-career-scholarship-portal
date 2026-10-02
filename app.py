"""
Application Factory & Main Entry Point
Student Career & Scholarship Portal
"""

import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from config import Config
from models import db, User, StudentProfile, Scholarship, Internship, Course, Notification
from routes import register_blueprints
from services.career_service import ROADMAP_DEFINITIONS
from services.notification_service import NotificationService

def create_app(config_class=Config):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(
        __name__,
        root_path=root_dir,
        static_folder=os.path.join(root_dir, 'static'),
        static_url_path='/static',
        template_folder=os.path.join(root_dir, 'templates')
    )
    app.config.from_object(config_class)

    # Ensure instance directory exists safely (avoid crash on read-only serverless filesystems)
    try:
        instance_path = os.path.join(root_dir, 'instance')
        os.makedirs(instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Security Headers Middleware
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Global Context Processors
    @app.context_processor
    def inject_globals():
        user = None
        unread_count = 0
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            if user:
                unread_count = NotificationService.get_unread_count(user.id)
        return {
            'current_user': user,
            'unread_notifications_count': unread_count,
            'is_logged_in': user is not None,
            'is_admin': session.get('role') == 'admin'
        }

    # Landing Page Route
    @app.route('/')
    def index():
        featured_scholarships = Scholarship.query.filter_by(is_active=True).order_by(Scholarship.id.desc()).limit(3).all()
        popular_internships = Internship.query.filter_by(is_active=True).order_by(Internship.id.desc()).limit(3).all()
        top_courses = Course.query.filter_by(is_active=True).order_by(Course.rating.desc()).limit(3).all()

        student_count = User.query.filter_by(role='student').count()
        scholarship_count = Scholarship.query.filter_by(is_active=True).count()
        internship_count = Internship.query.filter_by(is_active=True).count()
        course_count = Course.query.filter_by(is_active=True).count()

        stats = {
            'students': student_count,
            'scholarships': scholarship_count,
            'internships': internship_count,
            'courses': course_count
        }

        full_stack_preview = ROADMAP_DEFINITIONS.get('Full Stack Developer', [])[:4]

        return render_template(
            'index.html',
            featured_scholarships=featured_scholarships,
            popular_internships=popular_internships,
            top_courses=top_courses,
            stats=stats,
            roadmap_preview=full_stack_preview
        )

    @app.route('/favicon.ico')
    def favicon():
        return app.response_class(status=204)

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'BAD_REQUEST', 'message': str(e)}}), 400
        return render_template('404.html', error_title="400 Bad Request", error_msg="The submitted request was malformed or invalid."), 400

    @app.errorhandler(401)
    def unauthorized(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}}), 401
        return redirect(url_for('auth.login', next=request.path))

    @app.errorhandler(403)
    def forbidden(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'FORBIDDEN', 'message': 'Access denied'}}), 403
        return render_template('404.html', error_title="403 Forbidden", error_msg="You do not have administrative permission to access this resource."), 403

    @app.errorhandler(404)
    def page_not_found(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Resource not found'}}), 404
        return render_template('404.html', error_title="404 Not Found", error_msg="The page or resource you are looking for does not exist."), 404

    @app.errorhandler(409)
    def conflict(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'CONFLICT', 'message': 'Resource already exists or conflicting state.'}}), 409
        return render_template('404.html', error_title="409 Conflict", error_msg="A conflicting record or duplicate entry already exists."), 409

    @app.errorhandler(422)
    def unprocessable_entity(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'UNPROCESSABLE_ENTITY', 'message': str(e)}}), 422
        return render_template('404.html', error_title="422 Validation Error", error_msg="Semantic validation error in submitted payload."), 422

    @app.errorhandler(429)
    def too_many_requests(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'TOO_MANY_REQUESTS', 'message': 'Rate limit exceeded. Please try again later.'}}), 429
        return render_template('404.html', error_title="429 Rate Limit Exceeded", error_msg="Too many requests submitted. Please slow down and try again."), 429

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'An unexpected server error occurred'}}), 500
        return render_template('500.html'), 500

    with app.app_context():
        try:
            db.create_all()
            # Safe idempotent admin bootstrap & demo seed if not in testing mode
            if not app.config.get('TESTING'):
                if Scholarship.query.count() == 0:
                    from seed import seed_database
                    seed_database(app, reset=False)
                else:
                    from services.auth_service import AuthService
                    AuthService.bootstrap_admin_from_env(app)
        except Exception as err:
            import sys
            print(f"[ERROR] Application context initialization warning: {err}", file=sys.stderr)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    app.run(debug=True, host=host, port=port)
