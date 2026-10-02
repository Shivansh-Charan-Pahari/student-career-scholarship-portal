"""
Analytics & Business Intelligence Engine
Computes:
- Real-time dynamic Student Profile Strength Meter (0-100%)
- Student Dashboard KPI statistics
- System-wide Admin Analytics (Application conversion pipeline, domain distributions, social categories)
"""

from models import db, User, StudentProfile, Skill, Project, Certification, Scholarship, Internship, Course, Application

class AnalyticsService:
    @staticmethod
    def calculate_profile_strength(profile: StudentProfile | None, skills: list | None = None) -> dict:
        """
        Calculates dynamic profile strength score (0-100%)
        Weights:
        - Personal Info: 15% (Full name, phone, dob/gender, state/city)
        - Academic Record: 25% (College, branch, degree, CGPA, 10th/12th)
        - Financial & Social: 15% (Family income, Category)
        - Technical Skills: 15% (1 skill: 8%, 3+ skills: 15%)
        - Projects Portfolio: 15% (1 project: 8%, 2+ projects: 15%)
        - Career & Resume: 15% (Career goal, preferred role, resume URL, GitHub)
        """
        if not profile:
            return {'percentage': 0, 'missing': ['Create your profile'], 'sections': {}}

        missing = []

        # 1. Personal (15%)
        personal_score = 0
        if profile.full_name:
            personal_score += 4
        else:
            missing.append("Add full name")

        if profile.phone:
            personal_score += 4
        else:
            missing.append("Add phone number")

        if profile.date_of_birth or profile.gender:
            personal_score += 4
        else:
            missing.append("Select date of birth / gender")

        if profile.state or profile.city:
            personal_score += 3
        else:
            missing.append("Add city and state")

        # 2. Academic (25%)
        academic_score = 0
        if profile.college or profile.university:
            academic_score += 8
        else:
            missing.append("Add college / university name")

        if profile.branch and profile.degree:
            academic_score += 7
        else:
            missing.append("Select branch & degree program")

        if profile.cgpa and profile.cgpa > 0:
            academic_score += 6
        else:
            missing.append("Enter current CGPA")

        if (profile.tenth_percentage and profile.tenth_percentage > 0) or (profile.twelfth_percentage and profile.twelfth_percentage > 0):
            academic_score += 4
        else:
            missing.append("Enter 10th / 12th percentages")

        # 3. Financial & Social (15%)
        financial_score = 0
        if profile.family_income and profile.family_income > 0:
            financial_score += 8
        else:
            missing.append("Enter annual family income")

        if profile.category:
            financial_score += 7
        else:
            missing.append("Specify social category")

        # 4. Technical Skills (15%)
        skills_list = skills if skills is not None else (profile.skills or [])
        skills_count = len(skills_list)
        if skills_count >= 3:
            skills_score = 15
        elif skills_count >= 1:
            skills_score = 8
            missing.append("Add at least 3 skills to achieve full skill score")
        else:
            skills_score = 0
            missing.append("Add your technical skills")

        # 5. Projects Portfolio (15%)
        projects = profile.projects or []
        projects_count = len(projects)
        if projects_count >= 2:
            projects_score = 15
        elif projects_count == 1:
            projects_score = 8
            missing.append("Add a second project to maximize portfolio score")
        else:
            projects_score = 0
            missing.append("Add capstone projects to your portfolio")

        # 6. Career & Resume (15%)
        career_score = 0
        if profile.career_goal:
            career_score += 4
        else:
            missing.append("Set your career goal")

        if profile.preferred_role:
            career_score += 4
        else:
            missing.append("Specify preferred industry role")

        if profile.resume_url:
            career_score += 4
        else:
            missing.append("Attach your online resume link")

        if profile.github_url or profile.linkedin_url:
            career_score += 3
        else:
            missing.append("Add your GitHub or LinkedIn profile")

        total = min(100, personal_score + academic_score + financial_score + skills_score + projects_score + career_score)

        return {
            'percentage': total,
            'missing': missing,
            'sections': {
                'personal': personal_score,
                'academic': academic_score,
                'financial': financial_score,
                'skills': skills_score,
                'projects': projects_score,
                'career': career_score
            }
        }

    @staticmethod
    def get_admin_dashboard_metrics() -> dict:
        total_students = User.query.filter_by(role='student').count()
        total_scholarships = Scholarship.query.filter_by(is_active=True).count()
        total_internships = Internship.query.filter_by(is_active=True).count()
        total_courses = Course.query.filter_by(is_active=True).count()
        total_applications = Application.query.count()

        # Status breakdown
        all_apps = Application.query.all()
        status_counts = {
            'Applied': 0,
            'Under Review': 0,
            'Shortlisted': 0,
            'Interview': 0,
            'Accepted': 0,
            'Rejected': 0,
            'Saved': 0
        }
        for a in all_apps:
            if a.status in status_counts:
                status_counts[a.status] += 1
            else:
                status_counts['Applied'] += 1

        # Domain breakdown for Internships
        domain_counts = {}
        for intern in Internship.query.all():
            domain_counts[intern.domain] = domain_counts.get(intern.domain, 0) + 1

        # Platform breakdown for Courses
        platform_counts = {}
        for c in Course.query.all():
            platform_counts[c.platform] = platform_counts.get(c.platform, 0) + 1

        # Social Category breakdown for Students
        cat_counts = {}
        for p in StudentProfile.query.all():
            cat = p.category or 'General'
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        # Popular Student Skills
        skills = Skill.query.all()
        skill_popularity = {}
        for s in skills:
            skill_popularity[s.name] = skill_popularity.get(s.name, 0) + 1
        top_skills = sorted(skill_popularity.items(), key=lambda x: x[1], reverse=True)[:6]

        # Recent applications
        recent_apps = Application.query.order_by(Application.created_at.desc()).limit(10).all()

        return {
            'kpis': {
                'total_students': total_students,
                'total_scholarships': total_scholarships,
                'total_internships': total_internships,
                'total_courses': total_courses,
                'total_applications': total_applications
            },
            'status_counts': status_counts,
            'domain_counts': domain_counts,
            'platform_counts': platform_counts,
            'cat_counts': cat_counts,
            'top_skills': top_skills,
            'recent_applications': recent_apps
        }
