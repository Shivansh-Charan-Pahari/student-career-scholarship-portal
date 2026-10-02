"""
Production-Grade Database Seeder
Populates comprehensive demo data covering:
- 1 System Administrator (admin@portal.com / Admin@123)
- 6 Diverse Student Personas with academic profiles, skills, projects, certifications, & career goals
- 16 Realistic Scholarships with multi-dimensional criteria
- 16 Industry Internships across major domains
- 16 High-Quality Courses (Free & Paid)
- 20+ Sample Applications spanning pipeline workflows
- Bookmarks, Priority Notifications, Roadmap Progress, and Admin Action Logs
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from app import create_app
from models import (
    db, User, StudentProfile, Skill, Project, Certification,
    Scholarship, Internship, Course, Application, SavedOpportunity,
    Notification, RoadmapProgress, AdminActionLog
)

def seed_database(app_instance=None, reset=True):
    target_app = app_instance or create_app()
    with target_app.app_context():
        if reset:
            print("[*] Resetting database tables...")
            db.drop_all()
            db.create_all()
        else:
            db.create_all()
            if Scholarship.query.count() > 0:
                print("[+] Database already contains records. Skipping destructive seed.")
                return

        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@portal.com')
        admin_password = os.environ.get('ADMIN_INITIAL_PASSWORD', 'Admin@123')

        print(f"[*] Seeding Administrator Account ({admin_email})...")
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                name="System Administrator",
                email=admin_email,
                role="admin",
                is_active=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.flush()

        print("[*] Seeding 6 Diverse Student Personas...")
        students_config = [
            {
                "name": "Rahul Sharma",
                "email": "rahul@student.com",
                "password": "Student@123",
                "profile": {
                    "full_name": "Rahul Sharma",
                    "headline": "Aspiring Full Stack Engineer | Python & JavaScript Developer",
                    "phone": "+91 9876543210",
                    "date_of_birth": "2004-05-14",
                    "gender": "Male",
                    "state": "Maharashtra",
                    "city": "Pune",
                    "bio": "Third-year Computer Science student passionate about building scalable web applications and clean API architectures.",
                    "college": "Pune Institute of Computer Technology",
                    "university": "Savitribai Phule Pune University",
                    "degree": "B.Tech",
                    "branch": "Computer Science",
                    "current_year": "3rd Year",
                    "semester": "6th Semester",
                    "cgpa": 8.65,
                    "tenth_percentage": 91.5,
                    "twelfth_percentage": 88.0,
                    "family_income": 350000.0,
                    "category": "OBC",
                    "career_goal": "Full Stack Developer",
                    "preferred_role": "Full Stack Developer",
                    "resume_url": "https://example.com/resumes/rahul_sharma.pdf",
                    "github_url": "https://github.com/rahulsharma-dev",
                    "linkedin_url": "https://linkedin.com/in/rahulsharma-dev",
                    "portfolio_url": "https://rahulsharma.dev"
                },
                "skills": [
                    ("Python", "Advanced", "Technical"),
                    ("JavaScript", "Intermediate", "Technical"),
                    ("Flask", "Intermediate", "Technical"),
                    ("HTML5", "Advanced", "Technical"),
                    ("CSS3", "Advanced", "Technical"),
                    ("SQL", "Intermediate", "Technical"),
                    ("Git", "Intermediate", "Tool"),
                    ("DSA", "Intermediate", "Technical")
                ],
                "projects": [
                    ("E-Commerce Portal", "Full-stack marketplace with real-time cart and payment gateway mock.", "Python, Flask, SQLite, Vanilla JS", "https://github.com/rahul/e-commerce", "https://shop-demo.com"),
                    ("Task Workflow Manager", "Collaborative Kanban board with persistent SQLite task tracking.", "JavaScript, HTML5, CSS3, Flask", "https://github.com/rahul/kanban", "")
                ],
                "certifications": [
                    ("Meta Back-End Developer Certificate", "Coursera / Meta", "2025-08-10", "https://coursera.org/verify/meta-backend", "META-BE-892"),
                    ("Python for Everybody Specialization", "University of Michigan", "2024-12-05", "https://coursera.org/verify/py4e", "UMICH-PY-412")
                ],
                "roadmap_completed": ["01", "02", "03", "04", "05", "06"]
            },
            {
                "name": "Priya Patel",
                "email": "priya@student.com",
                "password": "Student@123",
                "profile": {
                    "full_name": "Priya Patel",
                    "headline": "Data Science Enthusiast | Machine Learning & Statistical Modeling",
                    "phone": "+91 9876543211",
                    "date_of_birth": "2003-11-20",
                    "gender": "Female",
                    "state": "Gujarat",
                    "city": "Ahmedabad",
                    "bio": "Final year IT undergrad with deep interest in predictive analytics, NLP, and data-driven insights.",
                    "college": "Nirma University Institute of Technology",
                    "university": "Nirma University",
                    "degree": "B.Tech",
                    "branch": "Information Technology",
                    "current_year": "4th Year",
                    "semester": "8th Semester",
                    "cgpa": 9.25,
                    "tenth_percentage": 95.0,
                    "twelfth_percentage": 93.5,
                    "family_income": 200000.0,
                    "category": "General",
                    "career_goal": "Data Scientist",
                    "preferred_role": "Data Scientist",
                    "resume_url": "https://example.com/resumes/priya_patel.pdf",
                    "github_url": "https://github.com/priyapatel-ds",
                    "linkedin_url": "https://linkedin.com/in/priyapatel-ds"
                },
                "skills": [
                    ("Python", "Advanced", "Technical"),
                    ("SQL", "Advanced", "Technical"),
                    ("Pandas", "Advanced", "Technical"),
                    ("NumPy", "Advanced", "Technical"),
                    ("Machine Learning", "Intermediate", "Technical"),
                    ("Statistics", "Advanced", "Technical"),
                    ("Data Visualization", "Intermediate", "Technical")
                ],
                "projects": [
                    ("Customer Churn Predictor", "Trained Random Forest and XGBoost models on 50k customer records with 92% ROC-AUC.", "Python, Scikit-Learn, Pandas, Seaborn", "https://github.com/priya/churn-ml", ""),
                    ("Healthcare Analytics Dashboard", "Interactive dashboard visualizing patient recovery trends across hospitals.", "Python, Streamlit, Plotly, SQL", "https://github.com/priya/health-dash", "")
                ],
                "certifications": [
                    ("IBM Data Science Professional Certificate", "IBM", "2025-06-15", "https://coursera.org/verify/ibm-ds", "IBM-DS-774"),
                    ("Deep Learning Specialization", "DeepLearning.AI", "2025-11-01", "https://coursera.org/verify/dl-spec", "DLAI-DL-991")
                ],
                "roadmap_completed": ["01", "02", "03", "04", "05"]
            },
            {
                "name": "Ananya Deshmukh",
                "email": "ananya@student.com",
                "password": "Student@123",
                "profile": {
                    "full_name": "Ananya Deshmukh",
                    "headline": "Electronics & Embedded Systems Engineer | IoT Protocols & Robotics",
                    "phone": "+91 9876543212",
                    "date_of_birth": "2004-02-18",
                    "gender": "Female",
                    "state": "Karnataka",
                    "city": "Bengaluru",
                    "bio": "ECE student passionate about hardware-software co-design, sensor integration, and FreeRTOS firmware.",
                    "college": "BMS College of Engineering",
                    "university": "Visvesvaraya Technological University",
                    "degree": "B.Tech",
                    "branch": "Electronics & Comm (ECE)",
                    "current_year": "3rd Year",
                    "semester": "5th Semester",
                    "cgpa": 7.80,
                    "tenth_percentage": 88.0,
                    "twelfth_percentage": 85.5,
                    "family_income": 550000.0,
                    "category": "General",
                    "career_goal": "Embedded Systems & IoT",
                    "preferred_role": "Embedded Systems & IoT",
                    "resume_url": "https://example.com/resumes/ananya_ece.pdf",
                    "github_url": "https://github.com/ananya-embedded",
                    "linkedin_url": "https://linkedin.com/in/ananya-deshmukh"
                },
                "skills": [
                    ("C", "Advanced", "Technical"),
                    ("C++", "Intermediate", "Technical"),
                    ("Microcontrollers", "Intermediate", "Technical"),
                    ("IoT Protocols", "Intermediate", "Technical"),
                    ("Embedded C", "Intermediate", "Technical"),
                    ("Python", "Beginner", "Technical")
                ],
                "projects": [
                    ("Smart Agriculture IoT Node", "Solar-powered ESP32 node publishing soil moisture & temperature via MQTT.", "C++, ESP32, MQTT, FreeRTOS", "https://github.com/ananya/agri-iot", "")
                ],
                "certifications": [
                    ("Introduction to Embedded Systems", "Coursera / CU Boulder", "2025-04-12", "https://coursera.org/verify/embedded", "CU-EMB-102")
                ],
                "roadmap_completed": ["01", "02", "03"]
            },
            {
                "name": "Rohan Gupta",
                "email": "rohan@student.com",
                "password": "Student@123",
                "profile": {
                    "full_name": "Rohan Gupta",
                    "headline": "Mechanical Engineering Undergrad | Robotics & CAD Simulation",
                    "phone": "+91 9876543213",
                    "date_of_birth": "2003-08-25",
                    "gender": "Male",
                    "state": "Uttar Pradesh",
                    "city": "Kanpur",
                    "bio": "Mechanical engineer exploring automation, finite element analysis, and Python scripting for engineering computation.",
                    "college": "Harcourt Butler Technical University",
                    "university": "HBTU",
                    "degree": "B.Tech",
                    "branch": "Mechanical",
                    "current_year": "4th Year",
                    "semester": "7th Semester",
                    "cgpa": 8.10,
                    "tenth_percentage": 89.0,
                    "twelfth_percentage": 86.0,
                    "family_income": 400000.0,
                    "category": "OBC",
                    "career_goal": "Software Developer",
                    "preferred_role": "Software Developer",
                    "resume_url": "https://example.com/resumes/rohan_gupta.pdf"
                },
                "skills": [
                    ("Python", "Intermediate", "Technical"),
                    ("C++", "Intermediate", "Technical"),
                    ("DSA", "Beginner", "Technical"),
                    ("Git", "Intermediate", "Tool"),
                    ("Linux", "Beginner", "Technical")
                ],
                "projects": [
                    ("Autonomous Robotic Arm Simulator", "Kinematic path planning simulation with Python and Matplotlib.", "Python, NumPy, Matplotlib", "https://github.com/rohan/robot-arm", "")
                ],
                "certifications": [
                    ("Programming for Everybody", "Coursera", "2024-09-15", "https://coursera.org/verify/py-rohan", "ROH-PY-11")
                ],
                "roadmap_completed": ["01", "02"]
            },
            {
                "name": "Sneha Reddy",
                "email": "sneha@student.com",
                "password": "Student@123",
                "profile": {
                    "full_name": "Sneha Reddy",
                    "headline": "AI & Deep Learning Researcher | Computer Vision & PyTorch",
                    "phone": "+91 9876543214",
                    "date_of_birth": "2004-01-10",
                    "gender": "Female",
                    "state": "Telangana",
                    "city": "Hyderabad",
                    "bio": "High-performing CSE student with focus on neural architectures, transfer learning, and efficient edge inference.",
                    "college": "International Institute of Information Technology (IIIT Hyderabad)",
                    "university": "IIIT Hyderabad",
                    "degree": "B.Tech",
                    "branch": "Computer Science",
                    "current_year": "3rd Year",
                    "semester": "6th Semester",
                    "cgpa": 9.50,
                    "tenth_percentage": 97.0,
                    "twelfth_percentage": 96.0,
                    "family_income": 180000.0,
                    "category": "SC",
                    "career_goal": "AI/ML Engineer",
                    "preferred_role": "AI/ML Engineer",
                    "resume_url": "https://example.com/resumes/sneha_reddy.pdf",
                    "github_url": "https://github.com/snehareddy-ai",
                    "linkedin_url": "https://linkedin.com/in/sneha-reddy-ai"
                },
                "skills": [
                    ("Python", "Advanced", "Technical"),
                    ("PyTorch", "Advanced", "Technical"),
                    ("Machine Learning", "Advanced", "Technical"),
                    ("Deep Learning", "Advanced", "Technical"),
                    ("Mathematics", "Advanced", "Technical"),
                    ("Git", "Intermediate", "Tool"),
                    ("Data Analysis", "Advanced", "Technical"),
                    ("DSA", "Advanced", "Technical")
                ],
                "projects": [
                    ("Medical Image Segmentation", "U-Net architecture for CT-scan lesion detection with 94.5% Dice score.", "PyTorch, OpenCV, NumPy, Scikit-Image", "https://github.com/sneha/unet-med", "https://med-ai-demo.org"),
                    ("Multilingual Translation Transformer", "Trained 6-layer encoder-decoder Transformer on Telugu-English corpus.", "PyTorch, HuggingFace, Tokenizers", "https://github.com/sneha/transformer-te", "")
                ],
                "certifications": [
                    ("Generative AI with Large Language Models", "DeepLearning.AI / AWS", "2025-07-20", "https://coursera.org/verify/genai-aws", "DLAI-GEN-551"),
                    ("Advanced Computer Vision with TensorFlow", "deeplearning.ai", "2025-02-14", "https://coursera.org/verify/cv-tf", "TF-CV-901")
                ],
                "roadmap_completed": ["01", "02", "03", "04", "05", "06", "07"]
            },
            {
                "name": "Vikram Singh",
                "email": "vikram@student.com",
                "password": "Student@123",
                "profile": {
                    "full_name": "Vikram Singh",
                    "headline": "Civil Engineering Student | Construction Tech & Infrastructure Analytics",
                    "phone": "+91 9876543215",
                    "date_of_birth": "2003-04-12",
                    "gender": "Male",
                    "state": "Rajasthan",
                    "city": "Jaipur",
                    "bio": "Final-year civil engineering undergrad interested in sustainable infrastructure and computational planning.",
                    "college": "Malaviya National Institute of Technology (MNIT Jaipur)",
                    "university": "MNIT Jaipur",
                    "degree": "B.Tech",
                    "branch": "Civil",
                    "current_year": "4th Year",
                    "semester": "8th Semester",
                    "cgpa": 7.40,
                    "tenth_percentage": 82.0,
                    "twelfth_percentage": 80.0,
                    "family_income": 600000.0,
                    "category": "General",
                    "career_goal": "Cloud & DevOps Engineer",
                    "preferred_role": "Cloud & DevOps Engineer",
                    "resume_url": "https://example.com/resumes/vikram_singh.pdf"
                },
                "skills": [
                    ("Linux", "Intermediate", "Technical"),
                    ("Python", "Beginner", "Technical"),
                    ("Networking", "Beginner", "Technical"),
                    ("Git", "Beginner", "Tool")
                ],
                "projects": [
                    ("Structural Load Calculation Script", "Automated stress calculation using Python numerical matrices.", "Python, NumPy", "https://github.com/vikram/load-calc", "")
                ],
                "certifications": [
                    ("Linux Fundamentals", "edX / Linux Foundation", "2024-11-10", "https://edx.org/verify/linux-found", "LF-LIN-101")
                ],
                "roadmap_completed": ["01"]
            }
        ]

        created_students = []
        for s_data in students_config:
            user = User(
                name=s_data["name"],
                email=s_data["email"],
                role="student",
                is_active=True
            )
            user.set_password(s_data["password"])
            db.session.add(user)
            db.session.flush()

            # Profile
            p_dict = s_data["profile"]
            profile = StudentProfile(user_id=user.id, **p_dict)
            db.session.add(profile)
            db.session.flush()

            # Skills
            for sk_name, sk_lvl, sk_cat in s_data["skills"]:
                skill = Skill(student_id=profile.id, name=sk_name, level=sk_lvl, category=sk_cat)
                db.session.add(skill)

            # Projects
            for p_title, p_desc, p_tech, p_gh, p_live in s_data.get("projects", []):
                proj = Project(student_id=profile.id, title=p_title, description=p_desc, technologies=p_tech, github_link=p_gh, live_link=p_live)
                db.session.add(proj)

            # Certifications
            for c_name, c_issuer, c_date, c_url, c_id in s_data.get("certifications", []):
                cert = Certification(student_id=profile.id, name=c_name, issuer=c_issuer, issue_date=c_date, credential_url=c_url, credential_id=c_id)
                db.session.add(cert)

            # Roadmap Progress
            for stage_code in s_data.get("roadmap_completed", []):
                rp = RoadmapProgress(
                    user_id=user.id,
                    roadmap_item=stage_code,
                    career_role=p_dict.get("preferred_role", "Full Stack Developer"),
                    status="completed",
                    completed=True
                )
                db.session.add(rp)

            # Initial Notification
            notif = Notification(
                user_id=user.id,
                title="Profile Verified",
                message="Welcome to the Student Career Portal! Your academic records have been indexed.",
                priority="INFO",
                link="/dashboard"
            )
            db.session.add(notif)
            created_students.append(user)

        print("[*] Seeding 16 Scholarships with realistic criteria...")
        scholarships_data = [
            {
                "name": "Tata Trust Means-Cum-Merit Scholarship",
                "provider": "Tata Trusts Foundation",
                "description": "Financial grant for meritorious undergraduate engineering students from low-income families demonstrating outstanding academic records.",
                "amount": "₹50,000 / Year",
                "amount_numeric": 50000.0,
                "deadline": "2026-11-30",
                "minimum_cgpa": 7.5,
                "maximum_income": 450000.0,
                "eligible_branches": "Computer Science, Information Technology, Electronics & Comm (ECE), Electrical (EEE)",
                "eligible_categories": "All",
                "required_documents": "Income Certificate, Previous Semester Grade Card, College Identity Card, Aadhaar Card",
                "application_url": "https://www.tatatrusts.org/scholarships"
            },
            {
                "name": "Google Generation Scholarship (APAC)",
                "provider": "Google Inc.",
                "description": "Designed to help students pursuing computer science degrees excel in technology and become active leaders in the field.",
                "amount": "₹1,50,000 / One-time",
                "amount_numeric": 150000.0,
                "deadline": "2026-12-15",
                "minimum_cgpa": 8.0,
                "maximum_income": 0.0,
                "eligible_branches": "Computer Science, Information Technology, Data Science, AI & ML",
                "eligible_categories": "All",
                "required_documents": "Resume (PDF), Official Academic Transcript, Essay Responses, Recommendation Letter",
                "application_url": "https://buildyourfuture.withgoogle.com/scholarships"
            },
            {
                "name": "Reliance Foundation Undergraduate Scholarship",
                "provider": "Reliance Foundation",
                "description": "Prestigious scholarship supporting first-year undergraduate students in any discipline across India based on merit and financial need.",
                "amount": "₹2,00,000 Total",
                "amount_numeric": 200000.0,
                "deadline": "2026-10-31",
                "minimum_cgpa": 7.0,
                "maximum_income": 300000.0,
                "eligible_branches": "All",
                "eligible_categories": "All",
                "required_documents": "12th Marksheet, Bonafide Student Certificate, Income Proof, Aptitude Test Score",
                "application_url": "https://www.reliancefoundation.org"
            },
            {
                "name": "Aditya Birla Group Technical Scholarship",
                "provider": "Aditya Birla Management Corporation",
                "description": "Merit-based financial award for high-performing engineering students across premier institutions in India.",
                "amount": "₹1,75,000 / Year",
                "amount_numeric": 175000.0,
                "deadline": "2026-11-20",
                "minimum_cgpa": 8.5,
                "maximum_income": 0.0,
                "eligible_branches": "Computer Science, Mechanical, Civil, Electrical (EEE)",
                "eligible_categories": "All",
                "required_documents": "JEE Advanced Rank Card, Dean Recommendation, Grade Sheets, Statement of Purpose",
                "application_url": "https://www.adityabirlascholars.net"
            },
            {
                "name": "ONGC Foundation Merit Scholarship for SC/ST/OBC",
                "provider": "Oil and Natural Gas Corporation (ONGC)",
                "description": "Empowering socio-economically marginalized students pursuing professional engineering and medical degree programs.",
                "amount": "₹48,000 / Year",
                "amount_numeric": 48000.0,
                "deadline": "2026-12-05",
                "minimum_cgpa": 6.5,
                "maximum_income": 250000.0,
                "eligible_branches": "All",
                "eligible_categories": "SC, ST, OBC, EWS",
                "required_documents": "Caste Certificate, Income Certificate, College Enrollment Letter, Bank Passbook Copy",
                "application_url": "https://www.ongcindia.com"
            },
            {
                "name": "Adobe Women-in-Technology Scholarship",
                "provider": "Adobe Systems",
                "description": "Scholarship recognizing outstanding female undergraduate students identifying as innovators in computer science and engineering.",
                "amount": "₹1,00,000 + Mentorship",
                "amount_numeric": 100000.0,
                "deadline": "2026-11-15",
                "minimum_cgpa": 8.0,
                "maximum_income": 0.0,
                "eligible_branches": "Computer Science, Information Technology, Data Science",
                "eligible_categories": "All",
                "required_documents": "Technical Portfolio, GitHub Link, Resume, 3 Letter of Recommendations",
                "application_url": "https://www.adobe.com/careers/university/scholarships"
            },
            {
                "name": "HDFC Badhte Kadam Financial Aid",
                "provider": "HDFC Bank Education Crisis Program",
                "description": "Dedicated assistance for students facing financial distress to ensure uninterrupted completion of technical education.",
                "amount": "₹30,000 / Year",
                "amount_numeric": 30000.0,
                "deadline": "2026-10-25",
                "minimum_cgpa": 6.0,
                "maximum_income": 200000.0,
                "eligible_branches": "All",
                "eligible_categories": "All",
                "required_documents": "Fee Structure Proof, Marksheets, Ration Card / Income Certificate",
                "application_url": "https://www.hdfcbank.com/csr"
            },
            {
                "name": "Siemens Tech Scholars Grant",
                "provider": "Siemens India Foundation",
                "description": "Scholarship and industrial skill-training program for engineering students from government and aided engineering colleges.",
                "amount": "100% Tuition Fee",
                "amount_numeric": 80000.0,
                "deadline": "2026-11-28",
                "minimum_cgpa": 7.2,
                "maximum_income": 350000.0,
                "eligible_branches": "Electronics & Comm (ECE), Electrical (EEE), Mechanical",
                "eligible_categories": "All",
                "required_documents": "Annual Fee Receipt, Income Proof, 10th & 12th Marksheets",
                "application_url": "https://www.siemens.com/in/scholars"
            },
            {
                "name": "Infosys Foundation STEM Excellence Grant",
                "provider": "Infosys Foundation",
                "description": "Supporting talented young minds in computer science and quantitative STEM disciplines across tier-2 and tier-3 colleges.",
                "amount": "₹1,00,000 / Year",
                "amount_numeric": 100000.0,
                "deadline": "2026-12-20",
                "minimum_cgpa": 8.0,
                "maximum_income": 500000.0,
                "eligible_branches": "Computer Science, Information Technology, Data Science, AI & ML",
                "eligible_categories": "All",
                "required_documents": "College ID, CGPA Transcript, Project Portfolio Link",
                "application_url": "https://www.infosys.org/infosys-foundation"
            },
            {
                "name": "Amazon Future Engineer Scholarship",
                "provider": "Amazon India",
                "description": "Comprehensive scholarship and tech mentorship grant for female students enrolled in 1st year B.Tech Computer Science programs.",
                "amount": "₹50,000 / Year + Laptop",
                "amount_numeric": 50000.0,
                "deadline": "2026-12-31",
                "minimum_cgpa": 7.0,
                "maximum_income": 300000.0,
                "eligible_branches": "Computer Science, Information Technology",
                "eligible_categories": "All",
                "required_documents": "Admission Letter, 12th Board Certificate, Income Certificate",
                "application_url": "https://www.amazonfutureengineer.in"
            },
            {
                "name": "Kotak Kanya Scholarship for Girls in Higher Education",
                "provider": "Kotak Education Foundation",
                "description": "Supporting meritorious girl students from underprivileged families pursuing professional degrees in engineering and architecture.",
                "amount": "₹1,50,000 / Year",
                "amount_numeric": 150000.0,
                "deadline": "2026-11-10",
                "minimum_cgpa": 7.5,
                "maximum_income": 320000.0,
                "eligible_branches": "All",
                "eligible_categories": "All",
                "required_documents": "12th Marks Sheet (min 85%), Income Proof, Identity Proof",
                "application_url": "https://kotakeducation.org/kotak-kanya-scholarship"
            },
            {
                "name": "L'Oreal India For Young Women in Science",
                "provider": "L'Oréal India",
                "description": "Encouraging young women to pursue higher studies in science and engineering disciplines across recognized Indian universities.",
                "amount": "₹2,50,000 Total",
                "amount_numeric": 250000.0,
                "deadline": "2026-12-10",
                "minimum_cgpa": 8.2,
                "maximum_income": 400000.0,
                "eligible_branches": "All",
                "eligible_categories": "All",
                "required_documents": "12th PCB/PCM Marksheet (min 85%), Family Income Proof, Essay",
                "application_url": "https://www.loreal.com/en/india"
            },
            {
                "name": "National Merit Post-Matric State Scholarship",
                "provider": "Ministry of Social Justice & Empowerment",
                "description": "Government of India financial aid scheme supporting reserved category students across all undergraduate engineering programs.",
                "amount": "₹35,000 / Year",
                "amount_numeric": 35000.0,
                "deadline": "2026-11-25",
                "minimum_cgpa": 6.0,
                "maximum_income": 250000.0,
                "eligible_branches": "All",
                "eligible_categories": "SC, ST, OBC, EWS",
                "required_documents": "NSP Portal ID, Caste Certificate, Domicile Certificate, Bank Account Details",
                "application_url": "https://scholarships.gov.in"
            },
            {
                "name": "NTPC Special Technical Scholarship",
                "provider": "National Thermal Power Corporation (NTPC)",
                "description": "Targeted educational assistance for third-year engineering students in electrical, mechanical, and civil engineering disciplines.",
                "amount": "₹40,000 / Year",
                "amount_numeric": 40000.0,
                "deadline": "2026-12-28",
                "minimum_cgpa": 7.0,
                "maximum_income": 500000.0,
                "eligible_branches": "Electrical (EEE), Mechanical, Civil",
                "eligible_categories": "All",
                "required_documents": "College Bonafide, 4th Semester Marksheet, Identity Proof",
                "application_url": "https://www.ntpc.co.in"
            },
            {
                "name": "Mahindra All India Talent Scholarship",
                "provider": "K. C. Mahindra Education Trust",
                "description": "Supporting young students across diverse engineering diploma and degree programs to foster grassroots technical development.",
                "amount": "₹25,000 / Year",
                "amount_numeric": 25000.0,
                "deadline": "2026-11-18",
                "minimum_cgpa": 6.8,
                "maximum_income": 300000.0,
                "eligible_branches": "All",
                "eligible_categories": "All",
                "required_documents": "Admission Proof, 10th / 12th Marksheet, Recommendation",
                "application_url": "https://www.kcmet.org"
            },
            {
                "name": "Sitaram Jindal Foundation Merit Scholarship",
                "provider": "Sitaram Jindal Foundation",
                "description": "Purely merit-cum-means financial aid helping deserving undergraduate students across all engineering branches.",
                "amount": "₹36,000 / Year",
                "amount_numeric": 36000.0,
                "deadline": "2026-12-22",
                "minimum_cgpa": 7.0,
                "maximum_income": 350000.0,
                "eligible_branches": "All",
                "eligible_categories": "All",
                "required_documents": "Jindal Form Annexures, Income Certificate, Marksheets",
                "application_url": "https://www.sitaramjindalfoundation.org"
            }
        ]

        for s in scholarships_data:
            sch_obj = Scholarship(**s, is_active=True)
            db.session.add(sch_obj)

        print("[*] Seeding 16 Internships across tech domains...")
        internships_data = [
            {
                "company": "Microsoft",
                "title": "Software Engineering Intern",
                "description": "Collaborate with Azure core engineering teams to develop cloud microservices, automate distributed testing, and optimize API latencies.",
                "location": "Hyderabad / Bengaluru",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹1,25,000 / Month",
                "required_skills": "C++, Python, Data Structures, Algorithms, Git, Linux",
                "domain": "Software Development",
                "deadline": "2026-11-15",
                "application_url": "https://careers.microsoft.com"
            },
            {
                "company": "Google",
                "title": "Winter STEP Intern (Software Student Training)",
                "description": "Development internship specifically designed for undergraduate computer science students to work on real Google software systems.",
                "location": "Bengaluru",
                "work_mode": "On-site",
                "duration": "3 Months",
                "stipend": "₹1,10,000 / Month",
                "required_skills": "Python, Java, C++, DSA, OOP, Problem Solving",
                "domain": "Software Development",
                "deadline": "2026-11-20",
                "application_url": "https://careers.google.com"
            },
            {
                "company": "Amazon",
                "title": "Full Stack Web Developer Intern",
                "description": "Design and implement scalable customer-facing web interfaces and backend microservices supporting Amazon retail systems.",
                "location": "Remote",
                "work_mode": "Remote",
                "duration": "6 Months",
                "stipend": "₹80,000 / Month",
                "required_skills": "JavaScript, Python, Flask, HTML, CSS, SQL, Git",
                "domain": "Web Development",
                "deadline": "2026-12-01",
                "application_url": "https://amazon.jobs"
            },
            {
                "company": "Cisco",
                "title": "Cybersecurity & Network Analyst Intern",
                "description": "Analyze network traffic telemetry, perform automated vulnerability assessments, and implement zero-trust access protocols.",
                "location": "Bengaluru",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹60,000 / Month",
                "required_skills": "Networking, Linux, Python, Cryptography, Wireshark, Firewalls",
                "domain": "Cybersecurity",
                "deadline": "2026-11-30",
                "application_url": "https://jobs.cisco.com"
            },
            {
                "company": "IBM Research",
                "title": "AI & Machine Learning Research Intern",
                "description": "Conduct applied research on natural language transformers, model distillation, and trustworthy AI governance tools.",
                "location": "Bengaluru",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹70,000 / Month",
                "required_skills": "Python, PyTorch, Machine Learning, Deep Learning, Statistics",
                "domain": "AI/ML",
                "deadline": "2026-12-10",
                "application_url": "https://ibm.com/employment"
            },
            {
                "company": "Goldman Sachs",
                "title": "Data Analyst / Quant Intern",
                "description": "Build high-throughput financial data pipelines, calculate risk telemetry, and generate interactive analytics dashboards.",
                "location": "Bengaluru",
                "work_mode": "On-site",
                "duration": "3 Months",
                "stipend": "₹1,00,000 / Month",
                "required_skills": "SQL, Python, Pandas, Statistics, Excel, Data Visualization",
                "domain": "Data Science",
                "deadline": "2026-11-25",
                "application_url": "https://goldmansachs.com/careers"
            },
            {
                "company": "Swiggy",
                "title": "Backend Engineering Intern",
                "description": "Scale real-time order matching, geospatial querying, and high-concurrency microservices during surge delivery hours.",
                "location": "Remote",
                "work_mode": "Remote",
                "duration": "3 Months",
                "stipend": "₹45,000 / Month",
                "required_skills": "Python, Flask, SQL, Redis, REST APIs, Git",
                "domain": "Web Development",
                "deadline": "2026-11-18",
                "application_url": "https://careers.swiggy.com"
            },
            {
                "company": "Intel Corporation",
                "title": "Embedded Systems & Firmware Intern",
                "description": "Write low-level device drivers, optimize microcontroller register accesses, and validate hardware-in-the-loop test benches.",
                "location": "Bengaluru",
                "work_mode": "On-site",
                "duration": "6 Months",
                "stipend": "₹55,000 / Month",
                "required_skills": "C, C++, Embedded C, Microcontrollers, RTOS, I2C, SPI",
                "domain": "Embedded Systems",
                "deadline": "2026-12-05",
                "application_url": "https://intel.com/jobs"
            },
            {
                "company": "Zerodha",
                "title": "Frontend / UI/UX Engineering Intern",
                "description": "Craft ultra-fast, zero-dependency financial chart visualizations and responsive interfaces with clean vanilla web standards.",
                "location": "Remote",
                "work_mode": "Remote",
                "duration": "3 Months",
                "stipend": "₹50,000 / Month",
                "required_skills": "HTML5, CSS3, JavaScript, UI/UX, Web Performance, Git",
                "domain": "Web Development",
                "deadline": "2026-12-15",
                "application_url": "https://zerodha.com/careers"
            },
            {
                "company": "PhonePe",
                "title": "Cloud & DevOps Intern",
                "description": "Maintain high-uptime Kubernetes clusters, automate deployment pipelines with Docker and Terraform for UPI payments.",
                "location": "Bengaluru",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹75,000 / Month",
                "required_skills": "Linux, Docker, AWS, Git, CI/CD, Kubernetes, Python",
                "domain": "Cloud Computing",
                "deadline": "2026-11-28",
                "application_url": "https://phonepe.com/careers"
            },
            {
                "company": "Adobe",
                "title": "Machine Learning Engineering Intern",
                "description": "Develop and deploy deep neural network models for automated image editing and generative creative workflows.",
                "location": "Noida",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹90,000 / Month",
                "required_skills": "Python, Machine Learning, Deep Learning, PyTorch, OpenCV",
                "domain": "AI/ML",
                "deadline": "2026-12-20",
                "application_url": "https://adobe.com/careers"
            },
            {
                "company": "Razorpay",
                "title": "Software Engineering Intern - FinTech",
                "description": "Build robust payment settlement workflows, fraud anomaly detectors, and high-reliability RESTful API endpoints.",
                "location": "Bengaluru",
                "work_mode": "Remote",
                "duration": "3 Months",
                "stipend": "₹65,000 / Month",
                "required_skills": "Python, SQL, DSA, REST APIs, Git, Linux",
                "domain": "Software Development",
                "deadline": "2026-12-12",
                "application_url": "https://razorpay.com/jobs"
            },
            {
                "company": "Zomato",
                "title": "Data Science & NLP Intern",
                "description": "Analyze restaurant review sentiment, train semantic recommendation vectors, and optimize real-time search queries.",
                "location": "Gurugram",
                "work_mode": "Hybrid",
                "duration": "3 Months",
                "stipend": "₹50,000 / Month",
                "required_skills": "Python, Pandas, Machine Learning, SQL, Statistics, NLP",
                "domain": "Data Science",
                "deadline": "2026-11-22",
                "application_url": "https://zomato.com/careers"
            },
            {
                "company": "ISRO (Indian Space Research Organisation)",
                "title": "Space Flight Dynamics Software Trainee",
                "description": "Collaborate on orbital mechanics numerical simulation routines and sensor telemetry software packages.",
                "location": "Trivandrum",
                "work_mode": "On-site",
                "duration": "6 Months",
                "stipend": "₹35,000 / Month",
                "required_skills": "C++, Python, Mathematics, DSA, Linux",
                "domain": "Software Development",
                "deadline": "2026-12-18",
                "application_url": "https://isro.gov.in/careers"
            },
            {
                "company": "TCS Research & Innovations",
                "title": "Cloud Security Research Intern",
                "description": "Research automated zero-day vulnerability discovery, container sandbox isolation, and cryptographic auditing.",
                "location": "Pune",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹40,000 / Month",
                "required_skills": "Linux, Python, Networking, Cryptography, Security",
                "domain": "Cybersecurity",
                "deadline": "2026-11-26",
                "application_url": "https://tcs.com/careers"
            },
            {
                "company": "Flipkart",
                "title": "Mobile App Development Intern (Android/Flutter)",
                "description": "Enhance mobile shopping application performance, offline caching, smooth animations, and secure checkout flows.",
                "location": "Bengaluru",
                "work_mode": "Hybrid",
                "duration": "6 Months",
                "stipend": "₹70,000 / Month",
                "required_skills": "Java, Kotlin, Mobile Development, Git, REST APIs",
                "domain": "Mobile Development",
                "deadline": "2026-12-08",
                "application_url": "https://flipkartcareers.com"
            }
        ]

        for intern in internships_data:
            intern_obj = Internship(**intern, is_active=True)
            db.session.add(intern_obj)

        print("[*] Seeding 16 Industry-Standard Courses...")
        courses_data = [
            {
                "name": "CS50's Introduction to Computer Science",
                "platform": "YouTube/Harvard CS50",
                "description": "Harvard University's flagship introduction to the intellectual enterprises of computer science and the art of programming.",
                "duration": "12 Weeks",
                "level": "Beginner",
                "skill": "C",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.9,
                "course_url": "https://cs50.harvard.edu/x"
            },
            {
                "name": "Python for Everybody Specialization",
                "platform": "Coursera",
                "description": "Learn to program and analyze data with Python. Develop programs to gather, clean, analyze, and visualize data.",
                "duration": "8 Weeks",
                "level": "Beginner",
                "skill": "Python",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.8,
                "course_url": "https://www.coursera.org/specializations/python"
            },
            {
                "name": "Modern HTML5 & Responsive CSS3 Bootcamp",
                "platform": "FreeCodeCamp",
                "description": "Master web styling fundamentals, CSS Flexbox, Grid, custom properties, animations, and accessible semantic layouts.",
                "duration": "30 Hours",
                "level": "Beginner",
                "skill": "CSS",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.7,
                "course_url": "https://www.freecodecamp.org"
            },
            {
                "name": "The Complete JavaScript Algorithm Course",
                "platform": "Udemy",
                "description": "Deep dive into ES6+ syntax, asynchronous event loop, Promises, Fetch API, closures, prototypes, and DOM rendering.",
                "duration": "50 Hours",
                "level": "Intermediate",
                "skill": "JavaScript",
                "price": "₹499",
                "price_numeric": 499.0,
                "rating": 4.8,
                "course_url": "https://www.udemy.com"
            },
            {
                "name": "Relational Databases & SQL Mastery",
                "platform": "Coursera",
                "description": "Learn 3NF schema design, indexing strategies, aggregate functions, complex joins, and SQLite / PostgreSQL optimization.",
                "duration": "6 Weeks",
                "level": "Intermediate",
                "skill": "SQL",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.7,
                "course_url": "https://www.coursera.org"
            },
            {
                "name": "Flask Web Development & Microservices",
                "platform": "edX",
                "description": "Build robust web applications, REST APIs, session authentication, and SQLAlchemy database ORMs with Python Flask.",
                "duration": "6 Weeks",
                "level": "Intermediate",
                "skill": "Flask",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.8,
                "course_url": "https://www.edx.org"
            },
            {
                "name": "Machine Learning Specialization by Andrew Ng",
                "platform": "Coursera",
                "description": "Master fundamental AI concepts, supervised learning, neural networks, decision trees, and unsupervised techniques.",
                "duration": "10 Weeks",
                "level": "Intermediate",
                "skill": "Machine Learning",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.9,
                "course_url": "https://www.coursera.org/specializations/machine-learning-introduction"
            },
            {
                "name": "Deep Learning with PyTorch",
                "platform": "FreeCodeCamp",
                "description": "Build CNNs, RNNs, and Transformers from scratch with GPU acceleration and tensor operations in PyTorch.",
                "duration": "25 Hours",
                "level": "Advanced",
                "skill": "PyTorch",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.9,
                "course_url": "https://www.freecodecamp.org"
            },
            {
                "name": "Data Structures & Algorithms in C++",
                "platform": "NPTEL",
                "description": "Rigorous IIT-curated course covering asymptotic complexity, dynamic programming, graph traversal, and tree data structures.",
                "duration": "12 Weeks",
                "level": "Advanced",
                "skill": "DSA",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.7,
                "course_url": "https://nptel.ac.in"
            },
            {
                "name": "Linux Command Line & Shell Scripting",
                "platform": "edX",
                "description": "Master Bash scripting, process scheduling, file permissions, pipe redirection, systemd, and server administration.",
                "duration": "4 Weeks",
                "level": "Beginner",
                "skill": "Linux",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.6,
                "course_url": "https://www.edx.org"
            },
            {
                "name": "AWS Certified Cloud Practitioner",
                "platform": "Udemy",
                "description": "Complete guide to Amazon Web Services architecture, EC2 instances, S3 storage, IAM security policies, and VPC routing.",
                "duration": "15 Hours",
                "level": "Beginner",
                "skill": "AWS",
                "price": "₹649",
                "price_numeric": 649.0,
                "rating": 4.7,
                "course_url": "https://www.udemy.com"
            },
            {
                "name": "Docker & Kubernetes DevOps Masterclass",
                "platform": "Coursera",
                "description": "Containerize microservices, build multi-stage Dockerfiles, manage Helm charts, and configure CI/CD deployment pipelines.",
                "duration": "8 Weeks",
                "level": "Advanced",
                "skill": "Docker",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.8,
                "course_url": "https://www.coursera.org"
            },
            {
                "name": "Cybersecurity Fundamentals & Network Defense",
                "platform": "Coursera",
                "description": "Explore network defense strategies, symmetric/asymmetric cryptography, packet analysis, and OWASP web vulnerability prevention.",
                "duration": "8 Weeks",
                "level": "Intermediate",
                "skill": "Networking",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.6,
                "course_url": "https://www.coursera.org"
            },
            {
                "name": "Applied Data Analysis with Pandas & NumPy",
                "platform": "Coursera",
                "description": "Data wrangling, cleaning missing values, exploratory analysis, time-series parsing, and feature extraction with Python Pandas.",
                "duration": "6 Weeks",
                "level": "Intermediate",
                "skill": "Pandas",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.8,
                "course_url": "https://www.coursera.org"
            },
            {
                "name": "Embedded Systems Architecture & Microcontrollers",
                "platform": "NPTEL",
                "description": "Comprehensive study of ARM Cortex-M architecture, GPIO registers, interrupt service routines, and I2C/SPI interfaces.",
                "duration": "12 Weeks",
                "level": "Advanced",
                "skill": "Microcontrollers",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.7,
                "course_url": "https://nptel.ac.in"
            },
            {
                "name": "Git & GitHub Version Control Collaboration",
                "platform": "FreeCodeCamp",
                "description": "Master Git commits, branching strategies, resolving merge conflicts, pull requests, and CI/CD automation with GitHub Actions.",
                "duration": "10 Hours",
                "level": "Beginner",
                "skill": "Git",
                "price": "Free",
                "price_numeric": 0.0,
                "rating": 4.9,
                "course_url": "https://www.freecodecamp.org"
            }
        ]

        for course in courses_data:
            c_obj = Course(**course, is_active=True)
            db.session.add(c_obj)

        db.session.flush()

        # Seed sample applications across students
        print("[*] Seeding sample applications and pipeline workflows...")
        rahul = created_students[0]
        priya = created_students[1]
        ananya = created_students[2]
        sneha = created_students[4]

        applications_seed = [
            (rahul.id, "scholarship", 1, "Shortlisted", "Applied with semester 5 marksheets; shortlisted for telephonic interview.", "2026-11-30", "2026-10-15"),
            (rahul.id, "internship", 3, "Under Review", "Submitted online coding assessment for Amazon Full Stack role.", "2026-12-01", ""),
            (rahul.id, "internship", 7, "Applied", "Applied on Swiggy career portal.", "2026-11-18", ""),
            (rahul.id, "course", 4, "Accepted", "Completed 60% of curriculum.", "", ""),
            
            (priya.id, "scholarship", 2, "Applied", "Submitted essay on AI for social good.", "2026-12-15", ""),
            (priya.id, "internship", 6, "Interview", "Technical interview scheduled with Goldman Sachs Quant team.", "2026-11-25", "2026-10-20"),
            (priya.id, "internship", 5, "Applied", "Submitted research proposal on NLP.", "2026-12-10", ""),
            
            (ananya.id, "scholarship", 8, "Applied", "Siemens scholarship application submitted via college office.", "2026-11-28", ""),
            (ananya.id, "internship", 8, "Under Review", "Intel embedded engineering candidate screening.", "2026-12-05", ""),
            
            (sneha.id, "scholarship", 6, "Accepted", "Awarded Adobe Women-in-Technology 2026 Grant!", "2026-11-15", ""),
            (sneha.id, "internship", 11, "Accepted", "Offer letter received for Adobe ML Intern.", "2026-12-20", "")
        ]

        for u_id, o_type, o_id, status, notes, dline, idate in applications_seed:
            app_rec = Application(
                user_id=u_id,
                opportunity_type=o_type,
                opportunity_id=o_id,
                status=status,
                notes=notes,
                deadline=dline,
                interview_date=idate
            )
            db.session.add(app_rec)

        # Seed bookmarks
        saved_seed = [
            (rahul.id, "scholarship", 1),
            (rahul.id, "internship", 1),
            (rahul.id, "course", 6),
            (priya.id, "scholarship", 2),
            (priya.id, "internship", 6),
            (sneha.id, "scholarship", 6),
            (sneha.id, "internship", 11)
        ]
        for u_id, o_type, o_id in saved_seed:
            saved_item = SavedOpportunity(user_id=u_id, opportunity_type=o_type, opportunity_id=o_id)
            db.session.add(saved_item)

        # Seed sample Admin Action Logs
        print("[*] Seeding administrative audit trail...")
        logs_seed = [
            (admin.id, admin.name, "SYSTEM_INIT", "Database", 1, "Initialized system schema and production seed records", "127.0.0.1"),
            (admin.id, admin.name, "CREATE_SCHOLARSHIP", "Scholarship", 1, "Published Tata Trust Means-Cum-Merit Scholarship (₹50,000/yr)", "127.0.0.1"),
            (admin.id, admin.name, "CREATE_SCHOLARSHIP", "Scholarship", 2, "Published Google Generation Scholarship (₹1,50,000)", "127.0.0.1"),
            (admin.id, admin.name, "CREATE_INTERNSHIP", "Internship", 1, "Published Microsoft Software Engineering Intern posting", "127.0.0.1"),
            (admin.id, admin.name, "UPDATE_APPLICATION_STATUS", "Application", 1, "Promoted Rahul Sharma's Tata Trust application to 'Shortlisted'", "127.0.0.1"),
            (admin.id, admin.name, "UPDATE_APPLICATION_STATUS", "Application", 10, "Approved Sneha Reddy's Adobe scholarship grant (Status: Accepted)", "127.0.0.1")
        ]
        for a_id, a_name, act, ent, t_id, det, ip in logs_seed:
            log_item = AdminActionLog(
                admin_id=a_id,
                admin_name=a_name,
                action=act,
                target_entity=ent,
                target_id=t_id,
                details=det,
                ip_address=ip
            )
            db.session.add(log_item)

        db.session.commit()
        print("\n========================================================")
        print("[+] DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print(f"    - Administrator: admin@portal.com (Password: Admin@123)")
        print(f"    - Students: {len(created_students)} diverse student accounts")
        print(f"    - Scholarships: {len(scholarships_data)} active grants")
        print(f"    - Internships: {len(internships_data)} industry roles")
        print(f"    - Courses: {len(courses_data)} certified courses")
        print(f"    - Applications: {len(applications_seed)} pipeline records")
        print(f"    - Audit Logs: {len(logs_seed)} initial governance logs")
        print("========================================================\n")

if __name__ == "__main__":
    seed_database()
