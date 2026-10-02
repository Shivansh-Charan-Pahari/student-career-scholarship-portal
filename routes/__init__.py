from flask import Blueprint

def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.scholarships import scholarships_bp
    from routes.internships import internships_bp
    from routes.courses import courses_bp
    from routes.applications import applications_bp
    from routes.career import career_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(scholarships_bp)
    app.register_blueprint(internships_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
