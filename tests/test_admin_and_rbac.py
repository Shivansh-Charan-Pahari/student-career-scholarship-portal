"""
Unit & Integration Tests for Administrator RBAC, CRUD, and Audit Logs
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app
from config import TestingConfig
from models import db, User, Scholarship, Internship, Course, Application, AdminActionLog
from services.auth_service import AuthService
from services.admin_service import AdminService

class TestAdminAndRBAC(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Create 1 student and 1 admin
        _, _, self.student = AuthService.register_user("Student User", "student@test.com", "Student@123", role="student")
        _, _, self.admin = AuthService.register_user("Admin User", "admin@test.com", "Admin@123", role="admin")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_student_blocked_from_admin_pages(self):
        # Log in as student
        self.client.post('/login', data={'email': 'student@test.com', 'password': 'Student@123'})
        
        # Try accessing admin endpoints
        res = self.client.get('/admin/dashboard', follow_redirects=False)
        self.assertIn(res.status_code, [302, 403])

        res_sch = self.client.get('/admin/scholarships', follow_redirects=False)
        self.assertIn(res_sch.status_code, [302, 403])

    def test_admin_full_scholarship_crud_and_audit(self):
        # 1. Admin Create Scholarship
        create_ok, msg, sch = AdminService.create_scholarship(self.admin, {
            'name': 'Government Merit Award',
            'provider': 'Education Board',
            'description': 'Award description',
            'amount': '₹70,000 / Year',
            'amount_numeric': '70000',
            'deadline': '2026-12-31',
            'minimum_cgpa': '8.0'
        }, ip='127.0.0.1')
        self.assertTrue(create_ok)
        self.assertIsNotNone(sch)

        # Verify audit log generated for this specific scholarship
        log_create = AdminActionLog.query.filter_by(action="CREATE_SCHOLARSHIP", target_id=sch.id).first()
        self.assertIsNotNone(log_create)
        self.assertEqual(log_create.admin_id, self.admin.id)
        self.assertIn("Government Merit Award", log_create.details)

        # 2. Admin Update Scholarship
        up_ok, _, updated_sch = AdminService.update_scholarship(self.admin, sch.id, {
            'name': 'Government Merit Award (Revised)',
            'amount': '₹80,000 / Year'
        })
        self.assertTrue(up_ok)
        self.assertEqual(updated_sch.name, 'Government Merit Award (Revised)')

        # 3. Admin Delete Scholarship
        del_ok, _ = AdminService.delete_scholarship(self.admin, sch.id)
        self.assertTrue(del_ok)
        self.assertIsNone(db.session.get(Scholarship, sch.id))

        # Verify delete audit log
        log_del = AdminActionLog.query.filter_by(action="DELETE_SCHOLARSHIP").first()
        self.assertIsNotNone(log_del)

if __name__ == '__main__':
    unittest.main()
