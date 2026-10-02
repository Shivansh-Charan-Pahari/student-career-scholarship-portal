"""
Unit Tests for AuthService & Password Security
"""

import unittest
from app import create_app
from config import TestingConfig
from models import db, User, StudentProfile, Skill, Project, Certification
from services.auth_service import AuthService

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_email_validation(self):
        self.assertTrue(AuthService.is_valid_email("student@college.edu"))
        self.assertTrue(AuthService.is_valid_email("test.user_12@sub.domain.org"))
        self.assertFalse(AuthService.is_valid_email("invalid-email"))
        self.assertFalse(AuthService.is_valid_email("test@domain"))
        self.assertFalse(AuthService.is_valid_email(""))

    def test_password_strength(self):
        valid, msg = AuthService.validate_password_strength("Short")
        self.assertFalse(valid)
        valid_good, _ = AuthService.validate_password_strength("StrongPass@123")
        self.assertTrue(valid_good)

    def test_registration_and_hashing(self):
        success, msg, user = AuthService.register_user("Nikhil Mehra", "nikhil@college.edu", "Password123", role="student")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "student")
        self.assertNotEqual(user.password_hash, "Password123") # Must be hashed!
        self.assertTrue(user.check_password("Password123"))
        self.assertFalse(user.check_password("WrongPassword"))

        # Profile automatically created
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.full_name, "Nikhil Mehra")

        # Duplicate registration prevented
        dup_success, dup_msg, _ = AuthService.register_user("Nikhil Two", "nikhil@college.edu", "AnotherPassword")
        self.assertFalse(dup_success)
        self.assertIn("already exists", dup_msg)

    def test_authentication(self):
        AuthService.register_user("Divya Sen", "divya@college.edu", "Divya@123")
        
        # Valid login
        auth_ok, _, user = AuthService.authenticate_user("divya@college.edu", "Divya@123")
        self.assertTrue(auth_ok)
        self.assertEqual(user.name, "Divya Sen")

        # Invalid password
        auth_fail, msg, _ = AuthService.authenticate_user("divya@college.edu", "WrongPass")
        self.assertFalse(auth_fail)

        # Invalid email
        auth_unknown, _, _ = AuthService.authenticate_user("unknown@college.edu", "SomePass")
        self.assertFalse(auth_unknown)

if __name__ == '__main__':
    unittest.main()
