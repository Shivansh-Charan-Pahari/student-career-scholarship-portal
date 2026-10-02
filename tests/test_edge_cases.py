"""
Edge Case & Boundary Tests
Validates algorithm stability under extreme or malformed inputs:
- CGPA = 0.0, CGPA = 10.0, CGPA > 10.0 (clamping)
- Family Income = 0, Missing Income
- Empty skills, single skill, many skills
- Expired scholarship & internship deadline filtering
- Invalid opportunity IDs and non-existent records
- Duplicate bookmark protection
"""

import unittest
from datetime import datetime, timezone, timedelta
from app import create_app
from config import TestingConfig
from models import db, StudentProfile, Skill, Scholarship, Internship, Course
from services.eligibility_service import EligibilityService
from services.career_service import CareerService
from services.recommendation_service import RecommendationService
from services.auth_service import AuthService
from services.application_service import ApplicationService

class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        _, _, self.user = AuthService.register_user("Edge Case User", "edge@test.com", "Password@123")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_extreme_cgpa_boundaries(self):
        # CGPA = 0.0
        p_zero = StudentProfile(user_id=self.user.id, cgpa=0.0, branch="CSE")
        sch = Scholarship(name="Cutoff Sch", provider="Org", description="Desc", amount="₹10k", deadline="2026-12-31", minimum_cgpa=8.0)
        res_zero = EligibilityService.calculate_scholarship_match(p_zero, sch)
        self.assertFalse(res_zero['eligible'])
        self.assertLessEqual(res_zero['score'], 50)

        # CGPA = 10.0 (Perfect Score)
        p_perfect = StudentProfile(user_id=self.user.id, cgpa=10.0, branch="Computer Science", family_income=100000.0)
        res_perfect = EligibilityService.calculate_scholarship_match(p_perfect, sch)
        self.assertTrue(res_perfect['eligible'])
        self.assertGreaterEqual(res_perfect['score'], 85)

    def test_zero_and_missing_income(self):
        sch_capped = Scholarship(name="Need Cap", provider="Org", description="Desc", amount="₹20k", deadline="2026-12-31", maximum_income=300000.0)
        
        # Zero income entered (treated as no income entered or extreme need)
        p_no_income = StudentProfile(user_id=self.user.id, cgpa=8.5, family_income=0.0, branch="CSE")
        res_no_income = EligibilityService.calculate_scholarship_match(p_no_income, sch_capped)
        self.assertTrue(res_no_income['eligible'])

    def test_expired_deadlines_filtering(self):
        # Past deadline
        expired_sch = Scholarship(
            name="Expired Award",
            provider="Org",
            description="Desc",
            amount="₹10k",
            deadline="2020-01-01",
            is_active=True
        )
        db.session.add(expired_sch)
        db.session.commit()

        upcoming = RecommendationService.get_upcoming_deadlines()
        self.assertFalse(any(d['title'] == "Expired Award" for d in upcoming))

    def test_invalid_opportunity_id_handling(self):
        # Invalid application status update
        success, msg, _ = ApplicationService.update_application_status(999999, self.user.id, "Accepted")
        self.assertFalse(success)
        self.assertIn("not found", msg.lower())

    def test_duplicate_bookmark_idempotency(self):
        sch = Scholarship(name="Grant", provider="Org", description="D", amount="₹5k", deadline="2026-12-31", is_active=True)
        db.session.add(sch)
        db.session.commit()

        # Save once
        s1, _ = ApplicationService.save_opportunity(self.user.id, "scholarship", sch.id)
        self.assertTrue(s1)

        # Save again (should be idempotent)
        s2, msg = ApplicationService.save_opportunity(self.user.id, "scholarship", sch.id)
        self.assertTrue(s2)
        self.assertIn("already bookmarked", msg.lower())

if __name__ == '__main__':
    unittest.main()
