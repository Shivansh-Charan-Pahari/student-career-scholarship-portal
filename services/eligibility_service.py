"""
Scholarship Eligibility & Explainable Matching Engine
Implements deterministic, multi-criteria decision algorithms for scholarship qualification.
Evaluates:
- Academic Fit (30%): CGPA thresholds & secondary school performance
- Financial Need Fit (25%): Family income brackets vs maximum ceiling
- Academic Branch Fit (20%): Normalized discipline synonym mappings (CSE, IT, ECE, EEE, Mech, Civil)
- Social Category Fit (10%): Reservation and affirmative category matching
- Career Alignment (10%): Match between scholarship focus and student career aspirations
- Application Feasibility (5%): Document readiness and profile completeness
"""

from models import StudentProfile, Scholarship

BRANCH_SYNONYMS = {
    'cse': ['cs', 'cse', 'computer science', 'computer engineering', 'software', 'software engineering', 'information technology', 'it', 'bca', 'mca', 'data science', 'artificial intelligence', 'ai', 'ai & ml', 'machine learning'],
    'it': ['it', 'information technology', 'computer science', 'cs', 'cse', 'software'],
    'ece': ['ece', 'electronics', 'electronics & communication', 'communication', 'telecommunication', 'vlsi', 'embedded systems', 'iot'],
    'eee': ['eee', 'electrical', 'electrical & electronics', 'power engineering', 'energy engineering'],
    'mech': ['mech', 'mechanical', 'mechanical engineering', 'automobile', 'automotive', 'mechatronics', 'robotics', 'production'],
    'civil': ['civil', 'civil engineering', 'structural', 'construction', 'infrastructure', 'environmental']
}

