"""
Database Models for Student Career & Scholarship Portal
Defines relational schema, constraints, indexes, timestamps, and ORM relationships.
Demonstrates:
- 3NF relational database normalization
- Foreign keys with ON DELETE CASCADE
- Composite and single-column indexing for query optimization
- JSON serialization helpers (to_dict)
- Password hashing & verification
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False, index=True) # 'student' or 'admin'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    saved_opportunities = db.relationship('SavedOpportunity', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    roadmap_progress = db.relationship('RoadmapProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    admin_logs = db.relationship('AdminActionLog', backref='admin', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    
    # Personal Info
    full_name = db.Column(db.String(120))
    headline = db.Column(db.String(200)) # e.g. "Aspiring Full Stack Engineer | CSE '27"
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    state = db.Column(db.String(80))
    city = db.Column(db.String(80))
    bio = db.Column(db.Text)
    
    # Academic Info
    college = db.Column(db.String(200))
    university = db.Column(db.String(200))
    degree = db.Column(db.String(100)) # B.Tech, B.Sc, BCA, M.Tech, etc.
    branch = db.Column(db.String(100), index=True) # Computer Science, IT, ECE, etc.
    current_year = db.Column(db.String(20)) # 1st Year, 2nd Year, 3rd Year, 4th Year, Graduated
    semester = db.Column(db.String(20))
    cgpa = db.Column(db.Float, default=0.0, index=True)
    tenth_percentage = db.Column(db.Float, default=0.0)
    twelfth_percentage = db.Column(db.Float, default=0.0)
    
    # Financial & Social Info
    family_income = db.Column(db.Float, default=0.0, index=True)
    category = db.Column(db.String(50), default='General', index=True) # General, OBC, SC, ST, EWS
    
    # Career Goals
    career_goal = db.Column(db.String(150))
    preferred_role = db.Column(db.String(100))
    
    # Professional Links
    resume_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    linkedin_url = db.Column(db.String(500))
    portfolio_url = db.Column(db.String(500))
    profile_image = db.Column(db.String(500))
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relational Child Entities
    skills = db.relationship('Skill', backref='profile', lazy='select', cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='profile', lazy='select', cascade='all, delete-orphan')
    certifications = db.relationship('Certification', backref='profile', lazy='select', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name or '',
            'headline': self.headline or '',
            'phone': self.phone or '',
            'date_of_birth': self.date_of_birth or '',
            'gender': self.gender or '',
            'state': self.state or '',
            'city': self.city or '',
            'bio': self.bio or '',
            'college': self.college or '',
            'university': self.university or '',
            'degree': self.degree or '',
            'branch': self.branch or '',
            'current_year': self.current_year or '',
            'semester': self.semester or '',
            'cgpa': self.cgpa or 0.0,
            'tenth_percentage': self.tenth_percentage or 0.0,
            'twelfth_percentage': self.twelfth_percentage or 0.0,
            'family_income': self.family_income or 0.0,
            'category': self.category or 'General',
            'career_goal': self.career_goal or '',
            'preferred_role': self.preferred_role or '',
            'resume_url': self.resume_url or '',
            'github_url': self.github_url or '',
            'linkedin_url': self.linkedin_url or '',
            'portfolio_url': self.portfolio_url or '',
            'skills': [s.to_dict() for s in self.skills],
            'projects': [p.to_dict() for p in self.projects],
            'certifications': [c.to_dict() for c in self.certifications]
        }


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(30), default='Intermediate') # Beginner, Intermediate, Advanced
    category = db.Column(db.String(50), default='Technical') # Technical, Soft, Language, Tool
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'level': self.level,
            'category': self.category
        }


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(300), nullable=False) # e.g. "Python, Flask, SQLite, HTML/CSS"
    github_link = db.Column(db.String(500))
    live_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'title': self.title,
            'description': self.description,
            'technologies': [t.strip() for t in self.technologies.split(',') if t.strip()] if self.technologies else [],
            'github_link': self.github_link or '',
            'live_link': self.live_link or ''
        }


class Certification(db.Model):
    __tablename__ = 'certifications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(150), nullable=False) # Coursera, AWS, Google, HackerRank, etc.
    issue_date = db.Column(db.String(50))
    credential_url = db.Column(db.String(500))
    credential_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'issuer': self.issuer,
            'issue_date': self.issue_date or '',
            'credential_url': self.credential_url or '',
            'credential_id': self.credential_id or ''
        }


class Scholarship(db.Model):
    __tablename__ = 'scholarships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.String(100), nullable=False) # e.g. "₹50,000/year" or "100% Tuition"
    amount_numeric = db.Column(db.Float, default=0.0, index=True) # For filtering/sorting
    deadline = db.Column(db.String(50), nullable=False, index=True) # e.g. "2026-11-30"
    minimum_cgpa = db.Column(db.Float, default=0.0, index=True)
    maximum_income = db.Column(db.Float, default=0.0, index=True) # 0 means no income limit
    eligible_branches = db.Column(db.String(255), default='All') # Comma-separated or "All"
    eligible_categories = db.Column(db.String(255), default='All') # Comma-separated or "All"
    required_documents = db.Column(db.Text)
    application_url = db.Column(db.String(500), default='#')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'description': self.description,
            'amount': self.amount,
            'amount_numeric': self.amount_numeric,
            'deadline': self.deadline,
            'minimum_cgpa': self.minimum_cgpa,
            'maximum_income': self.maximum_income,
            'eligible_branches': self.eligible_branches,
            'eligible_categories': self.eligible_categories,
            'required_documents': self.required_documents,
            'application_url': self.application_url,
            'is_active': self.is_active
        }


class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    work_mode = db.Column(db.String(50), default='Remote', index=True) # Remote, Hybrid, On-site
    duration = db.Column(db.String(50), nullable=False) # e.g. "3 Months", "6 Months"
    stipend = db.Column(db.String(100), nullable=False) # e.g. "₹25,000/month", "Unpaid"
    required_skills = db.Column(db.String(300), nullable=False) # Comma-separated
    domain = db.Column(db.String(100), nullable=False, index=True) # Web Development, AI/ML, Data Science, etc.
    deadline = db.Column(db.String(50), nullable=False, index=True)
    application_url = db.Column(db.String(500), default='#')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'work_mode': self.work_mode,
            'duration': self.duration,
            'stipend': self.stipend,
            'required_skills': [s.strip() for s in self.required_skills.split(',') if s.strip()],
            'domain': self.domain,
            'deadline': self.deadline,
            'application_url': self.application_url,
            'is_active': self.is_active
        }


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100), nullable=False, index=True) # Coursera, edX, Udemy, NPTEL, FreeCodeCamp
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False) # e.g. "8 Weeks", "20 Hours"
    level = db.Column(db.String(50), default='Beginner') # Beginner, Intermediate, Advanced, All Levels
    skill = db.Column(db.String(100), nullable=False, index=True) # Python, React, Machine Learning, etc.
    price = db.Column(db.String(50), default='Free') # Free or ₹1,499
    price_numeric = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=4.5, index=True)
    course_url = db.Column(db.String(500), default='#')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'platform': self.platform,
            'description': self.description,
            'duration': self.duration,
            'level': self.level,
            'skill': self.skill,
            'price': self.price,
            'price_numeric': self.price_numeric,
            'rating': self.rating,
            'course_url': self.course_url,
            'is_active': self.is_active
        }


class Application(db.Model):
    __tablename__ = 'applications'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'opportunity_type', 'opportunity_id', name='uq_user_application'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    opportunity_type = db.Column(db.String(50), nullable=False, index=True) # 'scholarship', 'internship', 'course'
    opportunity_id = db.Column(db.Integer, nullable=False, index=True)
    status = db.Column(db.String(50), default='Applied', index=True) # Saved, Applied, Under Review, Shortlisted, Interview, Accepted, Rejected
    application_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deadline = db.Column(db.String(50))
    interview_date = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def get_opportunity(self):
        if self.opportunity_type == 'scholarship':
            return db.session.get(Scholarship, self.opportunity_id)
        elif self.opportunity_type == 'internship':
            return db.session.get(Internship, self.opportunity_id)
        elif self.opportunity_type == 'course':
            return db.session.get(Course, self.opportunity_id)
        return None

    @property
    def opportunity_title(self):
        opp = self.get_opportunity()
        if not opp:
            return f"Opportunity #{self.opportunity_id}"
        return getattr(opp, 'name', getattr(opp, 'title', f"Opportunity #{self.opportunity_id}"))

    @property
    def opportunity_provider(self):
        opp = self.get_opportunity()
        if not opp:
            return "Direct Submission"
        return getattr(opp, 'provider', getattr(opp, 'company', getattr(opp, 'platform', 'Direct Submission')))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'opportunity_type': self.opportunity_type,
            'opportunity_id': self.opportunity_id,
            'title': self.opportunity_title,
            'provider': self.opportunity_provider,
            'status': self.status,
            'application_date': self.application_date.strftime('%Y-%m-%d') if self.application_date else '',
            'deadline': self.deadline or '',
            'interview_date': self.interview_date or '',
            'notes': self.notes or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class SavedOpportunity(db.Model):
    __tablename__ = 'saved_opportunities'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'opportunity_type', 'opportunity_id', name='uq_user_opportunity'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    opportunity_type = db.Column(db.String(50), nullable=False) # 'scholarship', 'internship', 'course'
    opportunity_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_opportunity(self):
        if self.opportunity_type == 'scholarship':
            return db.session.get(Scholarship, self.opportunity_id)
        elif self.opportunity_type == 'internship':
            return db.session.get(Internship, self.opportunity_id)
        elif self.opportunity_type == 'course':
            return db.session.get(Course, self.opportunity_id)
        return None

    def to_dict(self):
        opp = self.get_opportunity()
        return {
            'id': self.id,
            'user_id': self.user_id,
            'opportunity_type': self.opportunity_type,
            'opportunity_id': self.opportunity_id,
            'opportunity': opp.to_dict() if opp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='INFO') # 'INFO', 'WARNING', 'IMPORTANT'
    link = db.Column(db.String(255), default='#')
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'priority': self.priority,
            'link': self.link or '#',
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%b %d, %Y %I:%M %p') if self.created_at else ''
        }


class RoadmapProgress(db.Model):
    __tablename__ = 'roadmap_progress'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'roadmap_item', name='uq_user_roadmap_item'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    career_role = db.Column(db.String(100), default='Full Stack Developer')
    roadmap_item = db.Column(db.String(100), nullable=False) # Stage ID, e.g. "01"
    status = db.Column(db.String(30), default='not_started') # 'not_started', 'in_progress', 'completed'
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'career_role': self.career_role,
            'roadmap_item': self.roadmap_item,
            'status': self.status,
            'completed': self.completed,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AdminActionLog(db.Model):
    __tablename__ = 'admin_action_logs'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    admin_name = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(100), nullable=False, index=True) # e.g. "CREATE_SCHOLARSHIP", "UPDATE_APPLICATION_STATUS"
    target_entity = db.Column(db.String(50), nullable=False) # "Scholarship", "Internship", "Course", "Application"
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'admin_name': self.admin_name,
            'action': self.action,
            'target_entity': self.target_entity,
            'target_id': self.target_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }
