"""
Unit Tests for Application Lifecycle & Analytics
"""

import unittest
from app import create_app
from config import TestingConfig
from models import db, User, Application, Scholarship, Internship, Course, SavedOpportunity
from services.auth_service import AuthService
from services.application_service import ApplicationService

class TestApplicationService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create student user
        _, _, self.student = AuthService.register_user("Test Applicant", "applicant@test.com", "Pass@123")
        
        # Create opportunity
        self.sch = Scholarship(
            name="Test Grant",
            provider="Test Org",
            description="Test Description",
            amount="₹50,000",
            deadline="2026-12-31"
        )
        db.session.add(self.sch)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_application_lifecycle(self):
        # 1. Create Application
        success, msg, app_rec = ApplicationService.create_or_update_application(
            self.student.id, "scholarship", self.sch.id, status="Applied", notes="Initial application"
        )
        self.assertTrue(success)
        self.assertEqual(app_rec.status, "Applied")

        # 2. Update Status to Shortlisted
        up_success, _, updated_app = ApplicationService.update_application_status(
            app_rec.id, self.student.id, "Shortlisted", notes="Review passed"
        )
        self.assertTrue(up_success)
        self.assertEqual(updated_app.status, "Shortlisted")

        # 3. Update Status to Accepted
        acc_success, _, final_app = ApplicationService.update_application_status(
            app_rec.id, self.student.id, "Accepted"
        )
        self.assertTrue(acc_success)
        self.assertEqual(final_app.status, "Accepted")

        # 4. Analytics
        analytics = ApplicationService.get_user_application_analytics(self.student.id)
        self.assertEqual(analytics['total_applications'], 1)
        self.assertEqual(analytics['acceptance_rate'], 100.0)

    def test_bookmark_saved_opportunities(self):
        # Save
        s_ok, _ = ApplicationService.save_opportunity(self.student.id, "scholarship", self.sch.id)
        self.assertTrue(s_ok)
        
        saved_count = SavedOpportunity.query.filter_by(user_id=self.student.id).count()
        self.assertEqual(saved_count, 1)

        # Remove
        r_ok, _ = ApplicationService.remove_saved_opportunity(self.student.id, "scholarship", self.sch.id)
        self.assertTrue(r_ok)
        self.assertEqual(SavedOpportunity.query.filter_by(user_id=self.student.id).count(), 0)

if __name__ == '__main__':
    unittest.main()
