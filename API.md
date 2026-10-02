# REST API Specification & Integration Guide

## Student Career & Scholarship Portal
**Standardized JSON REST API Layer with Uniform Payloads, Error Contracts & Auth Guards**

---

## 1. API Architecture & Standards

All REST endpoints reside under the `/api/` prefix. The API layer provides a decoupled interface that can serve modern web applications, mobile apps, and third-party institutional consumers.

### Uniform Response Format

#### 1. Success Response (`200 OK`, `201 Created`):
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}
```

#### 2. Error Response (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Detailed description of the validation failure"
  }
}
```

---

## 2. Authentication & Session Context

The API utilizes secure HTTP-only session cookies (`session['user_id']`).
* Unauthenticated requests to protected endpoints receive `401 Unauthorized`.
* When testing via `curl` or Postman, include the session cookie returned from `/login`.

---

## 3. Endpoints Directory

| Category | Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Catalog** | `GET` | `/api/scholarships` | Public | List all active scholarship grants |
| **Catalog** | `GET` | `/api/scholarships/<id>` | Public | Get granular details of a scholarship |
| **Catalog** | `GET` | `/api/internships` | Public | List all active industry internships |
| **Catalog** | `GET` | `/api/internships/<id>` | Public | Get granular details of an internship |
| **Catalog** | `GET` | `/api/courses` | Public | List all skill-gap remedy courses |
| **Catalog** | `GET` | `/api/courses/<id>` | Public | Get granular details of a course |
| **Intelligence** | `GET` | `/api/recommendations` | Student | Unified multi-criteria recommendations |
| **Intelligence** | `GET` | `/api/dashboard` | Student | Profile strength, readiness & metrics |
| **Intelligence** | `POST` | `/api/check-eligibility` | Student | Explainable scholarship eligibility engine |
| **Lifecycle** | `POST` | `/api/save-opportunity` | Student | Bookmark an opportunity |
| **Lifecycle** | `POST` | `/api/remove-saved` | Student | Remove a saved bookmark |
| **Lifecycle** | `POST` | `/api/applications` | Student | Create or log an opportunity application |
| **Lifecycle** | `POST` | `/api/update-application-status` | Student | Move application across 7 pipeline stages |
| **Roadmap** | `POST` | `/api/roadmap-progress` | Student | Toggle milestone completion per career pathway |
| **Alerts** | `GET` | `/api/notifications` | Student | Fetch tiered notifications and unread count |
| **Alerts** | `POST` | `/api/notifications/mark-read`| Student | Mark notifications as read |
| **Search** | `GET` | `/api/search?q={query}` | Public | Multi-entity global search across opportunities |

---

## 4. Granular Endpoint Documentation

### 4.1 Opportunity Catalogs

#### `GET /api/scholarships`
Returns active scholarships ordered by closing deadline.

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Scholarships fetched successfully",
  "data": [
    {
      "id": 1,
      "title": "National Merit STEM Scholarship 2026",
      "provider": "Ministry of Education & Science",
      "amount": 75000.0,
      "deadline": "2026-11-15",
      "minimum_cgpa": 8.0,
      "max_family_income": 600000.0,
      "eligible_branches": "Computer Science, Information Technology, Electronics",
      "eligible_categories": "General, OBC, SC, ST, EWS",
      "application_url": "https://scholarships.gov.in"
    }
  ]
}
```

---

### 4.2 Intelligent Decision Systems

#### `POST /api/check-eligibility`
Executes the deterministic weighted matching algorithm against the authenticated student's profile.

**Sample Request:**
```json
{
  "scholarship_id": 1
}
```

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Eligibility calculation completed",
  "data": {
    "scholarship": {
      "id": 1,
      "title": "National Merit STEM Scholarship 2026",
      "amount": 75000.0
    },
    "result": {
      "eligible": true,
      "score": 92.5,
      "match_percentage": 92.5,
      "academic_score": 30.0,
      "financial_score": 25.0,
      "branch_score": 20.0,
      "category_score": 10.0,
      "reasons": [
        "CGPA (8.80) satisfies minimum requirement (8.00)",
        "Family income (₹450,000) is within ceiling (₹600,000)",
        "Branch 'Computer Science' matches STEM requirements",
        "Category 'General' is eligible"
      ],
      "missing_criteria": [],
      "recommendations": [
        "High priority grant: Apply before 2026-11-15.",
        "Prepare attested income certificate and semester grade cards."
      ]
    }
  }
}
```

---

