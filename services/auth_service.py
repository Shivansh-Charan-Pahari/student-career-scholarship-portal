"""
Authentication & User Management Service
Handles:
- User registration with validation & duplicate prevention
- Password hashing & verification
- Session & login management
- Student profile updates, projects, certifications, and skills management
"""

import re
from datetime import datetime, timezone
from models import db, User, StudentProfile, Skill, Project, Certification, Notification

class AuthService:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not email:
            return False
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, ""

    @staticmethod
    def register_user(name: str, email: str, password: str, role: str = 'student') -> tuple[bool, str, User | None]:
        name = (name or '').strip()
        email = (email or '').strip().lower()

        if not name:
            return False, "Full name is required.", None
        if not AuthService.is_valid_email(email):
            return False, "Please enter a valid email address.", None

        valid_pwd, msg = AuthService.validate_password_strength(password)
        if not valid_pwd:
            return False, msg, None

        # Check duplicate
        if User.query.filter_by(email=email).first():
            return False, "An account with this email address already exists.", None

        user = User(name=name, email=email, role=role, is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Initialize student profile if role is student
        if role == 'student':
            profile = StudentProfile(user_id=user.id, full_name=name)
            db.session.add(profile)

            # Welcome notification
            welcome_notif = Notification(
                user_id=user.id,
                title="Welcome to Student Career Portal!",
                message="Complete your academic profile and add your technical skills to receive personalized opportunity matches and roadmap milestones.",
                priority="IMPORTANT",
                link="/profile"
            )
            db.session.add(welcome_notif)

        db.session.commit()
        return True, "Account created successfully.", user

    @staticmethod
    def bootstrap_admin_from_env(app=None) -> tuple[bool, str, User | None]:
        """
        Idempotent Administrator Bootstrap.
        Safely creates the initial administrator from environment variables if not already present.
        Never overwrites or resets an existing admin's password.
        """
        import os
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@portal.com').strip().lower()
        admin_password = os.environ.get('ADMIN_INITIAL_PASSWORD', 'Admin@123')

        if not admin_email or not admin_password:
            return False, "ADMIN_EMAIL or ADMIN_INITIAL_PASSWORD not configured.", None

        existing_admin = User.query.filter_by(email=admin_email).first()
        if existing_admin:
            if existing_admin.role != 'admin':
                existing_admin.role = 'admin'
                db.session.commit()
            return True, f"Admin account '{admin_email}' already exists.", existing_admin

        # Create new admin
        admin = User(
            name="System Administrator",
            email=admin_email,
            role="admin",
            is_active=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        return True, f"Admin account '{admin_email}' securely bootstrapped.", admin


    @staticmethod
    def authenticate_user(email: str, password: str, required_role: str | None = None) -> tuple[bool, str, User | None]:
        email = (email or '').strip().lower()
        if not email or not password:
            return False, "Please provide both email and password.", None

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return False, "Invalid email address or password.", None

        if not user.is_active:
            return False, "Your account has been deactivated. Please contact support.", None

        if required_role and user.role != required_role:
            return False, f"Unauthorized: {required_role.capitalize()} access required.", None

        # Update last login timestamp
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()

        return True, "Authentication successful.", user

    @staticmethod
    def get_or_create_profile(user: User) -> StudentProfile:
        if not user.profile:
            profile = StudentProfile(user_id=user.id, full_name=user.name)
            db.session.add(profile)
            db.session.commit()
            return profile
        return user.profile

    @staticmethod
    def update_profile(user: User, data: dict) -> tuple[bool, str, StudentProfile]:
        profile = AuthService.get_or_create_profile(user)

        # Personal
        profile.full_name = data.get('full_name', profile.full_name or user.name).strip()
        profile.headline = data.get('headline', profile.headline or '').strip()
        profile.phone = data.get('phone', '').strip()
        profile.date_of_birth = data.get('date_of_birth', '').strip()
        profile.gender = data.get('gender', '').strip()
        profile.state = data.get('state', '').strip()
        profile.city = data.get('city', '').strip()
        profile.bio = data.get('bio', '').strip()

        # Academic
        profile.college = data.get('college', '').strip()
        profile.university = data.get('university', '').strip()
        profile.degree = data.get('degree', '').strip()
        profile.branch = data.get('branch', '').strip()
        profile.current_year = data.get('current_year', '').strip()
        profile.semester = data.get('semester', '').strip()

        try:
            profile.cgpa = max(0.0, min(10.0, float(data.get('cgpa', 0) or 0.0)))
        except (ValueError, TypeError):
            profile.cgpa = 0.0

        try:
            profile.tenth_percentage = max(0.0, min(100.0, float(data.get('tenth_percentage', 0) or 0.0)))
        except (ValueError, TypeError):
            profile.tenth_percentage = 0.0

        try:
            profile.twelfth_percentage = max(0.0, min(100.0, float(data.get('twelfth_percentage', 0) or 0.0)))
        except (ValueError, TypeError):
            profile.twelfth_percentage = 0.0

        # Financial & Social
        try:
            profile.family_income = max(0.0, float(data.get('family_income', 0) or 0.0))
        except (ValueError, TypeError):
            profile.family_income = 0.0

        profile.category = data.get('category', 'General').strip()

        # Career Goals
        profile.career_goal = data.get('career_goal', '').strip()
        profile.preferred_role = data.get('preferred_role', '').strip()

        # Professional links
        profile.resume_url = data.get('resume_url', '').strip()
        profile.github_url = data.get('github_url', '').strip()
        profile.linkedin_url = data.get('linkedin_url', '').strip()
        profile.portfolio_url = data.get('portfolio_url', '').strip()

        profile.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return True, "Profile updated successfully.", profile

    @staticmethod
    def add_or_update_skill(profile: StudentProfile, name: str, level: str = 'Intermediate', category: str = 'Technical') -> tuple[bool, str, Skill | None]:
        name = (name or '').strip()
        if not name:
            return False, "Skill name cannot be empty.", None

        existing = Skill.query.filter_by(student_id=profile.id, name=name).first()
        if existing:
            existing.level = level
            existing.category = category
            db.session.commit()
            return True, f"Proficiency updated for '{name}'.", existing

        skill = Skill(student_id=profile.id, name=name, level=level, category=category)
        db.session.add(skill)
        db.session.commit()
        return True, f"Skill '{name}' added.", skill

    @staticmethod
    def delete_skill(profile: StudentProfile, skill_id: int) -> tuple[bool, str]:
        skill = Skill.query.filter_by(id=skill_id, student_id=profile.id).first()
        if not skill:
            return False, "Skill not found."
        name = skill.name
        db.session.delete(skill)
        db.session.commit()
        return True, f"Skill '{name}' deleted."

    @staticmethod
    def add_project(profile: StudentProfile, title: str, description: str, technologies: str, github_link: str = '', live_link: str = '') -> tuple[bool, str, Project | None]:
        title = (title or '').strip()
        description = (description or '').strip()
        technologies = (technologies or '').strip()

        if not title or not description:
            return False, "Project title and description are required.", None

        proj = Project(
            student_id=profile.id,
            title=title,
            description=description,
            technologies=technologies,
            github_link=github_link.strip(),
            live_link=live_link.strip()
        )
        db.session.add(proj)
        db.session.commit()
        return True, f"Project '{title}' added successfully.", proj

    @staticmethod
    def delete_project(profile: StudentProfile, project_id: int) -> tuple[bool, str]:
        proj = Project.query.filter_by(id=project_id, student_id=profile.id).first()
        if not proj:
            return False, "Project not found."
        db.session.delete(proj)
        db.session.commit()
        return True, "Project deleted."

    @staticmethod
    def add_certification(profile: StudentProfile, name: str, issuer: str, issue_date: str = '', credential_url: str = '', credential_id: str = '') -> tuple[bool, str, Certification | None]:
        name = (name or '').strip()
        issuer = (issuer or '').strip()

        if not name or not issuer:
            return False, "Certification name and issuer are required.", None

        cert = Certification(
            student_id=profile.id,
            name=name,
            issuer=issuer,
            issue_date=issue_date.strip(),
            credential_url=credential_url.strip(),
            credential_id=credential_id.strip()
        )
        db.session.add(cert)
        db.session.commit()
        return True, f"Certification '{name}' added successfully.", cert

    @staticmethod
    def delete_certification(profile: StudentProfile, cert_id: int) -> tuple[bool, str]:
        cert = Certification.query.filter_by(id=cert_id, student_id=profile.id).first()
        if not cert:
            return False, "Certification not found."
        db.session.delete(cert)
        db.session.commit()
        return True, "Certification deleted."
