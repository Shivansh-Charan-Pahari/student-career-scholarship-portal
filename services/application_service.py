"""
Application Management & Tracking Service
Handles:
- Complete application lifecycle: Saved -> Applied -> Under Review -> Shortlisted -> Interview -> Accepted / Rejected
- Application notes and timeline updates
- Dynamic application analytics, success rate, and conversion funnel calculations
- Saved opportunities (Bookmarks)
"""

from datetime import datetime, timezone
from models import db, Application, SavedOpportunity, Notification, Scholarship, Internship, Course

VALID_STATUSES = ['Saved', 'Applied', 'Under Review', 'Shortlisted', 'Interview', 'Accepted', 'Rejected']

class ApplicationService:
    @staticmethod
    def create_or_update_application(user_id: int, opp_type: str, opp_id: int, status: str = 'Applied', notes: str = '', deadline: str = '', interview_date: str = '') -> tuple[bool, str, Application]:
        opp_type = (opp_type or 'scholarship').lower()
        if status not in VALID_STATUSES:
            status = 'Applied'

        # Verify opportunity exists
        opp_title = f"{opp_type.capitalize()} #{opp_id}"
        if opp_type == 'scholarship':
            obj = db.session.get(Scholarship, opp_id)
            if obj:
                opp_title = obj.name
        elif opp_type == 'internship':
            obj = db.session.get(Internship, opp_id)
            if obj:
                opp_title = f"{obj.title} ({obj.company})"
        elif opp_type == 'course':
            obj = db.session.get(Course, opp_id)
            if obj:
                opp_title = obj.name

        existing = Application.query.filter_by(
            user_id=user_id, opportunity_type=opp_type, opportunity_id=opp_id
        ).first()

        if existing:
            existing.status = status
            if notes:
                existing.notes = notes
            if deadline:
                existing.deadline = deadline
            if interview_date:
                existing.interview_date = interview_date
            existing.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return True, f"Application updated to '{status}'.", existing

        new_app = Application(
            user_id=user_id,
            opportunity_type=opp_type,
            opportunity_id=opp_id,
            status=status,
            notes=notes,
            deadline=deadline,
            interview_date=interview_date
        )
        db.session.add(new_app)

        # Trigger notification
        notif = Notification(
            user_id=user_id,
            title="Application Logged",
            message=f"You successfully tracked your application for '{opp_title}'. Current status: {status}.",
            priority="INFO",
            link="/applications"
        )
        db.session.add(notif)
        db.session.commit()

        return True, "Application logged successfully.", new_app

    @staticmethod
    def update_application_status(app_id: int, user_id: int | None, new_status: str, notes: str = '', is_admin: bool = False) -> tuple[bool, str, Application | None]:
        if new_status not in VALID_STATUSES:
            return False, f"Invalid status '{new_status}'.", None

        query = Application.query.filter_by(id=app_id)
        if not is_admin and user_id is not None:
            query = query.filter_by(user_id=user_id)

        app_record = query.first()
        if not app_record:
            return False, "Application record not found.", None

        old_status = app_record.status
        app_record.status = new_status
        if notes:
            app_record.notes = notes
        app_record.updated_at = datetime.now(timezone.utc)

        # Notify student if updated
        notif = Notification(
            user_id=app_record.user_id,
            title=f"Application Status Updated: {new_status}",
            message=f"Your application status for {app_record.opportunity_title} changed from '{old_status}' to '{new_status}'.",
            priority="IMPORTANT" if new_status in ['Shortlisted', 'Interview', 'Accepted'] else "INFO",
            link="/applications"
        )
        db.session.add(notif)
        db.session.commit()

        return True, f"Status updated to '{new_status}'.", app_record

    @staticmethod
    def delete_application(app_id: int, user_id: int | None, is_admin: bool = False) -> tuple[bool, str]:
        query = Application.query.filter_by(id=app_id)
        if not is_admin and user_id is not None:
            query = query.filter_by(user_id=user_id)

        app_record = query.first()
        if not app_record:
            return False, "Application not found."

        db.session.delete(app_record)
        db.session.commit()
        return True, "Application removed from tracker."

    @staticmethod
    def get_user_application_analytics(user_id: int) -> dict:
        apps = Application.query.filter_by(user_id=user_id).all()
        total = len(apps)

        status_counts = {s: 0 for s in VALID_STATUSES}
        type_counts = {'scholarship': 0, 'internship': 0, 'course': 0}

        for a in apps:
            status_counts[a.status] = status_counts.get(a.status, 0) + 1
            type_counts[a.opportunity_type] = type_counts.get(a.opportunity_type, 0) + 1

        accepted_count = status_counts.get('Accepted', 0)
        shortlisted_count = status_counts.get('Shortlisted', 0) + status_counts.get('Interview', 0) + accepted_count

        acceptance_rate = round((accepted_count / total) * 100, 1) if total > 0 else 0.0
        shortlist_rate = round((shortlisted_count / total) * 100, 1) if total > 0 else 0.0

        return {
            'total_applications': total,
            'total': total,
            'applied': status_counts.get('Applied', 0),
            'under_review': status_counts.get('Under Review', 0),
            'shortlisted': status_counts.get('Shortlisted', 0),
            'interview': status_counts.get('Interview', 0),
            'accepted': status_counts.get('Accepted', 0),
            'rejected': status_counts.get('Rejected', 0),
            'saved': status_counts.get('Saved', 0),
            'status_counts': status_counts,
            'type_counts': type_counts,
            'acceptance_rate': acceptance_rate,
            'shortlist_rate': shortlist_rate,
            'pipeline_funnel': [
                {'stage': 'Applied', 'count': status_counts['Applied']},
                {'stage': 'Under Review', 'count': status_counts['Under Review']},
                {'stage': 'Shortlisted', 'count': status_counts['Shortlisted']},
                {'stage': 'Interview', 'count': status_counts['Interview']},
                {'stage': 'Accepted', 'count': status_counts['Accepted']}
            ]
        }

    # Bookmark / Saved Opportunities
    @staticmethod
    def save_opportunity(user_id: int, opp_type: str, opp_id: int) -> tuple[bool, str]:
        existing = SavedOpportunity.query.filter_by(
            user_id=user_id, opportunity_type=opp_type, opportunity_id=opp_id
        ).first()

        if existing:
            return True, "Opportunity is already bookmarked."

        saved = SavedOpportunity(user_id=user_id, opportunity_type=opp_type, opportunity_id=opp_id)
        db.session.add(saved)
        db.session.commit()
        return True, f"{opp_type.capitalize()} bookmarked successfully."

    @staticmethod
    def remove_saved_opportunity(user_id: int, opp_type: str = '', opp_id: int = 0, item_id: int | None = None) -> tuple[bool, str]:
        if item_id:
            saved = SavedOpportunity.query.filter_by(id=item_id, user_id=user_id).first()
        else:
            saved = SavedOpportunity.query.filter_by(
                user_id=user_id, opportunity_type=opp_type, opportunity_id=opp_id
            ).first()

        if not saved:
            return False, "Bookmark not found."

        db.session.delete(saved)
        db.session.commit()
        return True, "Bookmark removed."
