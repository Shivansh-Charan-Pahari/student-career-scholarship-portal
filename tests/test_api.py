"""
Integration Tests for REST API Endpoints & Response Formats
"""

import unittest
from app import create_app
from config import TestingConfig
from models import db, User, Scholarship, Internship, Course
from services.auth_service import AuthService

class TestRestApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed sample data
        _, _, self.student = AuthService.register_user("API Tester", "api@test.com", "ApiPass@123")
        self.sch = Scholarship(
            name="API Test Grant",
            provider="API Foundation",
            description="Testing API",
            amount="₹25,000",
            deadline="2026-12-31",
            is_active=True
        )
        self.intern = Internship(
            company="API Corp",
            title="Backend Intern",
            description="Testing Intern API",
            location="Remote",
            duration="3 Months",
            stipend="₹30,000",
            required_skills="Python, SQL",
            domain="Web Development",
            deadline="2026-11-30",
            is_active=True
        )
        self.course = Course(
            name="API Mastery",
            platform="Coursera",
            description="Course Description",
            duration="4 Weeks",
            skill="Python",
            is_active=True
        )
        db.session.add_all([self.sch, self.intern, self.course])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_scholarships_api(self):
        res = self.client.get('/api/scholarships')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
        self.assertGreaterEqual(len(data['data']), 1)

    def test_get_internships_api(self):
        res = self.client.get('/api/internships')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

    def test_get_courses_api(self):
        res = self.client.get('/api/courses')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

    def test_check_eligibility_api(self):
        # Without login -> 401
        res = self.client.post('/api/check-eligibility', json={'scholarship_id': self.sch.id})
        self.assertEqual(res.status_code, 401)

        # With login
        self.client.post('/login', data={'email': 'api@test.com', 'password': 'ApiPass@123'})
        res_auth = self.client.post('/api/check-eligibility', json={'scholarship_id': self.sch.id})
        self.assertEqual(res_auth.status_code, 200)
        json_data = res_auth.get_json()
        self.assertTrue(json_data['success'])
        self.assertIn('result', json_data['data'])

    def test_global_search_api(self):
        res = self.client.get('/api/search?q=API')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('results', data['data'])

if __name__ == '__main__':
    unittest.main()