#### `GET /api/recommendations`
Returns personalized recommendations for scholarships, internships, and skill gap remediation courses, along with a top-priority action item.

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "priorities": [
      {
        "category": "DEADLINE",
        "level": "High",
        "title": "National Merit STEM Scholarship 2026",
        "action": "Submit Application",
        "url": "/scholarship/1",
        "due_in_days": 49
      }
    ],
    "scholarships": [
      {
        "id": 1,
        "name": "National Merit STEM Scholarship 2026",
        "provider": "Ministry of Education & Science",
        "amount": 75000.0,
        "match_score": 92.5,
        "eligible": true,
        "reasons": ["Branch matches target discipline", "CGPA exceeds threshold"],
        "explanation": "High academic alignment with strong financial qualification."
      }
    ],
    "internships": [
      {
        "id": 2,
        "title": "Software Engineer Intern (Cloud & Backend)",
        "company": "Amazon Web Services (AWS)",
        "stipend": 65000.0,
        "score": 88.0,
        "matched_skills": ["Python", "SQL", "Git"],
        "match_explanation": "Matches 3 of your core technical skills and your target role."
      }
    ],
    "courses": [
      {
        "id": 4,
        "name": "Distributed Systems & Cloud Architecture Masterclass",
        "platform": "Coursera",
        "price": "Free",
        "rating": 4.8,
        "is_gap_remedy": true,
        "reason": "Teaches Docker and Kubernetes which are missing from your profile for Cloud Engineer."
      }
    ]
  }
}
```

---

#### `GET /api/dashboard`
Returns live calculated analytics for the student dashboard.

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "profile_strength": 85.0,
    "career_readiness": {
      "score": 78.4,
      "academic_score": 17.6,
      "skill_score": 22.5,
      "project_score": 15.0,
      "certification_score": 8.0,
      "experience_score": 6.5,
      "resume_score": 8.8,
      "role": "Software Engineer",
      "summary": "Strong foundational candidate with high project alignment."
    },
    "application_analytics": {
      "total": 5,
      "applied": 2,
      "under_review": 1,
      "shortlisted": 1,
      "interview": 0,
      "accepted": 1,
      "rejected": 0,
      "acceptance_rate": 20.0
    },
    "saved_count": 4
  }
}
```

---

### 4.3 Lifecycle & Roadmap Operations

#### `POST /api/applications`
Submits or records an application.

**Sample Request:**
```json
{
  "opportunity_type": "internship",
  "opportunity_id": 2,
  "status": "Applied",
  "notes": "Applied via AWS careers portal. Reference #AWS-2026-991"
}
```

**Sample Response (`201 Created`):**
```json
{
  "success": true,
  "message": "Application logged successfully",
  "data": {
    "id": 12,
    "user_id": 2,
    "opportunity_type": "internship",
    "opportunity_id": 2,
    "status": "Applied",
    "applied_date": "2026-09-27"
  }
}
```

---

#### `POST /api/update-application-status`
Updates the pipeline status of an existing application.

**Sample Request:**
```json
{
  "application_id": 12,
  "status": "Interview",
  "notes": "Round 1 Technical Interview scheduled for next Tuesday."
}
```

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Application status updated to Interview",
  "data": {
    "id": 12,
    "status": "Interview",
    "notes": "Round 1 Technical Interview scheduled for next Tuesday."
  }
}
```

---

#### `POST /api/roadmap-progress`
Toggles milestone completion status for a specific career pathway.

**Sample Request:**
```json
{
  "career_role": "Full Stack Developer",
  "stage_id": "Data Structures & Algorithms",
  "completed": true
}
```

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Stage Data Structures & Algorithms status updated",
  "data": {
    "role": "Full Stack Developer",
    "completed_items": 4,
    "total_items": 7,
    "progress_percentage": 57.1
  }
}
```

---

### 4.4 Global Instant Search

#### `GET /api/search?q=Python`
Performs multi-entity ILIKE search across scholarships, internships, and courses.

**Sample Response (`200 OK`):**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "query": "Python",
    "results": {
      "scholarships": [],
      "internships": [
        {
          "id": 1,
          "title": "AI & Data Science Engineering Intern",
          "subtitle": "Microsoft",
          "badge": "₹50,000/mo",
          "url": "/internship/1"
        }
      ],
      "courses": [
        {
          "id": 1,
          "title": "Complete Python Bootcamp from Zero to Hero",
          "subtitle": "Coursera",
          "badge": "Free",
          "url": "/courses"
        }
      ]
    }
  }
}
```

---

## 5. Error Code Reference

| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `UNAUTHORIZED` | `401` | Missing or expired session cookie. |
| `FORBIDDEN` | `403` | Non-admin user attempted an administrative action. |
| `NOT_FOUND` | `404` | Requested record does not exist in the database. |
| `VALIDATION_ERROR`| `400` | Input payload missing mandatory fields or invalid values. |
| `DUPLICATE_ERROR` | `409` | Unique constraint violation (e.g., duplicate application). |
| `SERVER_ERROR` | `500` | Unhandled internal exception (logged to server logs). |
