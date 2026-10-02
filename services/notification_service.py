"""
Notification Management Service
Handles:
- Priority-tiered user notifications (INFO, WARNING, IMPORTANT)
- Unread badge counter
- Read status updates
- Automated trigger for impending scholarship & internship deadlines
"""

from datetime import datetime, timezone, timedelta
from models import db, Notification, Scholarship, Internship, Application

class NotificationService:
    @staticmethod
    def send_notification(user_id: int, title: str, message: str, priority: str = 'INFO', link: str = '#') -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            priority=priority,
            link=link
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_user_notifications(user_id: int, limit: int = 50) -> list[Notification]:
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def mark_as_read(user_id: int, notification_id: int | None = None) -> bool:
        if notification_id:
            notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
            if notif:
                notif.is_read = True
        else:
            Notification.query.filter_by(user_id=user_id).update({'is_read': True})
        db.session.commit()
        return True

    @staticmethod
    def delete_notification(user_id: int, notification_id: int) -> bool:
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            db.session.delete(notif)
            db.session.commit()
            return True
        return False
