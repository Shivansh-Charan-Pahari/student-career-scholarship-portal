"""
Unit Tests for Scholarship Eligibility & Matching Algorithm
"""

import unittest
from services.eligibility_service import EligibilityService, BRANCH_SYNONYMS
from models import StudentProfile, Scholarship

class TestEligibilityEngine(unittest.TestCase):
    def setUp(self):
        # Sample Student Profile
        self.eligible_student = StudentProfile(
            full_name="Karan Verma",
            branch="Computer Science",
            degree="B.Tech",
            cgpa=8.80,
            family_income=300000.0,
            category="OBC",
            preferred_role="Full Stack Developer",
            career_goal="Full Stack Developer",
            resume_url="https://example.com/karan_resume.pdf"
        )

        self.ineligible_cgpa_student = StudentProfile(
            full_name="Alok Nath",
            branch="Computer Science",
            cgpa=6.40,
            family_income=250000.0,
            category="General"
        )

        self.ineligible_income_student = StudentProfile(
            full_name="Meera Iyer",
            branch="Information Technology",
            cgpa=9.10,
            family_income=750000.0,
            category="General"
        )

        self.ineligible_branch_student = StudentProfile(
            full_name="Siddharth Rao",
            branch="Civil Engineering",
            cgpa=8.90,
            family_income=200000.0,
            category="General"
        )

        # Sample Scholarships
        self.merit_grant = Scholarship(
            name="National Technology Merit Grant",
            provider="Tech Foundation",
            description="Excellence award for high-performing engineering students in Computer Science and IT.",
            amount="₹60,000 / Year",
            minimum_cgpa=7.5,
            maximum_income=400000.0,
            eligible_branches="Computer Science, Information Technology, AI & ML",
            eligible_categories="All"
        )

        self.need_based_grant = Scholarship(
            name="Economic Empowerment Aid",
            provider="Welfare Society",
            description="Need-based grant for low income families.",
            amount="₹30,000 / Year",
            minimum_cgpa=6.0,
            maximum_income=300000.0,
            eligible_branches="All",
            eligible_categories="SC, ST, OBC, EWS"
        )

    def test_eligible_student_match(self):
        result = EligibilityService.calculate_scholarship_match(self.eligible_student, self.merit_grant)
        self.assertTrue(result['eligible'])
        self.assertGreaterEqual(result['score'], 80)
        self.assertEqual(len(result['missing_requirements']), 0)
        self.assertIn('academic_fit', result['breakdown'])
        self.assertIn('branch_fit', result['breakdown'])

    def test_cgpa_cutoff_failure(self):
        result = EligibilityService.calculate_scholarship_match(self.ineligible_cgpa_student, self.merit_grant)
        self.assertFalse(result['eligible'])
        self.assertLessEqual(result['score'], 52) # Capped when ineligible
        self.assertTrue(any('CGPA' in m for m in result['missing_requirements']))

    def test_income_ceiling_failure(self):
        result = EligibilityService.calculate_scholarship_match(self.ineligible_income_student, self.merit_grant)
        self.assertFalse(result['eligible'])
        self.assertTrue(any('income' in m.lower() for m in result['missing_requirements']))

    def test_branch_ineligibility(self):
        result = EligibilityService.calculate_scholarship_match(self.ineligible_branch_student, self.merit_grant)
        self.assertFalse(result['eligible'])
        self.assertTrue(any('branch' in m.lower() for m in result['missing_requirements']))

    def test_branch_synonym_normalization(self):
        match_cse, _ = EligibilityService.normalize_branch_match("CSE", "Computer Science, IT")
        self.assertTrue(match_cse)

        match_ai, _ = EligibilityService.normalize_branch_match("Artificial Intelligence & ML", "Computer Science")
        self.assertTrue(match_ai)

        match_ece, _ = EligibilityService.normalize_branch_match("Electronics & Communication", "ECE, VLSI")
        self.assertTrue(match_ece)

        match_false, _ = EligibilityService.normalize_branch_match("Mechanical Engineering", "Computer Science, IT")
        self.assertFalse(match_false)

    def test_missing_profile_handling(self):
        result = EligibilityService.calculate_scholarship_match(None, self.merit_grant)
        self.assertFalse(result['eligible'])
        self.assertEqual(result['score'], 0)
        self.assertIn('missing_requirements', result)

if __name__ == '__main__':
    unittest.main()
