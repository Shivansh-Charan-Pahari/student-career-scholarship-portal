"""
Engines Compatibility Module
Aliases methods from the new Service Layer for backward compatibility.
"""

from services.career_service import (
    CareerService,
    CAREER_ROLE_REQUIREMENTS,
    ROADMAP_DEFINITIONS
)
from services.eligibility_service import EligibilityService
from services.recommendation_service import RecommendationService
from services.analytics_service import AnalyticsService

# Expose default roadmap
ROADMAP_STAGES = ROADMAP_DEFINITIONS.get('Full Stack Developer', [])

def check_scholarship_eligibility(student_profile, scholarship):
    return EligibilityService.calculate_scholarship_match(student_profile, scholarship)

def calculate_profile_completion(student_profile, skills=None):
    return AnalyticsService.calculate_profile_strength(student_profile, skills)

def calculate_career_readiness(student_profile, skills=None):
    return CareerService.calculate_career_readiness(student_profile, skills)

def get_recommendations(user_id):
    return RecommendationService.get_unified_recommendations(user_id)