class EligibilityService:
    @staticmethod
    def normalize_branch_match(student_branch: str, eligible_branches_raw: str) -> tuple[bool, str]:
        """
        Determines whether student's branch matches the scholarship's eligible branches
        using synonym graph lookup and substring normalization.
        """
        if not eligible_branches_raw or eligible_branches_raw.strip().lower() in ['all', 'any', 'all branches', 'open to all']:
            return True, "Open to students from all academic disciplines."

        s_branch = (student_branch or '').strip().lower()
        if not s_branch:
            return False, "Student branch is not specified on profile."

        allowed_list = [b.strip().lower() for b in eligible_branches_raw.split(',') if b.strip()]

        # 1. Direct or substring match
        for allowed in allowed_list:
            if s_branch in allowed or allowed in s_branch:
                return True, f"Branch '{student_branch}' directly matches criteria [{eligible_branches_raw}]."

        # 2. Synonym graph match
        for key, aliases in BRANCH_SYNONYMS.items():
            student_in_group = any(alias in s_branch for alias in aliases)
            if student_in_group:
                for allowed in allowed_list:
                    if any(alias in allowed for alias in aliases):
                        return True, f"Branch '{student_branch}' qualifies under discipline cluster '{key.upper()}' [{eligible_branches_raw}]."

        return False, f"Scholarship is restricted to [{eligible_branches_raw}]. Your branch is '{student_branch}'."

    @staticmethod
    def calculate_scholarship_match(profile: StudentProfile | None, scholarship: Scholarship) -> dict:
        """
        Deterministic, explainable scoring algorithm.
        Returns:
        {
            'eligible': bool,
            'score': int (0-100),
            'reasons': list[str],
            'missing_requirements': list[str],
            'breakdown': dict,
            'explanation_summary': str
        }
        """
        if not profile:
            return {
                'eligible': False,
                'score': 0,
                'reasons': ["Student profile has not been created yet."],
                'missing_requirements': ["Please complete your academic profile to determine eligibility."],
                'breakdown': {
                    'academic_fit': 0,
                    'financial_fit': 0,
                    'branch_fit': 0,
                    'category_fit': 0,
                    'career_alignment': 0,
                    'feasibility': 0
                },
                'explanation_summary': "Incomplete Profile: Unable to evaluate eligibility without student records."
            }

        reasons = []
        missing_requirements = []
        is_eligible = True

        # -------------------------------------------------------------
        # 1. Academic Fit (Weight: 30%)
        # -------------------------------------------------------------
        academic_score = 0.0
        student_cgpa = float(profile.cgpa or 0.0)
        min_cgpa = float(scholarship.minimum_cgpa or 0.0)

        if min_cgpa > 0:
            if student_cgpa >= min_cgpa:
                # Scaled: full 30 pts for meeting or exceeding cutoff
                ratio = min(1.0, student_cgpa / 10.0)
                academic_score = 25.0 + (5.0 * ratio)
                reasons.append(f"CGPA Cutoff Met: Required ≥ {min_cgpa:.1f} | Your CGPA: {student_cgpa:.2f}")
            else:
                is_eligible = False
                academic_score = max(0.0, 15.0 * (student_cgpa / min_cgpa))
                reasons.append(f"CGPA Cutoff Not Met: Required ≥ {min_cgpa:.1f} | Your CGPA: {student_cgpa:.2f}")
                missing_requirements.append(f"Minimum CGPA of {min_cgpa:.1f} required (You have {student_cgpa:.2f})")
        else:
            academic_score = 30.0 * (student_cgpa / 10.0 if student_cgpa > 0 else 0.8)
            reasons.append(f"No minimum CGPA required. (Your CGPA: {student_cgpa:.2f})")

        # -------------------------------------------------------------
        # 2. Financial Need Fit (Weight: 25%)
        # -------------------------------------------------------------
        financial_score = 0.0
        student_income = float(profile.family_income or 0.0)
        max_income = float(scholarship.maximum_income or 0.0)

        if max_income > 0:
            if student_income <= max_income and student_income > 0:
                financial_score = 25.0
                reasons.append(f"Income Limit Met: Income ceiling is ₹{max_income:,.0f} | Your Family Income: ₹{student_income:,.0f}")
            elif student_income == 0:
                financial_score = 20.0
                reasons.append(f"Income Limit Cap: ₹{max_income:,.0f} | Family income not entered on profile")
            else:
                is_eligible = False
                financial_score = 0.0
                reasons.append(f"Income Ceiling Exceeded: Maximum allowed ₹{max_income:,.0f} | Your Family Income: ₹{student_income:,.0f}")
                missing_requirements.append(f"Annual family income must be ≤ ₹{max_income:,.0f} (Your profile indicates ₹{student_income:,.0f})")
        else:
            financial_score = 25.0
            reasons.append("Open to all income brackets (Merit / Universal grant).")

        # -------------------------------------------------------------
        # 3. Branch Fit (Weight: 20%)
        # -------------------------------------------------------------
        branch_score = 0.0
        eligible_branches_raw = scholarship.eligible_branches or 'All'
        student_branch = profile.branch or ''

        branch_matches, branch_reason = EligibilityService.normalize_branch_match(student_branch, eligible_branches_raw)
        if branch_matches:
            branch_score = 20.0
            reasons.append(branch_reason)
        else:
            is_eligible = False
            branch_score = 0.0
            reasons.append(branch_reason)
            missing_requirements.append(f"Eligible Academic Branches: {eligible_branches_raw}")

        # -------------------------------------------------------------
        # 4. Social Category Fit (Weight: 10%)
        # -------------------------------------------------------------
        category_score = 0.0
        eligible_cats_raw = (scholarship.eligible_categories or 'All').strip()
        student_cat = (profile.category or 'General').strip()

        if eligible_cats_raw.lower() in ['all', 'any', 'open to all', '']:
            category_score = 10.0
            reasons.append("Social Category: Open to candidates from all categories.")
        else:
            allowed_cats = [c.strip().lower() for c in eligible_cats_raw.split(',') if c.strip()]
            if student_cat.lower() in allowed_cats:
                category_score = 10.0
                reasons.append(f"Social Category Eligible: '{student_cat}' is eligible for [{eligible_cats_raw}].")
            else:
                is_eligible = False
                category_score = 0.0
                reasons.append(f"Category Restriction: Restricted to [{eligible_cats_raw}]. Your profile category is '{student_cat}'.")
                missing_requirements.append(f"Target Social Category: {eligible_cats_raw}")

        # -------------------------------------------------------------
        # 5. Career & Domain Alignment (Weight: 10%)
        # -------------------------------------------------------------
        career_score = 0.0
        target_role = (profile.preferred_role or profile.career_goal or '').lower()
        sch_text = f"{scholarship.name} {scholarship.description} {scholarship.provider}".lower()

        if target_role and (target_role in sch_text or any(w in sch_text for w in target_role.split() if len(w) > 3)):
            career_score = 10.0
            reasons.append(f"Career Alignment: Scholarship focus strongly aligns with your goal '{profile.preferred_role or profile.career_goal}'.")
        else:
            career_score = 6.0

        # -------------------------------------------------------------
        # 6. Application Feasibility & Documents (Weight: 5%)
        # -------------------------------------------------------------
        feasibility_score = 5.0
        if profile.resume_url:
            reasons.append("Application Readiness: Resume link is active on your profile.")
        else:
            feasibility_score = 3.0

        # -------------------------------------------------------------
        # Compute Weighted Match Score
        # -------------------------------------------------------------
        total_score = round(academic_score + financial_score + branch_score + category_score + career_score + feasibility_score)
        total_score = max(5, min(100, total_score))

        # Ineligible cap to prevent misleading student with high score when failing a hard filter
        if not is_eligible and total_score > 52:
            total_score = 50

        # Summary text
        if is_eligible:
            explanation_summary = f"Eligible: You satisfy all academic, financial, branch, and category criteria for this scholarship with a {total_score}% overall compatibility score."
        else:
            explanation_summary = f"Not Eligible: You currently miss {len(missing_requirements)} prerequisite criteria ({', '.join(missing_requirements[:2])})."

        return {
            'eligible': is_eligible,
            'score': total_score,
            'reasons': reasons,
            'missing_requirements': missing_requirements,
            'breakdown': {
                'academic_fit': round(academic_score, 1),
                'financial_fit': round(financial_score, 1),
                'branch_fit': round(branch_score, 1),
                'category_fit': round(category_score, 1),
                'career_alignment': round(career_score, 1),
                'feasibility': round(feasibility_score, 1)
            },
            'explanation_summary': explanation_summary
        }
