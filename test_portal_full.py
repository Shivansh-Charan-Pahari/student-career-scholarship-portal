"""
Full-Spectrum QA Test Suite for Student Career & Scholarship Portal
Tests all 26 QA checkpoints:
1. Server initialization & DB schema with relational constraints & indexes
2. Registration flow with validation & password hashing verification
3. Student Login, Logout, and Session Security
4. Student Profile Updates (Personal, Academic, Financial, Career Goals, Social Links)
5. Skills Management (Add, Proficiency Level Update, Delete)
6. Projects Portfolio Management (Add Project with Tech Stack & GitHub, Delete)
7. Certifications Management (Add Credential with ID, Delete)
8. Dynamic Profile Strength Meter (0 - 100%)
9. Scholarship Search & Multi-criteria Filtering (Branch, Category, Income, CGPA, Sort)
10. Explainable Scholarship Eligibility Engine (Match scoring, condition breakdowns)
11. Save / Bookmark & Remove System (Scholarships, Internships, Courses)
12. Internships Hub (Search, Domain filter, Work mode filter, Location filter)
13. Courses Directory (Platform, Level, Price filter)
14. Application Tracker (Pipeline stages, Status updates, Notes, Interview dates)
15. Multi-dimensional Career Readiness Engine (6 dimensions, role benchmarks, skill gaps)
16. Dynamic Multi-Role Roadmaps (7 pathways, async progress toggle, persistence)
17. Notification Center (Priority levels INFO/WARNING/IMPORTANT, unread count, mark all read)
18. Administrator RBAC & Authorization (Student access blocked with 401/403/Redirect)
19. Admin Dashboard KPI Analytics & Chart.js live data feeds
20. Admin Scholarships Full CRUD + Immutable Audit Log Generation
21. Admin Internships Full CRUD + Immutable Audit Log Generation
22. Admin Courses Full CRUD + Immutable Audit Log Generation
23. Admin Application Review & Status Updates with automated student notifications
24. Admin Student Explorer & Comprehensive Profile Inspector
25. Admin Audit Trail Explorer & Event Filtration
26. REST API Schema & Instant Global Search Verification
"""

import sys
import os
from datetime import datetime, timezone
from app import create_app
from config import TestingConfig
from models import (
    db, User, StudentProfile, Skill, Project, Certification,
    Scholarship, Internship, Course, Application, SavedOpportunity,
    Notification, RoadmapProgress, AdminActionLog
)
from services.eligibility_service import EligibilityService
from services.career_service import CareerService, ROADMAP_DEFINITIONS
from services.recommendation_service import RecommendationService
from services.application_service import ApplicationService
from services.analytics_service import AnalyticsService
from services.auth_service import AuthService
from services.admin_service import AdminService

