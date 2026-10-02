# Software Testing & Quality Assurance Suite

## Student Career & Scholarship Portal
**Comprehensive Testing Architecture, Test Matrix, Edge Cases & Verification Instructions**

---

## 1. Testing Philosophy & Framework

The platform is backed by a multi-tiered test suite ensuring algorithmic accuracy, role-based authorization security, database integrity, and REST API contract compliance.

### Testing Frameworks:
* **Standard Test Runner**: Python `unittest` / `pytest`
* **Test Isolation**: In-memory SQLite database (`sqlite:///:memory:`) configured with isolated application context per test fixture.
* **Coverage Scope**:
  * Unit Tests: Algorithmic decision engines (Eligibility, Readiness, Skill Gap, Recommendations)
  * Integration Tests: Flask Blueprint controllers, Service Layer orchestration, and RBAC guards
  * API Contract Tests: REST response schemas, HTTP status codes, and error formats
  * Edge-Case Tests: Extreme boundary conditions (zero values, missing profiles, expired opportunities, privilege bypass attempts)
  * End-to-End Verification: Complete student and admin user journey simulation

---

## 2. Test Suite Directory Structure

```
SCHOLARSHIP WEBSITE/
├── test_portal_full.py               # Comprehensive 59-point E2E Integration Suite
├── verify_live.py                    # Live HTTP Session & Endpoint Verifier
└── tests/                            # Modular Unit & Feature Tests
    ├── __init__.py
    ├── conftest.py                   # Pytest Fixtures & In-Memory App Setup
    ├── test_auth_service.py          # Authentication, Passwords & Validation Tests
    ├── test_eligibility_engine.py    # Scholarship Weighted Matching & Qualifier Tests
    ├── test_career_readiness.py      # 6-Dimension Readiness & Skill Gap Tests
    ├── test_applications.py          # 7-Stage Pipeline, Conversions & Bookmarks Tests
    ├── test_admin_and_rbac.py        # RBAC Authorization & Audit Trail Tests
    ├── test_api.py                   # REST API Endpoints & Error Schemas Tests
    └── test_edge_cases.py            # Extreme Boundaries & Security Escalation Tests
```

---

## 3. Test Modules & Coverage Matrix

### 3.1 `tests/test_auth_service.py`
Tests identity verification, credential hashing, and profile portfolio CRUD:
* Student registration with valid credentials.
* Duplicate email rejection (`400 Bad Request`).
* Weak password rejection (< 8 characters or missing required character classes).
* Profile update and dynamic profile strength recalculation.
* Technical skill additions, updates, and cascading removals.

### 3.2 `tests/test_eligibility_engine.py`
Tests deterministic scholarship scoring logic:
* Student meeting all criteria (CGPA, Income ceiling, Branch, Category) scores $>90\%$ with `eligible = True`.
* Student with CGPA below cutoff receives explicit failure reason in `reasons` list and `eligible = False`.
* Student with family income exceeding ceiling receives `Income exceeds limit` reason.
* Engineering discipline synonym normalization (e.g., `'CSE'` properly matches `'Computer Science'`).
* Branch matching verification for unrestricted (`'All'`) scholarships.

### 3.3 `tests/test_career_readiness.py`
Tests career engine, readiness metric calculation, and roadmaps:
* 6-dimensional readiness score calculation across Academic, Skills, Projects, Certifications, Experience, and Resume.
* Accurate skill gap computation: partition of required role skills into `have_skills` vs `missing_skills`.
* Career pathway roadmap generation across 7 defined roles (Software Engineer, Data Scientist, Frontend, Backend, AI/ML, Cloud, Cybersecurity).
* Milestone status persistence in `RoadmapProgress`.

### 3.4 `tests/test_applications.py`
Tests the 7-stage application tracking system:
* Creating initial application in `'Applied'` state.
* Progressing status across stages: `'Applied'` $\to$ `'Under Review'` $\to$ `'Interview'` $\to$ `'Accepted'`.
* Unique constraint validation preventing duplicate active applications for the same opportunity.
* Accurate live acceptance rate and shortlist conversion computation.
* Bookmark saving and duplicate bookmark prevention.

### 3.5 `tests/test_admin_and_rbac.py`
Tests Role-Based Access Control and governance:
* Unauthenticated access to `/admin` returns `302 Redirect` to login.
* Authenticated student access to `/admin` returns `403 Forbidden`.
* Administrator can successfully access `/admin`, create/edit/delete opportunities.
* Immutable `AdminActionLog` records created for all admin operations.
* Audit log viewer renders action history with IP address and target metadata.

### 3.6 `tests/test_api.py`
Tests REST JSON contracts:
* Public catalog endpoints (`/api/scholarships`, `/api/internships`, `/api/courses`).
* Authenticated endpoints return `401 Unauthorized` without session.
* `/api/check-eligibility` returns structured match score and explainable reasons.
* `/api/search` executes multi-entity keyword lookup and returns standard payload.
* Error responses conform strictly to `{ "success": false, "error": { "code": "...", "message": "..." } }`.

### 3.7 `tests/test_edge_cases.py`
Tests extreme boundary values:
* Boundary CGPA values (`cgpa = 0.0` and `cgpa = 10.0`).
* Zero family income (`family_income = 0.0`) handling for BPL/EWS verification.
* Student with zero skills: readiness engine handles gracefully without division by zero.
* Student with 25+ skills: readiness engine caps score properly at maximum dimension limits.
* Non-existent ID lookups return clean `404 Not Found` without stack traces.
* Privilege escalation attempts: Student B cannot alter Student A's application status.

---

## 4. How to Execute Tests

### 4.1 Run Modular Unit & Feature Tests (`tests/`)
Using Python's built-in unittest test runner:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
Or using pytest:
```bash
pytest tests/ -v
```

*Expected Output:*
```
Ran 27 tests in 0.85s
OK
```

---

### 4.2 Run Full 59-Point E2E Integration Suite (`test_portal_full.py`)
Executes comprehensive end-to-end assertions against the integrated application:
```bash
python test_portal_full.py
```

*Expected Output:*
```
================================================================================
ALL 59 VERIFICATION CHECKS PASSED PERFECTLY! (100% SUCCESS)
================================================================================
```

---

### 4.3 Run Live HTTP Session & Endpoint Verifier (`verify_live.py`)
Validates live web server responses, cookie sessions, form submissions, and JSON API payloads on the running instance:
```bash
python verify_live.py
```

*Expected Output:*
```
[SUCCESS] Verified 20+ live HTTP routes, sessions, RBAC guards, and REST endpoints with 0 errors!
```
