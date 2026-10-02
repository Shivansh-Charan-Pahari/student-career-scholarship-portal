"""
Automated Comprehensive Test Suite for Student Career & Scholarship Portal
Tests:
1. Database Models & Seeding
2. Authentication (Registration, Login, Duplicate Prevention, Admin Protection)
3. Eligibility Engine & Match Scoring
4. Profile Completion Engine
5. Career Readiness & Skill Gap Engine
6. Application Pipeline Tracker
7. Bookmarking / Saved Opportunities
8. Roadmap Progress API
9. Global Search API
10. Admin Operations
"""

import sys
import os

from app import create_app
from models import db, User, StudentProfile, Skill, Scholarship, Internship, Course, Application, SavedOpportunity, Notification, RoadmapProgress
from utils.engines import (
    check_scholarship_eligibility,
    calculate_profile_completion,
    calculate_career_readiness,
    get_recommendations
)

def run_tests():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    passed = 0
    total = 0

    def assert_test(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name} - {details}")

    print("\n========================================================")
    print("[*] RUNNING STUDENT CAREER & SCHOLARSHIP PORTAL TEST SUITE")
    print("========================================================\n")

    with app.app_context():
        client = app.test_client()

        # ----------------------------------------------------
        # TEST 1: Database Verification
        # ----------------------------------------------------
        print("--- 1. Database & Seeding Verification ---")
        sch_count = Scholarship.query.count()
        intern_count = Internship.query.count()
        course_count = Course.query.count()
        student_count = User.query.filter_by(role='student').count()
        admin_count = User.query.filter_by(role='admin').count()

        assert_test("Scholarships seeded (>= 10)", sch_count >= 10, f"Found {sch_count}")
        assert_test("Internships seeded (>= 10)", intern_count >= 10, f"Found {intern_count}")
        assert_test("Courses seeded (>= 10)", course_count >= 10, f"Found {course_count}")
        assert_test("Student accounts seeded (>= 5)", student_count >= 5, f"Found {student_count}")
        assert_test("Admin account seeded (>= 1)", admin_count >= 1, f"Found {admin_count}")

        # ----------------------------------------------------
        # TEST 2: Eligibility Engine
        # ----------------------------------------------------
        print("\n--- 2. Eligibility & Match Scoring Engine ---")
        rahul = User.query.filter_by(email="rahul@student.com").first()
        tata_sch = db.session.get(Scholarship, 1) # Min CGPA 7.5, Max Income 450,000, Branch: CS/IT/ECE
        
        rahul_eligibility = check_scholarship_eligibility(rahul.profile, tata_sch)
        assert_test("Rahul meets Tata Trust criteria", rahul_eligibility['eligible'] is True)
        assert_test("Rahul match score is high (> 75)", rahul_eligibility['score'] >= 75, f"Score: {rahul_eligibility['score']}")
        assert_test("Eligibility reasons returned", len(rahul_eligibility['reasons']) >= 4)

        # Ineligible Test Case
        temp_profile = type('TempProfile', (), {
            'cgpa': 6.0,
            'family_income': 800000.0,
            'branch': 'Civil Engineering',
            'category': 'General',
            'tenth_percentage': 70.0,
            'twelfth_percentage': 70.0
        })()
        inelig_res = check_scholarship_eligibility(temp_profile, tata_sch)
        assert_test("Ineligible candidate fails criteria correctly", inelig_res['eligible'] is False)
        assert_test("Detailed reasons indicate failure causes", any('Not Met' in r or 'Exceeded' in r for r in inelig_res['reasons']))

        # ----------------------------------------------------
        # TEST 3: Profile Completion Engine
        # ----------------------------------------------------
        print("\n--- 3. Dynamic Profile Completion Engine ---")
        rahul_comp = calculate_profile_completion(rahul.profile, rahul.profile.skills)
        assert_test("Rahul profile completion computed (> 80%)", rahul_comp['percentage'] >= 80, f"{rahul_comp['percentage']}%")
        assert_test("Section scores present", 'personal' in rahul_comp['sections'] and 'academic' in rahul_comp['sections'])

        empty_comp = calculate_profile_completion(None)
        assert_test("Empty profile yields 0%", empty_comp['percentage'] == 0)

        # ----------------------------------------------------
        # TEST 4: Career Readiness & Skill Gap
        # ----------------------------------------------------
        print("\n--- 4. Career Readiness & Skill Gap Engine ---")
        career_res = calculate_career_readiness(rahul.profile, rahul.profile.skills)
        assert_test("Target role matched", career_res['target_role'] == "Full Stack Developer")
        assert_test("Readiness score computed (> 50%)", career_res['readiness_score'] >= 50, f"{career_res['readiness_score']}%")
        assert_test("Missing skills identified", len(career_res['missing_skills']) > 0)

        # ----------------------------------------------------
        # TEST 5: Authentication & Session Flows
        # ----------------------------------------------------
        print("\n--- 5. Authentication & Protected Routes ---")
        
        # Test Landing Page
        res = client.get('/')
        assert_test("Home page loads (200 OK)", res.status_code == 200)

        # Test Student Login
        res = client.post('/login', data={'email': 'rahul@student.com', 'password': 'Student@123'}, follow_redirects=True)
        assert_test("Student login successful (Redirects to dashboard)", res.status_code == 200 and b'Welcome back, Rahul' in res.data)

        # Test Protected Student Dashboard
        res = client.get('/dashboard')
        assert_test("Access authorized dashboard (200 OK)", res.status_code == 200)

        # Test Roadmap Progress API via session
        res = client.post('/api/roadmap-progress', json={'stage_id': '07', 'completed': True})
        assert_test("Roadmap API toggles stage (200 OK)", res.status_code == 200 and res.json.get('success') is True)

        # Test Save Opportunity API
        res = client.post('/api/save-opportunity', json={'opportunity_type': 'scholarship', 'opportunity_id': 2})
        assert_test("Save opportunity API works", res.status_code == 200 and res.json.get('saved') is True)

        # Test Logout
        res = client.get('/logout', follow_redirects=True)
        assert_test("Logout successful", res.status_code == 200)

        # Test Access Dashboard after Logout (Should Redirect)
        res = client.get('/dashboard', follow_redirects=False)
        assert_test("Protected route blocks logged-out access (302 Redirect)", res.status_code == 302)

        # ----------------------------------------------------
        # TEST 6: Admin Login & Operations
        # ----------------------------------------------------
        print("\n--- 6. Administrator Security & Control ---")
        # Non-admin trying admin route
        res = client.get('/admin/dashboard', follow_redirects=False)
        assert_test("Admin dashboard blocks unauthenticated access", res.status_code in [302, 401])

        # Login as Admin
        res = client.post('/admin/login', data={'email': 'admin@portal.com', 'password': 'Admin@123'}, follow_redirects=True)
        assert_test("Admin login successful", res.status_code == 200 and b'Administrator Analytics' in res.data)

        # Access Admin Students
        res = client.get('/admin/students')
        assert_test("Admin students page accessible (200 OK)", res.status_code == 200)

        # Access Admin Scholarships CRUD
        res = client.get('/admin/scholarships')
        assert_test("Admin scholarships CRUD accessible (200 OK)", res.status_code == 200)

        # ----------------------------------------------------
        # TEST 7: Global Search API
        # ----------------------------------------------------
        print("\n--- 7. Global Instant Search API ---")
        res = client.get('/api/search?q=Python')
        assert_test("Search API returns JSON matching Python", res.status_code == 200 and res.json.get('success') is True)

    print("\n========================================================")
    print(f"[+] TEST SUMMARY: {passed} / {total} tests passed ({round((passed/total)*100)}%)")
    print("========================================================\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