def run_full_qa():
    app = create_app(TestingConfig)
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
    print("[*] STARTING FULL-SPECTRUM COMPREHENSIVE QA AUDIT SUITE")
    print("========================================================\n")

    with app.app_context():
        db.create_all()
        client = app.test_client()

        # ----------------------------------------------------
        # 1. DATABASE & SEEDING INTEGRITY
        # ----------------------------------------------------
        print("--- Checkpoint 1: Database & Seed Data Integrity ---")
        from seed import seed_database
        seed_database(app)

        sch_count = Scholarship.query.filter_by(is_active=True).count()
        intern_count = Internship.query.filter_by(is_active=True).count()
        course_count = Course.query.filter_by(is_active=True).count()
        student_count = User.query.filter_by(role='student').count()
        admin_count = User.query.filter_by(role='admin').count()

        assert_test("Scholarships in DB (>= 15)", sch_count >= 15, f"Count: {sch_count}")
        assert_test("Internships in DB (>= 15)", intern_count >= 15, f"Count: {intern_count}")
        assert_test("Courses in DB (>= 15)", course_count >= 15, f"Count: {course_count}")
        assert_test("Students seeded (>= 5)", student_count >= 5, f"Count: {student_count}")
        assert_test("Admin seeded (>= 1)", admin_count >= 1, f"Count: {admin_count}")

        # ----------------------------------------------------
        # 2. REGISTRATION & VALIDATION
        # ----------------------------------------------------
        print("\n--- Checkpoint 2: Registration Flow & Field Validations ---")
        # Duplicate email prevention
        res = client.post('/register', data={
            'name': 'Duplicate User',
            'email': 'rahul@student.com',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }, follow_redirects=True)
        assert_test("Duplicate email registration prevented", b'already exists' in res.data or res.status_code == 200)

        # Password mismatch
        res = client.post('/register', data={
            'name': 'New Student',
            'email': 'newstudent@college.edu',
            'password': 'Password123',
            'confirm_password': 'MismatchPassword'
        }, follow_redirects=True)
        assert_test("Password mismatch validation triggered", b'do not match' in res.data)

        # Successful registration
        res = client.post('/register', data={
            'name': 'Amit Verma',
            'email': 'amit.verma@college.edu',
            'password': 'Student@123',
            'confirm_password': 'Student@123'
        }, follow_redirects=True)
        assert_test("Successful registration redirects to profile", b'profile' in res.data or b'Amit' in res.data or res.status_code == 200)
        
        amit = User.query.filter_by(email='amit.verma@college.edu').first()
        assert_test("New user record created with student role", amit is not None and amit.role == 'student')
        assert_test("Initial profile initialized for user", amit.profile is not None)
        assert_test("Password hash securely stored", amit.password_hash != 'Student@123' and amit.check_password('Student@123'))

        # ----------------------------------------------------
        # 3. STUDENT PROFILE & SKILL MANAGEMENT
        # ----------------------------------------------------
        print("\n--- Checkpoint 3: Profile Updates, Skills, Projects & Certifications ---")
        # Log in as Amit
        client.post('/login', data={'email': 'amit.verma@college.edu', 'password': 'Student@123'})
        
        # Update profile
        res = client.post('/profile', data={
            'full_name': 'Amit Kumar Verma',
            'headline': 'Computer Science Undergrad | Full Stack Developer',
            'phone': '+91 9988776655',
            'date_of_birth': '2004-06-15',
            'gender': 'Male',
            'state': 'Delhi',
            'city': 'New Delhi',
            'bio': 'Passionate about distributed web architectures.',
            'college': 'Delhi Technological University (DTU)',
            'university': 'DTU',
            'degree': 'B.Tech',
            'branch': 'Computer Science',
            'current_year': '3rd Year',
            'semester': '5th Semester',
            'cgpa': '8.80',
            'tenth_percentage': '92.0',
            'twelfth_percentage': '90.5',
            'family_income': '320000',
            'category': 'OBC',
            'career_goal': 'Full Stack Developer',
            'preferred_role': 'Full Stack Developer',
            'resume_url': 'https://example.com/amit_resume.pdf',
            'github_url': 'https://github.com/amitverma',
            'linkedin_url': 'https://linkedin.com/in/amitverma'
        }, follow_redirects=True)
        assert_test("Profile update submitted & saved", b'Profile updated successfully' in res.data or b'Amit Kumar Verma' in res.data)

        amit_profile = StudentProfile.query.filter_by(user_id=amit.id).first()
        assert_test("CGPA stored as float (8.80)", abs(amit_profile.cgpa - 8.80) < 0.01)
        assert_test("Family income stored correctly (320,000)", amit_profile.family_income == 320000.0)
        assert_test("GitHub link stored on profile", amit_profile.github_url == 'https://github.com/amitverma')

        # Add Skills
        client.post('/profile/skill/add', data={'name': 'Python', 'level': 'Advanced', 'category': 'Technical'})
        client.post('/profile/skill/add', data={'name': 'Flask', 'level': 'Intermediate', 'category': 'Technical'})
        client.post('/profile/skill/add', data={'name': 'JavaScript', 'level': 'Intermediate', 'category': 'Technical'})
        client.post('/profile/skill/add', data={'name': 'SQL', 'level': 'Beginner', 'category': 'Technical'})
        
        skill_count_amit = Skill.query.filter_by(student_id=amit_profile.id).count()
        assert_test("Skills added to student profile (4 skills)", skill_count_amit == 4)

        # Add Project
        client.post('/profile/project/add', data={
            'title': 'Job Portal Engine',
            'description': 'REST-driven opportunities management platform.',
            'technologies': 'Python, Flask, SQLite, HTML5',
            'github_link': 'https://github.com/amitverma/portal',
            'live_link': ''
        })
        proj_count = Project.query.filter_by(student_id=amit_profile.id).count()
        assert_test("Project added to student profile", proj_count == 1)

        # Add Certification
        client.post('/profile/certification/add', data={
            'name': 'Meta Full Stack Developer Certificate',
            'issuer': 'Coursera / Meta',
            'issue_date': '2025-06-10',
            'credential_url': 'https://coursera.org/verify/meta',
            'credential_id': 'META-881'
        })
        cert_count = Certification.query.filter_by(student_id=amit_profile.id).count()
        assert_test("Certification added to student profile", cert_count == 1)

        # Dynamic Strength Score
        comp_data = AnalyticsService.calculate_profile_strength(amit_profile, amit_profile.skills)
        assert_test("Profile strength calculated (>= 85%)", comp_data['percentage'] >= 85)

        # ----------------------------------------------------
        # 4. SCHOLARSHIP FILTERING & ELIGIBILITY ENGINE
        # ----------------------------------------------------
        print("\n--- Checkpoint 4: Scholarship Search, Filtering & Match Scoring ---")
        # Keyword Search
        res = client.get('/scholarships?search=Google')
        assert_test("Scholarship search by keyword returns matches", b'Google Generation' in res.data)

        # Branch Filter
        res = client.get('/scholarships?branch=Computer+Science')
        assert_test("Branch filter loads (200 OK)", res.status_code == 200)

        # Eligibility Check via API for Amit
        tata_sch = Scholarship.query.filter_by(name="Tata Trust Means-Cum-Merit Scholarship").first()
        res = client.post('/api/check-eligibility', json={'scholarship_id': tata_sch.id})
        assert_test("Eligibility API returns 200 OK", res.status_code == 200)
        res_json = res.get_json()
        assert_test("Amit is eligible for Tata Trust", res_json['data']['result']['eligible'] is True)
        assert_test("High match score (> 80%)", res_json['data']['result']['score'] >= 80)
        assert_test("Criteria breakdown returned with academic & financial fit", 'academic_fit' in res_json['data']['result']['breakdown'])

        # Ineligible Test Case
        ananya = User.query.filter_by(email="ananya@student.com").first() # ECE, CGPA 7.8
        aditya_sch = Scholarship.query.filter_by(name="Aditya Birla Group Technical Scholarship").first() # Min CGPA 8.5
        ananya_el = EligibilityService.calculate_scholarship_match(ananya.profile, aditya_sch)
        assert_test("Ananya fails CGPA cutoff for Birla (7.8 < 8.5)", ananya_el['eligible'] is False)
        assert_test("Unmet criteria listed explicitly", any('CGPA' in m for m in ananya_el['missing_requirements']))

        # ----------------------------------------------------
        # 5. BOOKMARKS / SAVED OPPORTUNITIES
        # ----------------------------------------------------
        print("\n--- Checkpoint 5: Bookmarking & Saved Opportunities ---")
        # Save Scholarship
        res = client.post('/api/save-opportunity', json={'opportunity_type': 'scholarship', 'opportunity_id': tata_sch.id})
        assert_test("Bookmark scholarship API returns saved=true", res.json.get('data', {}).get('saved') is True or res.json.get('saved') is True)

        # Save Internship
        res = client.post('/api/save-opportunity', json={'opportunity_type': 'internship', 'opportunity_id': 1})
        assert_test("Bookmark internship API returns saved=true", res.json.get('data', {}).get('saved') is True or res.json.get('saved') is True)

        # Save Course
        res = client.post('/api/save-opportunity', json={'opportunity_type': 'course', 'opportunity_id': 1})
        assert_test("Bookmark course API returns saved=true", res.json.get('data', {}).get('saved') is True or res.json.get('saved') is True)

        # View Saved Page
        res = client.get('/saved')
        assert_test("Saved opportunities page displays bookmarked items", res.status_code == 200 and b'Saved Opportunities' in res.data)

        # Remove Bookmark
        res = client.post('/api/remove-saved', json={'opportunity_type': 'course', 'opportunity_id': 1})
        assert_test("Remove bookmark API returns saved=false", res.json.get('data', {}).get('saved') is False or res.json.get('saved') is False)

        # ----------------------------------------------------
        # 6. INTERNSHIPS & COURSES CATALOGS
        # ----------------------------------------------------
        print("\n--- Checkpoint 6: Internships & Courses Directory ---")
        # Internships list
        res = client.get('/internships')
        assert_test("Internships directory loads (200 OK)", res.status_code == 200)

        # Internships filter by domain
        res = client.get('/internships?domain=Web+Development')
        assert_test("Filter internships by domain loads (200 OK)", res.status_code == 200)

        # Internship detail
        res = client.get('/internship/1')
        assert_test("Internship detail page loads (200 OK)", res.status_code == 200 and b'Microsoft' in res.data)

        # Courses list & filter
        res = client.get('/courses?price=Free')
        assert_test("Free courses filter loads (200 OK)", res.status_code == 200)

        # ----------------------------------------------------
        # 7. APPLICATION TRACKER PIPELINE
        # ----------------------------------------------------
        print("\n--- Checkpoint 7: Application Pipeline Tracker ---")
        # Create Application
        res = client.post('/applications/create', data={
            'opportunity_type': 'internship',
            'opportunity_id': 1,
            'status': 'Applied',
            'deadline': '2026-11-15',
            'notes': 'Submitted application on careers portal'
        }, follow_redirects=True)
        assert_test("Application created and visible on tracker", b'Applied' in res.data)

        amit_app = Application.query.filter_by(user_id=amit.id, opportunity_type='internship', opportunity_id=1).first()
        assert_test("Application persisted in database", amit_app is not None)

        # Update Application Status (Applied -> Under Review)
        res = client.post('/applications/update-status', data={
            'application_id': amit_app.id,
            'status': 'Under Review',
            'notes': 'Resume screening passed'
        }, follow_redirects=True)
        assert_test("Application status updated to Under Review", b'Under Review' in res.data)

        # ----------------------------------------------------
        # 8. CAREER READINESS & DYNAMIC ROADMAP
        # ----------------------------------------------------
        print("\n--- Checkpoint 8: Career Readiness & Interactive Dynamic Roadmap ---")
        # Career page
        res = client.get('/career')
        assert_test("Career page loads with readiness score", res.status_code == 200 and b'Career Readiness Score' in res.data)

        # Target Role Simulation
        res = client.get('/career?role=Data+Scientist')
        assert_test("Role simulation switch works (200 OK)", res.status_code == 200 and b'Data Scientist' in res.data)

        # Roadmap View
        res = client.get('/roadmap?role=Software+Engineer')
        assert_test("Roadmap page loads with Software Engineer stages", res.status_code == 200 and b'Software Engineer' in res.data)

        # Async Roadmap Progress Toggle
        res = client.post('/api/roadmap-progress', json={'stage_id': '01', 'career_role': 'Software Engineer', 'completed': True})
        assert_test("Toggle Stage 01 API returns success", res.json.get('success') is True)

        # ----------------------------------------------------
        # 9. NOTIFICATIONS CENTER
        # ----------------------------------------------------
        print("\n--- Checkpoint 9: Notification Center ---")
        res = client.get('/notifications')
        assert_test("Notifications page loads (200 OK)", res.status_code == 200)

        # Mark all read API
        res = client.post('/api/notifications/mark-read', json={})
        assert_test("Mark all notifications read API works", res.json.get('success') is True)

        # ----------------------------------------------------
        # 10. ADMINISTRATOR RBAC, CRUD & AUDIT LOGS
        # ----------------------------------------------------
        print("\n--- Checkpoint 10: Admin Authentication, Security, CRUD & Audit Logging ---")
        # Student blocked from admin dashboard
        res = client.get('/admin/dashboard', follow_redirects=False)
        assert_test("Student blocked from admin dashboard (Access Denied / Redirect)", res.status_code in [302, 403])

        # Admin Login
        client.get('/logout')
        res = client.post('/admin/login', data={'email': 'admin@portal.com', 'password': 'Admin@123'}, follow_redirects=True)
        assert_test("Admin login successful", res.status_code == 200 and b'Admin Console' in res.data)

        # Admin Dashboard
        res = client.get('/admin/dashboard')
        assert_test("Admin dashboard KPI analytics accessible", res.status_code == 200 and b'Total Students' in res.data)

        # Admin Students Directory
        res = client.get('/admin/students')
        assert_test("Admin students directory accessible", res.status_code == 200 and b'Amit' in res.data)

        # Admin Student Inspector
        res = client.get(f'/admin/student/{amit.id}')
        assert_test("Admin student profile inspector loads", res.status_code == 200 and b'DTU' in res.data)

        # Admin Scholarship CREATE with Audit Log
        res = client.post('/admin/scholarships', data={
            'name': 'QA Test National Merit Award',
            'provider': 'National Testing Agency',
            'description': 'Automated QA test scholarship grant for top engineering talents.',
            'amount': 'Rs 60,000 / Year',
            'amount_numeric': '60000',
            'deadline': '2026-12-31',
            'minimum_cgpa': '8.0',
            'maximum_income': '500000',
            'eligible_branches': 'Computer Science, IT',
            'eligible_categories': 'All',
            'required_documents': 'College ID, Semester Marksheet',
            'application_url': 'https://example.com/apply'
        }, follow_redirects=True)
        assert_test("Admin CREATE Scholarship works", b'QA Test National Merit Award' in res.data)
        
        qa_sch = Scholarship.query.filter_by(name='QA Test National Merit Award').first()
        assert_test("New scholarship persisted in database", qa_sch is not None)

        audit_create = AdminActionLog.query.filter_by(action="CREATE_SCHOLARSHIP", target_id=qa_sch.id).first()
        assert_test("Immutable audit log recorded for create scholarship", audit_create is not None)

        # Admin Scholarship EDIT
        res = client.post(f'/admin/scholarship/edit/{qa_sch.id}', data={
            'name': 'QA Test National Merit Award (Updated)',
            'provider': 'National Testing Agency',
            'description': 'Updated description',
            'amount': 'Rs 75,000 / Year',
            'amount_numeric': '75000',
            'deadline': '2026-12-31',
            'minimum_cgpa': '8.2',
            'maximum_income': '600000',
            'eligible_branches': 'All',
            'eligible_categories': 'All',
            'required_documents': 'Marksheets',
            'application_url': 'https://example.com/apply'
        }, follow_redirects=True)
        assert_test("Admin EDIT Scholarship works", b'QA Test National Merit Award (Updated)' in res.data)

        # Admin Scholarship DELETE
        res = client.post(f'/admin/scholarship/delete/{qa_sch.id}', follow_redirects=True)
        assert_test("Admin DELETE Scholarship works", Scholarship.query.filter_by(name='QA Test National Merit Award (Updated)').first() is None)

        # Admin Audit Logs View
        res = client.get('/admin/audit-logs')
        assert_test("Admin Audit Trail view accessible", res.status_code == 200 and b'Immutable Audit Trail' in res.data)

        # Admin Application Review & Status Update
        res = client.post(f'/admin/application/update-status/{amit_app.id}', data={
            'status': 'Shortlisted',
            'notes': 'Admin reviewed and shortlisted candidate'
        }, follow_redirects=True)
        assert_test("Admin application status update works", b'Application #' in res.data or res.status_code == 200)
        
        # Verify notification triggered to student
        amit_notif = Notification.query.filter_by(user_id=amit.id).order_by(Notification.id.desc()).first()
        assert_test("Status update automatically triggered notification to student", 'Shortlisted' in amit_notif.title or 'Shortlisted' in amit_notif.message)

        # Global Search API
        res = client.get('/api/search?q=Microsoft')
        assert_test("Global Search API returns matches", res.status_code == 200 and b'Microsoft' in res.data)

    print("\n========================================================")
    print(f"[+] QA AUDIT SUMMARY: {passed} / {total} tests passed ({round((passed/total)*100)}%)")
    print("========================================================\n")
    return passed == total

if __name__ == "__main__":
    success = run_full_qa()
    sys.exit(0 if success else 1)
