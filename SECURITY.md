# Security Architecture & Threat Modeling

## Student Career & Scholarship Portal
**Enterprise Security Guidelines, Role-Based Access Controls (RBAC), and OWASP Safeguards**

---

## 1. Security Architecture Overview

The platform implements a defense-in-depth security model across authentication, session handling, authorization, database interactions, and HTTP communications.

```
+-------------------------------------------------------------------------+
|                         HTTP Transport Layer                            |
|     HTTPS + Security Headers (HSTS, CSP, X-Frame-Options, Sniff Guard)  |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                       Authentication & Session                          |
|   PBKDF2 Password Hashes + HTTP-Only Session Cookies + Session Scoping   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                     Role-Based Access Control (RBAC)                    |
|   @login_required, @admin_required, Student Horizontal Isolation Check   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         Data Integrity Layer                            |
|     SQLAlchemy Parameterized Queries (Anti-SQLi) + Jinja2 Escaping      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         Audit Logging Layer                             |
|          Immutable Admin Action Logs (IP, Entity, Delta, Timestamp)     |
+-------------------------------------------------------------------------+
```

---

## 2. Authentication & Credential Storage

### 2.1 Password Hashing Mechanism
* **Algorithm**: PBKDF2 with SHA-256 and cryptographic salting (via `werkzeug.security.generate_password_hash`).
* **Validation**: Constant-time hash verification via `check_password_hash` to prevent timing attacks.
* **Storage**: Passwords are never stored in plaintext. The database only stores a 256-character salted hash string.

### 2.2 Password Complexity Policies
Enforced at registration:
* Minimum 8 characters.
* Must contain uppercase and lowercase letters.
* Must contain numeric digits and special symbols (`@$!%*?&`).
* Mandatory password confirmation equality check.

### 2.3 Session Management & Expiration
* **Storage**: Server-side signed sessions using Flask's secure cookie mechanism.
* **Session Lifetime**: 30-day permanent session duration with automatic renewal on activity.
* **Session Invalidation**: Calling `/logout` explicitly destroys `session.clear()`, preventing session replay attacks.

---

## 3. Role-Based Access Control (RBAC)

Access is bifurcated into two mutually exclusive roles:
1. **`student`**: Authorized to manage their own profile, skills, bookmarks, roadmap, and applications.
2. **`admin`**: Authorized to publish/edit/delete opportunities, view sitewide analytics, inspect student rosters, and view audit trails.

### RBAC Decorators:

#### `@login_required`
```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
```

#### `@admin_required`
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this resource.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        user = db.session.get(User, session['user_id'])
        if not user or user.role != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function
```

### Horizontal Privilege Escalation Prevention
Students are strictly isolated to their own records:
* Profile updates enforce `user_id == session['user_id']`.
* Application updates verify `application.user_id == session['user_id']`.
* Bookmarks cannot be created or deleted for foreign users.

---

## 4. OWASP Top 10 Protections

| OWASP Vulnerability | Risk | Mitigation in Portal |
| :--- | :--- | :--- |
| **A01: Broken Access Control** | URL tampering to view admin or other student data. | Strict `@admin_required` guard, URL parameter ownership checks, returning `403 Forbidden`. |
| **A02: Cryptographic Failures** | Exposed credentials or weak hashes. | PBKDF2:SHA256 salted hashes, zero plaintext secrets in code, `.env` secret management. |
| **A03: Injection (SQLi)** | Malicious SQL inputs bypassing filters. | Exclusively parameterized queries and ORM abstractions via SQLAlchemy. No raw string interpolation in SQL queries. |
| **A04: Insecure Design** | Unexplainable or manipulatable scoring. | Deterministic mathematical scoring formulas, server-side data validation. |
| **A05: Security Misconfiguration** | Stack traces or debug information leaked in production. | Custom error handlers for `400`, `401`, `403`, `404`, and `500`. Debug mode disabled in production config. |
| **A06: Vulnerable Components** | Outdated or vulnerable third-party dependencies. | Pinned dependencies in `requirements.txt` based on modern Flask 3.1.3 and Werkzeug 3.1.8. |
| **A07: Identification & Auth Failures** | Brute force or credential stuffing. | Server-side validation, unique email constraints, secure session invalidation. |
| **A08: Software & Data Integrity** | Unauthorized modification of administrative data. | Immutable `AdminActionLog` recording all CRUD operations with IP logging. |
| **A09: Logging & Monitoring Failures** | Lack of visibility into security events. | Structured console and file logging for logins, registrations, status updates, and administrative modifications. |
| **A10: SSRF / Cross-Site Scripting (XSS)** | Injected malicious JavaScript in profile/project fields. | Jinja2 automatic HTML escaping enabled across all templates, explicit sanitize on text inputs. |

---

## 5. HTTP Security Headers Middleware

Applied automatically via Flask's `@app.after_request` hook:

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:;"
    )
    return response
```

---

## 6. Immutable Administrative Audit Logging

Every administrative operation triggers a non-repudiable audit event in `AdminActionLog`:

```python
AdminService.log_admin_action(
    admin_id=admin_user.id,
    action="CREATE_SCHOLARSHIP",
    target_entity="Scholarship",
    target_id=new_scholarship.id,
    details=f"Created grant '{new_scholarship.title}' with amount ₹{new_scholarship.amount}",
    ip_address=request.remote_addr
)
```

Audited events include:
* Creating, editing, and deleting Scholarships
* Creating, editing, and deleting Internships
* Creating, editing, and deleting Courses
* Modifying student application statuses from the admin panel
* Toggling student account active statuses

---

## 7. Environment & Secrets Management

Secrets are managed outside source control:
1. `.env` is listed in `.gitignore` and never committed.
2. A clean template `.env.example` provides default variable names.
3. Production setups override `SECRET_KEY` with a cryptographically strong 64-byte random hex string:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
