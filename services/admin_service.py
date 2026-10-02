"""
Admin Operations & Audit Logging Service
Handles:
- Immutable audit log creation for all sensitive administrative actions
- Paginated and filtered queries for Scholarships, Internships, Courses, Applications, Students, and Logs
- CRUD logic with database transaction integrity
"""

from datetime import datetime, timezone
from models import db, User, Scholarship, Internship, Course, Application, StudentProfile, Notification, AdminActionLog

class AdminService:
    @staticmethod
    def log_action(admin: User, action: str, entity: str, target_id: int | None, details: str, ip_address: str = '') -> AdminActionLog:
        log_entry = AdminActionLog(
            admin_id=admin.id,
            admin_name=admin.name,
            action=action,
            target_entity=entity,
            target_id=target_id,
            details=details,
            ip_address=ip_address
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry

    # -------------------------------------------------------------
    # SCHOLARSHIPS CRUD
    # -------------------------------------------------------------
    @staticmethod
    def create_scholarship(admin: User, data: dict, ip: str = '') -> tuple[bool, str, Scholarship | None]:
        name = data.get('name', '').strip()
        provider = data.get('provider', '').strip()
        description = data.get('description', '').strip()
        amount = data.get('amount', '').strip()
        deadline = data.get('deadline', '').strip()

        if not name or not provider or not description or not amount or not deadline:
            return False, "Name, provider, description, amount, and deadline are mandatory.", None

        try:
            amount_numeric = float(data.get('amount_numeric', 0) or 0.0)
        except (ValueError, TypeError):
            amount_numeric = 0.0

        try:
            minimum_cgpa = float(data.get('minimum_cgpa', 0) or 0.0)
        except (ValueError, TypeError):
            minimum_cgpa = 0.0

        try:
            maximum_income = float(data.get('maximum_income', 0) or 0.0)
        except (ValueError, TypeError):
            maximum_income = 0.0

        sch = Scholarship(
            name=name,
            provider=provider,
            description=description,
            amount=amount,
            amount_numeric=amount_numeric,
            deadline=deadline,
            minimum_cgpa=minimum_cgpa,
            maximum_income=maximum_income,
            eligible_branches=data.get('eligible_branches', 'All').strip(),
            eligible_categories=data.get('eligible_categories', 'All').strip(),
            required_documents=data.get('required_documents', '').strip(),
            application_url=data.get('application_url', '#').strip(),
            is_active=True
        )
        db.session.add(sch)
        db.session.flush()

        AdminService.log_action(admin, "CREATE_SCHOLARSHIP", "Scholarship", sch.id, f"Created scholarship '{sch.name}' by {sch.provider}", ip)
        db.session.commit()
        return True, f"Scholarship '{name}' published successfully.", sch

    @staticmethod
    def update_scholarship(admin: User, sch_id: int, data: dict, ip: str = '') -> tuple[bool, str, Scholarship | None]:
        sch = db.session.get(Scholarship, sch_id)
        if not sch:
            return False, "Scholarship not found.", None

        sch.name = data.get('name', sch.name).strip()
        sch.provider = data.get('provider', sch.provider).strip()
        sch.description = data.get('description', sch.description).strip()
        sch.amount = data.get('amount', sch.amount).strip()
        sch.deadline = data.get('deadline', sch.deadline).strip()

        try:
            sch.amount_numeric = float(data.get('amount_numeric', sch.amount_numeric) or 0.0)
        except (ValueError, TypeError):
            pass

        try:
            sch.minimum_cgpa = float(data.get('minimum_cgpa', sch.minimum_cgpa) or 0.0)
        except (ValueError, TypeError):
            pass

        try:
            sch.maximum_income = float(data.get('maximum_income', sch.maximum_income) or 0.0)
        except (ValueError, TypeError):
            pass

        sch.eligible_branches = data.get('eligible_branches', sch.eligible_branches).strip()
        sch.eligible_categories = data.get('eligible_categories', sch.eligible_categories).strip()
        sch.required_documents = data.get('required_documents', sch.required_documents).strip()
        sch.application_url = data.get('application_url', sch.application_url).strip()
        sch.updated_at = datetime.now(timezone.utc)

        AdminService.log_action(admin, "UPDATE_SCHOLARSHIP", "Scholarship", sch.id, f"Updated scholarship details for '{sch.name}'", ip)
        db.session.commit()
        return True, f"Scholarship '{sch.name}' updated successfully.", sch

    @staticmethod
    def delete_scholarship(admin: User, sch_id: int, ip: str = '') -> tuple[bool, str]:
        sch = db.session.get(Scholarship, sch_id)
        if not sch:
            return False, "Scholarship not found."

        name = sch.name
        db.session.delete(sch)
        AdminService.log_action(admin, "DELETE_SCHOLARSHIP", "Scholarship", sch_id, f"Deleted scholarship '{name}'", ip)
        db.session.commit()
        return True, f"Scholarship '{name}' deleted."

    # -------------------------------------------------------------
    # INTERNSHIPS CRUD
    # -------------------------------------------------------------
    @staticmethod
    def create_internship(admin: User, data: dict, ip: str = '') -> tuple[bool, str, Internship | None]:
        company = data.get('company', '').strip()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        location = data.get('location', '').strip()
        stipend = data.get('stipend', '').strip()
        required_skills = data.get('required_skills', '').strip()
        domain = data.get('domain', '').strip()
        deadline = data.get('deadline', '').strip()

        if not company or not title or not description or not location or not required_skills or not domain or not deadline:
            return False, "All core internship fields are required.", None

        intern = Internship(
            company=company,
            title=title,
            description=description,
            location=location,
            work_mode=data.get('work_mode', 'Remote').strip(),
            duration=data.get('duration', '3 Months').strip(),
            stipend=stipend,
            required_skills=required_skills,
            domain=domain,
            deadline=deadline,
            application_url=data.get('application_url', '#').strip(),
            is_active=True
        )
        db.session.add(intern)
        db.session.flush()

        AdminService.log_action(admin, "CREATE_INTERNSHIP", "Internship", intern.id, f"Created internship '{title}' at {company}", ip)
        db.session.commit()
        return True, f"Internship '{title} at {company}' created.", intern

    @staticmethod
    def update_internship(admin: User, intern_id: int, data: dict, ip: str = '') -> tuple[bool, str, Internship | None]:
        intern = db.session.get(Internship, intern_id)
        if not intern:
            return False, "Internship not found.", None

        intern.company = data.get('company', intern.company).strip()
        intern.title = data.get('title', intern.title).strip()
        intern.description = data.get('description', intern.description).strip()
        intern.location = data.get('location', intern.location).strip()
        intern.work_mode = data.get('work_mode', intern.work_mode).strip()
        intern.duration = data.get('duration', intern.duration).strip()
        intern.stipend = data.get('stipend', intern.stipend).strip()
        intern.required_skills = data.get('required_skills', intern.required_skills).strip()
        intern.domain = data.get('domain', intern.domain).strip()
        intern.deadline = data.get('deadline', intern.deadline).strip()
        intern.application_url = data.get('application_url', intern.application_url).strip()
        intern.updated_at = datetime.now(timezone.utc)

        AdminService.log_action(admin, "UPDATE_INTERNSHIP", "Internship", intern.id, f"Updated internship '{intern.title}' at {intern.company}", ip)
        db.session.commit()
        return True, f"Internship '{intern.title}' updated.", intern

    @staticmethod
    def delete_internship(admin: User, intern_id: int, ip: str = '') -> tuple[bool, str]:
        intern = db.session.get(Internship, intern_id)
        if not intern:
            return False, "Internship not found."

        title = intern.title
        db.session.delete(intern)
        AdminService.log_action(admin, "DELETE_INTERNSHIP", "Internship", intern_id, f"Deleted internship '{title}'", ip)
        db.session.commit()
        return True, f"Internship '{title}' deleted."

    # -------------------------------------------------------------
    # COURSES CRUD
    # -------------------------------------------------------------
    @staticmethod
    def create_course(admin: User, data: dict, ip: str = '') -> tuple[bool, str, Course | None]:
        name = data.get('name', '').strip()
        platform = data.get('platform', '').strip()
        description = data.get('description', '').strip()
        duration = data.get('duration', '').strip()
        skill = data.get('skill', '').strip()

        if not name or not platform or not description or not skill:
            return False, "Course name, platform, description, and skill are required.", None

        try:
            rating = float(data.get('rating', 4.5) or 4.5)
        except (ValueError, TypeError):
            rating = 4.5

        course = Course(
            name=name,
            platform=platform,
            description=description,
            duration=duration,
            level=data.get('level', 'Beginner').strip(),
            skill=skill,
            price=data.get('price', 'Free').strip(),
            rating=rating,
            course_url=data.get('course_url', '#').strip(),
            is_active=True
        )
        db.session.add(course)
        db.session.flush()

        AdminService.log_action(admin, "CREATE_COURSE", "Course", course.id, f"Added course '{name}' on {platform}", ip)
        db.session.commit()
        return True, f"Course '{name}' added successfully.", course

    @staticmethod
    def update_course(admin: User, course_id: int, data: dict, ip: str = '') -> tuple[bool, str, Course | None]:
        course = db.session.get(Course, course_id)
        if not course:
            return False, "Course not found.", None

        course.name = data.get('name', course.name).strip()
        course.platform = data.get('platform', course.platform).strip()
        course.description = data.get('description', course.description).strip()
        course.duration = data.get('duration', course.duration).strip()
        course.level = data.get('level', course.level).strip()
        course.skill = data.get('skill', course.skill).strip()
        course.price = data.get('price', course.price).strip()

        try:
            course.rating = float(data.get('rating', course.rating) or 4.5)
        except (ValueError, TypeError):
            pass

        course.course_url = data.get('course_url', course.course_url).strip()

        AdminService.log_action(admin, "UPDATE_COURSE", "Course", course.id, f"Updated course '{course.name}'", ip)
        db.session.commit()
        return True, f"Course '{course.name}' updated.", course

    @staticmethod
    def delete_course(admin: User, course_id: int, ip: str = '') -> tuple[bool, str]:
        course = db.session.get(Course, course_id)
        if not course:
            return False, "Course not found."

        name = course.name
        db.session.delete(course)
        AdminService.log_action(admin, "DELETE_COURSE", "Course", course_id, f"Deleted course '{name}'", ip)
        db.session.commit()
        return True, f"Course '{name}' deleted."

    # -------------------------------------------------------------
    # APPLICATION REVIEW & AUDIT LOGS
    # -------------------------------------------------------------
    @staticmethod
    def update_application_status(admin: User, app_id: int, new_status: str, notes: str = '', ip: str = '') -> tuple[bool, str, Application | None]:
        app_record = db.session.get(Application, app_id)
        if not app_record:
            return False, "Application not found.", None

        old_status = app_record.status
        app_record.status = new_status
        if notes:
            app_record.notes = notes
        app_record.updated_at = datetime.now(timezone.utc)

        # Trigger notification to student
        notif = Notification(
            user_id=app_record.user_id,
            title=f"Application Status Updated: {new_status}",
            message=f"Administrator reviewed your application for {app_record.opportunity_type}. Status set to '{new_status}'.",
            priority="IMPORTANT",
            link="/applications"
        )
        db.session.add(notif)

        AdminService.log_action(admin, "UPDATE_APPLICATION_STATUS", "Application", app_record.id, f"Changed Application #{app_id} status from '{old_status}' to '{new_status}'", ip)
        db.session.commit()
        return True, f"Application #{app_id} updated to '{new_status}'.", app_record

    @staticmethod
    def get_audit_logs(search: str = '', entity: str = 'All', page: int = 1, per_page: int = 20):
        query = AdminActionLog.query

        if search:
            fmt = f"%{search}%"
            query = query.filter((AdminActionLog.admin_name.ilike(fmt)) | (AdminActionLog.action.ilike(fmt)) | (AdminActionLog.details.ilike(fmt)))

        if entity != 'All':
            query = query.filter_by(target_entity=entity)

        return query.order_by(AdminActionLog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
