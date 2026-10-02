"""
Unified Opportunity Recommendation & Priority Action Engine
Calculates:
- Explainable Scholarship Recommendations (Match score & eligibility ranked)
- Weighted Internship Matching (Skill overlap, career goal & domain alignment)
- Skill Gap-Driven Course Recommendations
- Deadline Urgency & Prioritized Student Action Center
"""

from datetime import datetime, timezone
from models import db, User, Scholarship, Internship, Course, StudentProfile, Application, SavedOpportunity
from services.eligibility_service import EligibilityService
from services.career_service import CareerService

class RecommendationService:
    @staticmethod
    def get_unified_recommendations(user_id: int) -> dict:
        user = db.session.get(User, user_id)
        if not user or not user.profile:
            return {'scholarships': [], 'internships': [], 'courses': [], 'priorities': []}

        profile = user.profile
        skills = profile.skills or []
        student_skill_names = [s.name.strip().lower() for s in skills]

        # -------------------------------------------------------------
        # 1. Scholarship Recommendations (Ranked by Match Score & Eligibility)
        # -------------------------------------------------------------
        all_scholarships = Scholarship.query.filter_by(is_active=True).all()
        scored_scholarships = []

        for sch in all_scholarships:
            el_res = EligibilityService.calculate_scholarship_match(profile, sch)
            scored_scholarships.append({
                'scholarship': sch,
                'match_score': el_res['score'],
                'eligible': el_res['eligible'],
                'reasons': el_res['reasons'],
                'missing_requirements': el_res['missing_requirements'],
                'breakdown': el_res['breakdown'],
                'explanation': el_res['explanation_summary']
            })

        # Sort: eligible first, then match score descending
        scored_scholarships.sort(key=lambda x: (x['eligible'], x['match_score']), reverse=True)
        top_scholarships = scored_scholarships[:5]

        # -------------------------------------------------------------
        # 2. Internship Recommendations (Weighted Skill & Domain Matching)
        # -------------------------------------------------------------
        all_internships = Internship.query.filter_by(is_active=True).all()
        scored_internships = []

        target_domain = (profile.preferred_role or profile.career_goal or '').lower()

        for intern in all_internships:
            score = 45 # Base baseline
            intern_skills = [s.strip().lower() for s in intern.required_skills.split(',') if s.strip()]
            
            # Skill overlap (40 pts)
            matched_skills = []
            for req in intern_skills:
                if any(req in s or s in req for s in student_skill_names):
                    matched_skills.append(req.capitalize())

            if intern_skills:
                score += int((len(matched_skills) / len(intern_skills)) * 35)

            # Domain & Career Match (20 pts)
            if target_domain and (target_domain in intern.domain.lower() or intern.domain.lower() in target_domain):
                score += 20
            elif target_domain and any(w in intern.domain.lower() for w in target_domain.split()):
                score += 10

            final_intern_score = min(100, max(10, score))
            scored_internships.append({
                'internship': intern,
                'score': final_intern_score,
                'matched_skills': matched_skills,
                'total_skills_count': len(intern_skills),
                'match_explanation': f"{len(matched_skills)} of {len(intern_skills)} required skills match your profile ({', '.join(matched_skills) if matched_skills else 'Baseline match'})."
            })

        scored_internships.sort(key=lambda x: x['score'], reverse=True)
        top_internships = scored_internships[:5]

        # -------------------------------------------------------------
        # 3. Course Recommendations (Direct Skill Gap Remediation)
        # -------------------------------------------------------------
        career_readiness = CareerService.calculate_career_readiness(profile, skills)
        missing_skills = [m.lower() for m in career_readiness['missing_skills']]

        all_courses = Course.query.filter_by(is_active=True).all()
        scored_courses = []

        for course in all_courses:
            score = 40
            c_skill = course.skill.lower()

            # Addresses a direct missing skill gap? (45 pts bonus)
            is_gap_remedy = any(c_skill in m or m in c_skill for m in missing_skills)
            if is_gap_remedy:
                score += 45
                gap_reason = f"Directly teaches missing skill '{course.skill}' required for {career_readiness['target_role']}."
            elif any(c_skill in s or s in c_skill for s in student_skill_names):
                score += 20
                gap_reason = f"Enhances your existing proficiency in '{course.skill}'."
            else:
                gap_reason = f"Broadens your core knowledge in '{course.skill}'."

            # Rating bonus (15 pts)
            rating = float(course.rating or 4.5)
            score += int((rating / 5.0) * 15)

            scored_courses.append({
                'course': course,
                'score': min(100, score),
                'is_gap_remedy': is_gap_remedy,
                'reason': gap_reason
            })

        scored_courses.sort(key=lambda x: (x['is_gap_remedy'], x['score'], x['course'].rating), reverse=True)
        top_courses = scored_courses[:5]

        # -------------------------------------------------------------
        # 4. Priority Action Center (Actionable Recommendations)
        # -------------------------------------------------------------
        priorities = []

        # Action 1: Profile completion
        if not profile.cgpa or profile.cgpa == 0:
            priorities.append({
                'title': 'Add your College CGPA',
                'description': 'Entering your CGPA allows the engine to accurately qualify you for merit scholarships.',
                'priority': 'HIGH',
                'badge': 'Profile',
                'action_url': '/profile',
                'action_text': 'Update CGPA'
            })
        elif len(skills) < 3:
            priorities.append({
                'title': 'Add 3+ Technical Skills',
                'description': 'Adding your core programming tools unlocks personalized internship and course matches.',
                'priority': 'HIGH',
                'badge': 'Skills',
                'action_url': '/profile',
                'action_text': 'Add Skills'
            })

        # Action 2: Top eligible scholarship
        if top_scholarships and top_scholarships[0]['eligible']:
            best_sch = top_scholarships[0]['scholarship']
            priorities.append({
                'title': f"Apply for {best_sch.name}",
                'description': f"You meet 100% of the criteria for this {best_sch.amount} grant by {best_sch.provider}.",
                'priority': 'HIGH',
                'badge': 'Scholarship',
                'action_url': f"/scholarship/{best_sch.id}",
                'action_text': 'View Grant'
            })

        # Action 3: Top skill gap course
        if missing_skills and top_courses:
            best_course = top_courses[0]['course']
            priorities.append({
                'title': f"Learn {best_course.skill} for {career_readiness['target_role']}",
                'description': f"Target course on {best_course.platform} with a {best_course.rating}★ rating to bridge your skill gap.",
                'priority': 'MEDIUM',
                'badge': 'Course',
                'action_url': '/courses',
                'action_text': 'Explore Course'
            })

        # Action 4: Top internship match
        if top_internships and top_internships[0]['score'] >= 70:
            best_intern = top_internships[0]['internship']
            priorities.append({
                'title': f"Review {best_intern.title} at {best_intern.company}",
                'description': f"{top_internships[0]['score']}% profile alignment | Stipend: {best_intern.stipend}",
                'priority': 'MEDIUM',
                'badge': 'Internship',
                'action_url': f"/internship/{best_intern.id}",
                'action_text': 'View Role'
            })

        return {
            'scholarships': top_scholarships,
            'internships': top_internships,
            'courses': top_courses,
            'priorities': priorities[:4],
            'career_readiness': career_readiness
        }

    @staticmethod
    def get_upcoming_deadlines() -> list[dict]:
        """
        Categorizes deadlines into Due Today, Due Tomorrow, Due This Week, Due Soon.
        """
        deadlines = []
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        for sch in Scholarship.query.filter_by(is_active=True).all():
            if sch.deadline:
                deadlines.append({
                    'id': sch.id,
                    'title': sch.name,
                    'type': 'Scholarship',
                    'provider': sch.provider,
                    'deadline': sch.deadline,
                    'amount_or_stipend': sch.amount,
                    'url': f'/scholarship/{sch.id}',
                    'is_expired': sch.deadline < today
                })

        for intern in Internship.query.filter_by(is_active=True).all():
            if intern.deadline:
                deadlines.append({
                    'id': intern.id,
                    'title': f"{intern.title} ({intern.company})",
                    'type': 'Internship',
                    'provider': intern.company,
                    'deadline': intern.deadline,
                    'amount_or_stipend': intern.stipend,
                    'url': f'/internship/{intern.id}',
                    'is_expired': intern.deadline < today
                })

        # Filter out expired items and sort by deadline ascending
        active_deadlines = [d for d in deadlines if not d['is_expired']]
        active_deadlines.sort(key=lambda x: x['deadline'])
        return active_deadlines[:8]
