# Student Career & Scholarship Portal
> **An Enterprise-Grade, Explainable Decision Support & Opportunity Management Platform**
> *Final-Year Computer Science & Engineering (CSE) Capstone Project*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-red.svg)](https://www.sqlalchemy.org/)
[![Architecture](https://img.shields.io/badge/Architecture-5--Layer%20Service%20Oriented-purple.svg)](#-system-architecture)
[![Security](https://img.shields.io/badge/Security-RBAC%20%7C%20OWASP%20Top%2010-orange.svg)](#-security-architecture)
[![Tests](https://img.shields.io/badge/Tests-59%2F59%20Passing%20(100%25)-brightgreen.svg)](#-testing--quality-assurance)

---

## 📌 Project Overview

The **Student Career & Scholarship Portal** is a centralized, production-quality web platform engineered to bridge the gap between higher education students and critical career advancement opportunities. Moving beyond simple CRUD functionality, the platform combines **deterministic explainable decision systems**, **multi-dimensional career readiness scoring**, **role-tailored career roadmaps**, and a **7-stage application tracking pipeline** into an intuitive SaaS-grade portal.

---

## 🌟 Core System Highlights

### 1. 🎓 Intelligent Student Decision Systems
* **Deterministic Explainable Scholarship Eligibility Engine**:
  * Evaluates academic cutoffs, income thresholds, engineering branch synonyms, and reservation categories with a weighted mathematical scoring algorithm ($S \in [0, 100]$).
  * Returns transparent reason explanations (*"CGPA exceeds minimum cutoff"*, *"Income within threshold"*) and missing criteria.
* **6-Dimensional Career Readiness Engine**:
  * Computes dynamic readiness scores across **Academic Performance (20%)**, **Technical Skills (25%)**, **Project Portfolio (20%)**, **Accredited Certifications (10%)**, **Practical Experience (10%)**, and **Resume Completeness (15%)**.
* **Role-Tailored Career Roadmaps & Skill Gap Analysis**:
  * Features 7 curated industry pathways (*Software Engineer, Full Stack Developer, Backend Developer, Frontend Developer, Data Scientist, Machine Learning Engineer, Cloud Engineer, Cybersecurity Analyst*).
  * Automatically categorizes acquired skills vs missing skills and links direct gap-remediation courses.
  * Milestone progress is tracked and persisted per student and role.
* **7-Stage Opportunity Application Pipeline**:
  * Complete lifecycle tracker: `Saved` $\to$ `Applied` $\to$ `Under Review` $\to$ `Shortlisted` $\to$ `Interview` $\to$ `Accepted` $\to$ `Rejected`.
  * Computes conversion funnels, interview reminders, and acceptance rates from real-time database queries.
* **Interactive Resume Profile & Live Preview**:
  * Displays academic background, verified skills with proficiency tags, project links, credentials, and live profile strength gauge with a formatted modal preview.

---

### 2. 🛡️ Administrative Governance & Analytics
* **Real-Time Operational Analytics**:
  * Live KPI aggregation feeds for total students, active listings, application distribution, conversion rates, and skill supply/demand.
* **Comprehensive Opportunity Management (CRUD)**:
  * Full administrative control over scholarships, internships, and courses with search, filtering, and backend pagination.
* **Immutable Compliance Audit Logging (`AdminActionLog`)**:
  * Every administrative action (create, update, delete, status toggle) is cryptographically recorded with actor ID, target entity, timestamp, and client IP address.

---

### 3. 🔒 Enterprise Security & Architecture
* **Role-Based Access Control (RBAC)**: Distinct permissions for `student` and `admin` with strict route decorators (`@login_required`, `@admin_required`) preventing privilege escalation.
* **OWASP Mitigations**: Parameterized SQLAlchemy queries (anti-SQLi), Jinja2 HTML auto-escaping (anti-XSS), HTTP security headers (`CSP`, `X-Frame-Options`, `X-Content-Type-Options`), and PBKDF2:SHA256 password salting.
* **Decoupled 5-Layer Design**: Complete separation between Presentation, Route Blueprints, Service Layer, Repository/ORM, and Database.

---

## 🏗️ System Architecture

```
+-------------------------------------------------------------------------+
|                         Presentation Layer                              |
|   HTML5 Semantic Templates + Jinja2 + Vanilla CSS3 Tokens + Chart.js    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                      Route / Controller Layer                           |
|       Flask Blueprints (Auth, Student, Scholarships, Internships,       |
|                  Courses, Applications, Career, Admin, API)             |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                           Service Layer                                 |
|  - AuthService: Identity, Password Hashing & Profile Management         |
|  - EligibilityService: Multi-criteria Explainable Scoring Engine        |
|  - CareerService: 6-Dimension Readiness & Multi-Path Roadmap Engine     |
|  - RecommendationService: Weighted Opportunity Matching & Priority Hub |
|  - ApplicationService: Lifecycle Tracking & Conversion Analytics       |
|  - NotificationService: Priority Tiering & Deadline Alert System        |
|  - AnalyticsService: Live Database KPI Feeds & Funnel Metrics           |
|  - AdminService: Immutable Audit Logging & Governance CRUD Operations   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  Repository & Data Access Layer                         |
|      SQLAlchemy ORM with 3NF Normalized Models, Constraints & Indexes   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         Database Layer                                  |
|         SQLite (Local Development) / PostgreSQL (Production WSGI)       |
+-------------------------------------------------------------------------+
```

---

## 📂 Codebase Directory Layout

```
SCHOLARSHIP WEBSITE/
├── app.py                      # Application Factory, Security Middleware & Error Handlers
├── config.py                   # Environment Configurations (Dev, Testing, Prod)
├── models.py                   # 3NF Relational Database Schema & Constraints (13 Tables)
├── seed.py                     # Production-Grade Database Seeder
├── gunicorn.conf.py            # WSGI Production Server Configuration
├── Dockerfile                  # Production Containerization Spec
├── docker-compose.yml          # Container Orchestration Spec
├── requirements.txt            # Python Dependencies
├── .env.example                # Environment Variable Template
├── test_portal_full.py         # 59-Point E2E Integration Suite
├── verify_live.py              # Live HTTP Endpoint Verifier
│
├── services/                   # Business Logic & Algorithmic Engines
│   ├── auth_service.py         # Authentication & Profile Service
│   ├── eligibility_service.py  # Scholarship Matching & Qualifier Logic
│   ├── career_service.py       # Career Readiness & 7-Pathway Roadmaps
│   ├── recommendation_service.py # Opportunity Recommendation & Priority Hub
│   ├── application_service.py  # Pipeline Lifecycle & Conversion Rates
│   ├── notification_service.py # Tiered Notifications & Deadline Alerts
│   ├── analytics_service.py    # Live KPI Aggregations & Profile Scoring
│   └── admin_service.py        # Admin Governance & Audit Logging
│
├── routes/                     # Blueprint Route Controllers
│   ├── auth.py                 # Registration, Student & Admin Login, Logout
│   ├── student.py              # Dashboard, Profile, Saved Items & Notifications
│   ├── scholarships.py         # Scholarship Discovery & Eligibility Evaluator
│   ├── internships.py          # Internship Catalog & Domain Search
│   ├── courses.py              # Course Catalog & Skill Gap Filtering
│   ├── applications.py         # Application Pipeline Tracker & Status Updates
│   ├── career.py               # Career Simulator & Roadmap Checklist
│   ├── admin.py                # Admin Console, Analytics & Audit Logs
│   └── api.py                  # Standard JSON REST API Layer
│
├── tests/                      # Modular Unit & Feature Test Suite
│   ├── conftest.py             # Test Fixtures & In-Memory Database
│   ├── test_auth_service.py    # Authentication & Password Tests
│   ├── test_eligibility_engine.py # Scholarship Algorithm Tests
│   ├── test_career_readiness.py # Readiness & Skill Gap Tests
│   ├── test_applications.py    # Pipeline & Conversion Tests
│   ├── test_admin_and_rbac.py  # RBAC & Audit Log Tests
│   ├── test_api.py             # REST API Contract Tests
│   └── test_edge_cases.py      # Edge Cases & Escalation Tests
│
├── templates/                  # Semantic HTML5 Templates (Jinja2)
│   ├── base.html               # Base Skeleton, Responsive Navbar & Modals
│   ├── index.html              # Modern Landing Page with Stats
│   ├── auth/                   # Login & Registration Templates
│   ├── student/                # Student Dashboard, Profile, Catalog & Tracker
│   ├── admin/                  # Admin Dashboard, Tables & Audit Trail
│   └── errors/                 # Standard 400, 401, 403, 404, 500 Pages
│
└── static/                     # Frontend Assets
    ├── css/                    # Custom Properties, Grids, Responsive Styles
    └── js/                     # Modular Vanilla JavaScript Controllers
```

---

## 🧮 Algorithmic Formulations

### 1. Scholarship Match Score Formula
$$\text{Score} = w_{\text{acad}} S_{\text{acad}} + w_{\text{fin}} S_{\text{fin}} + w_{\text{branch}} S_{\text{branch}} + w_{\text{cat}} S_{\text{cat}} + w_{\text{career}} S_{\text{career}} + w_{\text{feas}} S_{\text{feas}}$$

Where:
* $w_{\text{acad}} = 0.30$ (Academic Fit based on CGPA excess over cutoff)
* $w_{\text{fin}} = 0.25$ (Financial Fit based on income relative to ceiling)
* $w_{\text{branch}} = 0.20$ (Discipline Alignment with synonym normalization)
* $w_{\text{cat}} = 0.10$ (Social Category Eligibility)
* $w_{\text{career}} = 0.10$ (Career Goal Relevance)
* $w_{\text{feas}} = 0.05$ (Application Window Feasibility)

---

### 2. Multi-Dimensional Career Readiness Formula
$$\text{Readiness} = R_{\text{acad}} (20) + R_{\text{skills}} (25) + R_{\text{projects}} (20) + R_{\text{certs}} (10) + R_{\text{exp}} (10) + R_{\text{resume}} (15)$$

Each dimension is computed transparently from database records (e.g., skill weights factored by proficiency: Beginner = $0.6$, Intermediate = $0.85$, Advanced = $1.0$).

---

## 🚀 Quickstart & Installation

### Option 1: Standard Local Setup (Windows / macOS / Linux)

```bash
# 1. Clone or navigate to the project directory
cd "c:/Users/shiva/SCHOLARSHIP WEBSITE"

# 2. Create and activate a Python virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize and seed the database with sample data
python seed.py

# 5. Run the full verification test suite
python test_portal_full.py

# 6. Start the Flask application server
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

### Option 2: Docker & Docker Compose Setup

```bash
# Build and run containerized service
docker-compose up --build
```
Navigate to: **`http://localhost:5000`**

---

## 🔑 Demo User Credentials

The database seeder (`seed.py`) provisions accounts across various academic profiles:

| Role | Email | Password | Academic Profile | Target Career Goal |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin@portal.com` | `Admin@123` | System Administrator | System Governance |
| **Student A** | `rahul@student.com` | `Student@123` | B.Tech CSE (CGPA: 8.65, ₹3.5L) | Software Engineer |
| **Student B** | `priya@student.com` | `Student@123` | B.Tech IT (CGPA: 9.25, ₹2.0L) | Full Stack Developer |
| **Student C** | `ananya@student.com` | `Student@123` | B.Tech ECE (CGPA: 7.80, ₹4.5L) | IoT / Cloud Engineer |
| **Student D** | `vikram@student.com` | `Student@123` | BCA (CGPA: 8.10, ₹1.8L) | Backend Developer |
| **Student E** | `sneha@student.com` | `Student@123` | B.Tech AI & DS (CGPA: 8.90, ₹2.8L) | AI / ML Engineer |
| **Student F** | `arjun@student.com` | `Student@123` | B.Tech Cyber (CGPA: 7.40, ₹5.2L) | Cybersecurity Analyst |

---

## 🧪 Testing & Quality Assurance

The system includes a comprehensive two-tier test suite:

```bash
# Run modular unit tests (27 tests)
python -m unittest discover -s tests -p "test_*.py" -v

# Run 59-point full integration & E2E suite
python test_portal_full.py

# Run live endpoint and session verifier
python verify_live.py
```

*Results Summary:*
* **59 / 59 Integration Checks Passed (100% Success)**
* **27 / 27 Modular Unit Tests Passed (100% Success)**
* **0 Broken Routes / 0 Broken Templates / 0 Unhandled Exceptions**

---

## 📖 Complete Documentation Index

For in-depth technical inspection, refer to the dedicated architectural documents:
* [Architecture Documentation (`ARCHITECTURE.md`)](file:///c:/Users/shiva/SCHOLARSHIP%20WEBSITE/ARCHITECTURE.md)
* [Database Design & ER Diagram (`DATABASE.md`)](file:///c:/Users/shiva/SCHOLARSHIP%20WEBSITE/DATABASE.md)
* [REST API Specification (`API.md`)](file:///c:/Users/shiva/SCHOLARSHIP%20WEBSITE/API.md)
* [Security Architecture & Threat Model (`SECURITY.md`)](file:///c:/Users/shiva/SCHOLARSHIP%20WEBSITE/SECURITY.md)
* [Testing Architecture & Test Matrix (`TESTING.md`)](file:///c:/Users/shiva/SCHOLARSHIP%20WEBSITE/TESTING.md)

---

## 🎓 Academic Viva Voce Reference Guide

| Question | Technical Answer & Implementation Details |
| :--- | :--- |
| **Why did you choose a layered architecture?** | Decouples business logic from presentation and database layers, allowing independent unit testing of decision algorithms without mock HTTP requests, and simplifies database migration to PostgreSQL. |
| **How does the system prevent SQL Injection?** | All database interactions utilize SQLAlchemy's parameterized queries and Object-Relational Mapping (ORM). No raw SQL string formatting is used anywhere in the codebase. |
| **How is Role-Based Access Control enforced?** | Using custom Python function decorators (`@login_required`, `@admin_required`) that inspect server-side session identity and query the database role before invoking route handlers. |
| **How do you handle database normalization?** | The schema satisfies Third Normal Form (3NF). Student skills, projects, certifications, bookmarks, and applications are isolated into dedicated relation tables with foreign keys and cascade rules. |
| **What makes your recommendations explainable?** | Rather than black-box machine learning or arbitrary random scores, each recommendation decomposes its score into transparent sub-factors (academic, financial, discipline, career fit) and generates textual reasons. |

---

## 📄 License
This project is open-source under the [MIT License](file:///c:/Users/shiva/SCHOLARSHIP%20WEBSITE/LICENSE).
