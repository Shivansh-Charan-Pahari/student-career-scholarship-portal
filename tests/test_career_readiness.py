"""
Unit Tests for Career Readiness & Skill Gap Analyzer
"""

import unittest
from services.career_service import CareerService, CAREER_ROLE_REQUIREMENTS, ROADMAP_DEFINITIONS
from models import StudentProfile, Skill, Project, Certification

class TestCareerReadiness(unittest.TestCase):
    def setUp(self):
        self.profile = StudentProfile(
            full_name="Pooja Jain",
            degree="B.Tech",
            branch="Computer Science",
            cgpa=8.90,
            career_goal="Full Stack Developer",
            preferred_role="Full Stack Developer",
            resume_url="https://example.com/pooja.pdf",
            github_url="https://github.com/poojajain",
            bio="Passionate web developer"
        )
        self.profile.projects = [
            Project(title="E-Commerce Store", description="Full stack app", technologies="Python, Flask, SQL"),
            Project(title="Kanban Board", description="Task manager", technologies="JavaScript, HTML, CSS")
        ]
        self.profile.certifications = [
            Certification(name="Full Stack Spec", issuer="Coursera")
        ]
        self.skills = [
            Skill(name="HTML", level="Advanced"),
            Skill(name="CSS", level="Advanced"),
            Skill(name="JavaScript", level="Intermediate"),
            Skill(name="Python", level="Advanced"),
            Skill(name="Flask", level="Intermediate"),
            Skill(name="SQL", level="Intermediate"),
            Skill(name="Git", level="Intermediate"),
            Skill(name="DSA", level="Intermediate")
        ]

    def test_full_stack_readiness_calculation(self):
        readiness = CareerService.calculate_career_readiness(self.profile, self.skills)
        self.assertEqual(readiness['target_role'], "Full Stack Developer")
        self.assertGreaterEqual(readiness['readiness_score'], 70)
        self.assertEqual(len(readiness['missing_skills']), 0)
        self.assertIn('dimensions', readiness)
        self.assertGreater(readiness['dimensions']['skills_score'], 20)

    def test_skill_gap_detection(self):
        # Student with only Python and SQL targeting Data Scientist
        data_profile = StudentProfile(
            full_name="Arjun Kapoor",
            preferred_role="Data Scientist",
            career_goal="Data Scientist",
            cgpa=8.0
        )
        data_skills = [
            Skill(name="Python", level="Intermediate"),
            Skill(name="SQL", level="Intermediate")
        ]
        readiness = CareerService.calculate_career_readiness(data_profile, data_skills)
        self.assertEqual(readiness['target_role'], "Data Scientist")
        self.assertIn("Machine Learning", readiness['missing_skills'])
        self.assertIn("Pandas", readiness['missing_skills'])
        self.assertIn("NumPy", readiness['missing_skills'])
        self.assertLess(readiness['readiness_score'], 60)

    def test_multi_role_roadmap_generation(self):
        roles_to_test = ["Software Engineer", "Full Stack Developer", "Data Scientist", "AI/ML Engineer", "Cloud & DevOps Engineer", "Cybersecurity Analyst", "Embedded Systems & IoT"]
        for role in roles_to_test:
            self.assertIn(role, ROADMAP_DEFINITIONS)
            stages = ROADMAP_DEFINITIONS[role]
            self.assertGreaterEqual(len(stages), 8)
            for stage in stages:
                self.assertIn('id', stage)
                self.assertIn('title', stage)
                self.assertIn('skills', stage)
                self.assertIn('category', stage)

if __name__ == '__main__':
    unittest.main()
