# Database Design & Relational Engineering

## Student Career & Scholarship Portal
**A Highly Normalized 3NF Relational Data Architecture for Decision Support & Opportunity Management**

---

## 1. Database Architecture Overview

The database is designed according to **Third Normal Form (3NF)** principles to eliminate data redundancy, prevent update/delete anomalies, and ensure data integrity across student portfolios, opportunity listings, applications, and system audits.

### Key Architectural Characteristics:
* **Relational Normalization**: User identity, student academic profiles, skill proficiencies, project portfolios, and certifications are decoupled into dedicated relational tables with explicit foreign key constraints.
* **Referential Integrity**: Cascading deletions (`ON DELETE CASCADE`) ensure child entities (such as profile details, user applications, saved opportunities, and notifications) are cleaned up reliably when parent user records are purged.
* **Targeted Indexing**: Single and composite indexes are deployed on high-cardinality search, filter, and deadline fields to ensure $O(\log n)$ or $O(1)$ query execution even at scale.
* **Database Portability**: The schema is written with standard SQLAlchemy ORM constructs, allowing seamless transition from development (**SQLite**) to production enterprise DBMS (**PostgreSQL**) with zero code refactoring.

---

## 2. Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o| STUDENT_PROFILES : "has profile (1:1)"
    USERS ||--o{ APPLICATIONS : "submits (1:N)"
    USERS ||--o{ SAVED_OPPORTUNITIES : "bookmarks (1:N)"
    USERS ||--o{ NOTIFICATIONS : "receives (1:N)"
    USERS ||--o{ ROADMAP_PROGRESS : "tracks (1:N)"
    USERS ||--o{ ADMIN_ACTION_LOGS : "performs (1:N)"

    STUDENT_PROFILES ||--o{ SKILLS : "owns (1:N)"
    STUDENT_PROFILES ||--o{ PROJECTS : "showcases (1:N)"
    STUDENT_PROFILES ||--o{ CERTIFICATIONS : "holds (1:N)"

    SCHOLARSHIPS ||--o{ APPLICATIONS : "associated with"
    INTERNSHIPS ||--o{ APPLICATIONS : "associated with"
    COURSES ||--o{ APPLICATIONS : "associated with"

    SCHOLARSHIPS ||--o{ SAVED_OPPORTUNITIES : "bookmarked as"
    INTERNSHIPS ||--o{ SAVED_OPPORTUNITIES : "bookmarked as"
    COURSES ||--o{ SAVED_OPPORTUNITIES : "bookmarked as"

    USERS {
        int id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    STUDENT_PROFILES {
        int id PK
        int user_id FK,UK
        string full_name
        string phone
        string branch
        int graduation_year
        float cgpa
        float family_income
        string category
        string career_goal
        string preferred_domain
        string resume_url
        string github_url
        string linkedin_url
        datetime created_at
        datetime updated_at
    }

    SKILLS {
        int id PK
        int profile_id FK
        string skill_name
        string proficiency_level
        datetime created_at
    }

    PROJECTS {
        int id PK
        int profile_id FK
        string title
        text description
        string tech_stack
        string github_link
        string live_link
        datetime created_at
    }

    CERTIFICATIONS {
        int id PK
        int profile_id FK
        string certificate_name
        string issuing_org
        date issue_date
        string credential_url
        datetime created_at
    }

    SCHOLARSHIPS {
        int id PK
        string title
        string provider
        float amount
        date deadline
        text description
        float minimum_cgpa
        float max_family_income
        string eligible_branches
        string eligible_categories
        text required_documents
        string application_url
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    INTERNSHIPS {
        int id PK
        string title
        string company
        string role_domain
        string location
        string work_mode
        float stipend
        date deadline
        text description
        string required_skills
        string eligible_branches
        float minimum_cgpa
        string application_url
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    COURSES {
        int id PK
        string title
        string provider
        string domain
        string difficulty_level
        float duration_hours
        string skills_taught
        string course_url
        float rating
        boolean is_free
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    APPLICATIONS {
        int id PK
        int user_id FK
        string opportunity_type
        int opportunity_id
        string status
        date applied_date
        date deadline
        text notes
        datetime updated_at
    }

    SAVED_OPPORTUNITIES {
        int id PK
        int user_id FK
        string opportunity_type
        int opportunity_id
        datetime saved_at
    }

    NOTIFICATIONS {
        int id PK
        int user_id FK
        string title
        text message
        string notification_type
        string priority
        string action_url
        boolean is_read
        datetime created_at
    }

    ROADMAP_PROGRESS {
        int id PK
        int user_id FK
        string career_role
        string roadmap_item
        string status
        datetime completed_at
        datetime updated_at
    }

    ADMIN_ACTION_LOGS {
        int id PK
        int admin_id FK
        string action
        string target_entity
        int target_id
        text details
        string ip_address
        datetime timestamp
    }
```

---

## 3. Comprehensive Data Dictionary

### Table 1: `users`
Stores credentials, core authentication states, and role classification.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE, INDEXED | User login email address |
| `password_hash` | VARCHAR(256) | NOT NULL | Werkzeug-salted PBKDF2:SHA256 password hash |
| `role` | VARCHAR(20) | NOT NULL, DEFAULT 'student' | Role: `'student'` or `'admin'` |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft account status toggle |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Registration timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Timestamp of last credential update |

---

### Table 2: `student_profiles`
Maintains demographic, academic, financial, and target career preferences for students.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique profile identifier |
| `user_id` | INTEGER | NOT NULL, UNIQUE, FK (`users.id` ON DELETE CASCADE) | 1:1 foreign key binding to user account |
| `full_name` | VARCHAR(100) | NOT NULL | Student's formal name |
| `phone` | VARCHAR(20) | NULLABLE | Contact telephone number |
| `branch` | VARCHAR(80) | NOT NULL, INDEXED | Engineering discipline (e.g., Computer Science, ECE) |
| `graduation_year` | INTEGER | NULLABLE | Expected year of degree completion |
| `cgpa` | FLOAT | NOT NULL, INDEXED, CHECK (`0.0 <= cgpa <= 10.0`) | Cumulative Grade Point Average (10-point scale) |
| `family_income` | FLOAT | NOT NULL, CHECK (`family_income >= 0`) | Annual family income in INR (₹) |
| `category` | VARCHAR(50) | NOT NULL, DEFAULT 'General' | Social reservation category (General, OBC, SC, ST, EWS) |
| `career_goal` | VARCHAR(100) | NULLABLE, INDEXED | Desired career target (e.g., Software Engineer, Data Scientist) |
| `preferred_domain`| VARCHAR(100) | NULLABLE | Industry vertical of interest |
| `resume_url` | VARCHAR(255) | NULLABLE | Link to uploaded or external PDF resume |
| `github_url` | VARCHAR(255) | NULLABLE | Student's GitHub profile URL |
| `linkedin_url` | VARCHAR(255) | NULLABLE | Student's LinkedIn profile URL |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Profile initialization timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Last profile update timestamp |

---

### Table 3: `skills`
Itemized inventory of technical proficiencies linked to a student's profile.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique skill record ID |
| `profile_id` | INTEGER | NOT NULL, FK (`student_profiles.id` ON DELETE CASCADE) | Foreign key binding to student profile |
| `skill_name` | VARCHAR(50) | NOT NULL, INDEXED | Canonical skill name (e.g., Python, SQL, Docker) |
| `proficiency_level`| VARCHAR(20) | NOT NULL, DEFAULT 'Beginner' | Level: `'Beginner'`, `'Intermediate'`, `'Advanced'` |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Skill addition timestamp |

*Unique Composite Constraint: `(profile_id, skill_name)` prevents duplicate skill declarations.*

---

### Table 4: `projects`
Portfolio projects showcased by students.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique project ID |
| `profile_id` | INTEGER | NOT NULL, FK (`student_profiles.id` ON DELETE CASCADE) | Foreign key binding to student profile |
| `title` | VARCHAR(120) | NOT NULL | Project title |
| `description` | TEXT | NULLABLE | Technical summary of project functionality |
| `tech_stack` | VARCHAR(255) | NULLABLE | Comma-separated list of technologies used |
| `github_link` | VARCHAR(255) | NULLABLE | Repository URL |
| `live_link` | VARCHAR(255) | NULLABLE | Live deployment URL |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Project creation timestamp |

---

### Table 5: `certifications`
Accredited certifications achieved by students.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique certification ID |
| `profile_id` | INTEGER | NOT NULL, FK (`student_profiles.id` ON DELETE CASCADE) | Foreign key binding to student profile |
| `certificate_name`| VARCHAR(150) | NOT NULL | Name of certification or credential |
| `issuing_org` | VARCHAR(120) | NOT NULL | Issuing authority (e.g., AWS, Coursera, Google) |
| `issue_date` | DATE | NULLABLE | Date credential was awarded |
| `credential_url` | VARCHAR(255) | NULLABLE | Verification link or certificate URL |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Certification timestamp |

---

### Table 6: `scholarships`
Financial grant and scholarship opportunities.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique scholarship ID |
| `title` | VARCHAR(150) | NOT NULL, INDEXED | Scholarship award title |
| `provider` | VARCHAR(120) | NOT NULL | Sponsoring body or organization |
| `amount` | FLOAT | NOT NULL | Financial grant amount in INR (₹) |
| `deadline` | DATE | NOT NULL, INDEXED | Application closing deadline |
| `description` | TEXT | NOT NULL | Overview and requirements |
| `minimum_cgpa` | FLOAT | NOT NULL, DEFAULT 0.0, INDEXED | Cutoff CGPA threshold |
| `max_family_income`| FLOAT | NOT NULL, DEFAULT 0.0, INDEXED | Maximum allowable annual income in INR (0 = no limit) |
| `eligible_branches`| VARCHAR(255) | NOT NULL, DEFAULT 'All' | Allowed engineering branches (comma-separated or 'All') |
| `eligible_categories`| VARCHAR(255) | NOT NULL, DEFAULT 'All' | Allowed categories (e.g., 'SC, ST, OBC, EWS, All') |
| `required_documents`| TEXT | NULLABLE | Necessary certificates and proof documents |
| `application_url` | VARCHAR(255) | NOT NULL | Direct portal submission link |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE, INDEXED | Publication status flag |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Listing creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Listing modification timestamp |

---

### Table 7: `internships`
Industry training, internships, and work placements.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique internship ID |
| `title` | VARCHAR(150) | NOT NULL, INDEXED | Internship role title |
| `company` | VARCHAR(120) | NOT NULL, INDEXED | Hiring organization |
| `role_domain` | VARCHAR(80) | NOT NULL, INDEXED | Technical domain (e.g., Software Engineering, AI/ML, Cloud) |
| `location` | VARCHAR(100) | NOT NULL | Location or remote status |
| `work_mode` | VARCHAR(30) | NOT NULL, DEFAULT 'Remote' | Mode: `'Remote'`, `'Hybrid'`, `'On-site'` |
| `stipend` | FLOAT | NOT NULL, DEFAULT 0.0 | Monthly stipend in INR (₹) |
| `deadline` | DATE | NOT NULL, INDEXED | Application deadline |
| `description` | TEXT | NOT NULL | Role duties and expectations |
| `required_skills` | VARCHAR(255) | NOT NULL | Comma-separated prerequisite technical skills |
| `eligible_branches`| VARCHAR(255) | NOT NULL, DEFAULT 'All' | Allowed branches |
| `minimum_cgpa` | FLOAT | NOT NULL, DEFAULT 0.0 | Academic threshold |
| `application_url` | VARCHAR(255) | NOT NULL | External or internal application link |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE, INDEXED | Availability flag |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Update timestamp |

---

### Table 8: `courses`
Curated skill-building courses and certifications for roadmap gap remediation.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique course ID |
| `title` | VARCHAR(150) | NOT NULL, INDEXED | Course name |
| `provider` | VARCHAR(100) | NOT NULL | Educational provider (e.g., Coursera, Udemy, MIT OCW) |
| `domain` | VARCHAR(80) | NOT NULL, INDEXED | Target subject domain |
| `difficulty_level`| VARCHAR(30) | NOT NULL, DEFAULT 'Beginner' | Level: `'Beginner'`, `'Intermediate'`, `'Advanced'` |
| `duration_hours` | FLOAT | NOT NULL, DEFAULT 10.0 | Estimated completion hours |
| `skills_taught` | VARCHAR(255) | NOT NULL | Comma-separated skills acquired from course |
| `course_url` | VARCHAR(255) | NOT NULL | Direct enrollment link |
| `rating` | FLOAT | NOT NULL, DEFAULT 4.5 | Community rating (1.0 - 5.0) |
| `is_free` | BOOLEAN | NOT NULL, DEFAULT TRUE | Free or paid designation |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Listing status flag |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Modification timestamp |

---

### Table 9: `applications`
7-stage student application lifecycle tracker.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique application tracking ID |
| `user_id` | INTEGER | NOT NULL, INDEXED, FK (`users.id` ON DELETE CASCADE) | Submitting student |
| `opportunity_type`| VARCHAR(20) | NOT NULL | Type: `'scholarship'`, `'internship'`, `'course'` |
| `opportunity_id` | INTEGER | NOT NULL | ID in corresponding opportunity table |
| `status` | VARCHAR(30) | NOT NULL, DEFAULT 'Applied', INDEXED | Status: `'Saved'`, `'Applied'`, `'Under Review'`, `'Shortlisted'`, `'Interview'`, `'Accepted'`, `'Rejected'` |
| `applied_date` | DATE | NOT NULL, DEFAULT UTC_TODAY | Date application was logged |
| `deadline` | DATE | NULLABLE | Cached opportunity closing deadline |
| `notes` | TEXT | NULLABLE | Personal notes or interview scheduling details |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Last stage update timestamp |

*Unique Composite Constraint: `(user_id, opportunity_type, opportunity_id)` enforces single active application per opportunity.*

---

### Table 10: `saved_opportunities`
Student bookmarks and saved listings.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique bookmark ID |
| `user_id` | INTEGER | NOT NULL, INDEXED, FK (`users.id` ON DELETE CASCADE) | Student user ID |
| `opportunity_type`| VARCHAR(20) | NOT NULL | Type: `'scholarship'`, `'internship'`, `'course'` |
| `opportunity_id` | INTEGER | NOT NULL | ID of bookmarked opportunity |
| `saved_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Bookmark timestamp |

*Unique Composite Constraint: `(user_id, opportunity_type, opportunity_id)` prevents duplicate bookmarking.*

---

### Table 11: `notifications`
Tiered user notifications and deadline alert feed.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique notification ID |
| `user_id` | INTEGER | NOT NULL, INDEXED, FK (`users.id` ON DELETE CASCADE) | Target student recipient |
| `title` | VARCHAR(120) | NOT NULL | Notification headline |
| `message` | TEXT | NOT NULL | Body message text |
| `notification_type`| VARCHAR(50) | NOT NULL, DEFAULT 'GENERAL' | Category: `'DEADLINE'`, `'MATCH'`, `'STATUS_UPDATE'`, `'PROFILE'` |
| `priority` | VARCHAR(20) | NOT NULL, DEFAULT 'INFO' | Tier: `'INFO'`, `'WARNING'`, `'IMPORTANT'` |
| `action_url` | VARCHAR(255) | NULLABLE | Contextual redirect link |
| `is_read` | BOOLEAN | NOT NULL, DEFAULT FALSE, INDEXED | Read receipt indicator |
| `created_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Dispatch timestamp |

---

### Table 12: `roadmap_progress`
Dynamic milestone completion tracker for career pathways.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique progress record ID |
| `user_id` | INTEGER | NOT NULL, INDEXED, FK (`users.id` ON DELETE CASCADE) | Student tracking progress |
| `career_role` | VARCHAR(80) | NOT NULL, INDEXED | Specific career pathway (e.g., Software Engineer, Data Scientist) |
| `roadmap_item` | VARCHAR(120) | NOT NULL | Milestone topic key (e.g., 'Data Structures & Algorithms') |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'Completed' | Status: `'Completed'`, `'In Progress'`, `'Not Started'` |
| `completed_at` | DATETIME | NULLABLE | Timestamp of milestone completion |
| `updated_at` | DATETIME | NOT NULL, DEFAULT UTC_NOW | Last status update timestamp |

*Unique Composite Constraint: `(user_id, career_role, roadmap_item)` maintains exact status per milestone.*

---

### Table 13: `admin_action_logs`
Immutable compliance audit trail recording all administrative operations.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique log entry ID |
| `admin_id` | INTEGER | NOT NULL, INDEXED, FK (`users.id`) | Administrator who executed the action |
| `action` | VARCHAR(80) | NOT NULL, INDEXED | Operation name (e.g., 'CREATE_SCHOLARSHIP', 'DELETE_COURSE') |
| `target_entity` | VARCHAR(50) | NOT NULL, INDEXED | Entity type: `'Scholarship'`, `'Internship'`, `'Course'`, `'User'`, `'Application'` |
| `target_id` | INTEGER | NULLABLE | Primary key ID of affected record |
| `details` | TEXT | NULLABLE | JSON or text audit details of modified attributes |
| `ip_address` | VARCHAR(45) | NULLABLE | Client IPv4/IPv6 address |
| `timestamp` | DATETIME | NOT NULL, DEFAULT UTC_NOW, INDEXED | Immutable action timestamp |

---

## 4. Query Optimization & Indexing Strategy

To guarantee rapid query response times under high concurrency and growing datasets, specialized indexes have been defined:

1. **Academic Range Queries**:
   - `idx_student_profile_cgpa_income` on `student_profiles (cgpa, family_income)` accelerates eligibility pre-filtering.
2. **Deadline-Driven Sorting & Filtering**:
   - `idx_scholarship_deadline_active` on `scholarships (deadline, is_active)`
   - `idx_internship_deadline_active` on `internships (deadline, is_active)`
   Allows the priority alert engine to fetch upcoming deadlines in $O(\log n)$ time.
3. **Domain & Role Categorization**:
   - `idx_internship_domain` on `internships (role_domain)`
   - `idx_course_domain_rating` on `courses (domain, rating DESC)`
4. **User-Scoped Join Speed**:
   - `idx_application_user_status` on `applications (user_id, status)`
   - `idx_saved_user_opp` on `saved_opportunities (user_id, opportunity_type)`
   - `idx_notification_user_unread` on `notifications (user_id, is_read)`
5. **Governance Audit Queries**:
   - `idx_admin_log_entity_time` on `admin_action_logs (target_entity, timestamp DESC)`

---

## 5. Production PostgreSQL Readiness

To migrate from local development (SQLite) to production PostgreSQL:
1. Update `.env` with the PostgreSQL connection string:
   ```env
   DATABASE_URL=postgresql+psycopg2://portal_user:SecurePassword123@localhost:5432/career_portal_db
   ```
2. Run database initialization/migration:
   ```bash
   python seed.py
   ```
All data types, boolean toggles, `DateTime` defaults, cascading constraints, and text fields are strictly standard SQL compliant.
