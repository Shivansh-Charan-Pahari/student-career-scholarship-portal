"""
Service Layer Package for Student Career & Scholarship Portal
Provides clean separation of business logic from routing and presentation layers.
"""
from services.auth_service import AuthService
from services.eligibility_service import EligibilityService
from services.career_service import CareerService, ROADMAP_DEFINITIONS
from services.recommendation_service import RecommendationService
from services.application_service import ApplicationService
from services.notification_service import NotificationService
from services.analytics_service import AnalyticsService
from services.admin_service import AdminService

__all__ = [
    'AuthService',
    'EligibilityService',
    'CareerService',
    'RecommendationService',
    'ApplicationService',
    'NotificationService',
    'AnalyticsService',
    'AdminService',
    'ROADMAP_DEFINITIONS'
]
