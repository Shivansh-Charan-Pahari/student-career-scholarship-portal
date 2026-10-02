# Production Deployment Guide: Student Career & Scholarship Portal

This document outlines the deployment strategy for deploying the **Student Career & Scholarship Portal** to **Vercel** with a persistent **PostgreSQL** database (via Neon or Supabase).

---

## 1. Architectural Overview

```
Client (Browser)
    │
    ▼
Vercel Edge Network / CDN
    │
    ├── Static Assets (/static/*) ─── Served directly by Vercel Edge
    │
    └── Dynamic Requests (/*) ────── Routed to api/index.py (Flask WSGI Serverless Function)
                                             │
                                             ▼
                                  SQLAlchemy Connection Pool
                                             │
                                             ▼
                                  PostgreSQL Cloud Database
                                   (Neon / Supabase Serverless)
```

---

## 2. Serverless Storage Principles & Vercel Considerations

1. **No Ephemeral SQLite in Production**:
   - Vercel functions execute in stateless, ephemeral serverless execution containers.
   - Any local SQLite file written to `/tmp` or the project root will not persist across function invocations or concurrent instances.
   - Therefore, production deployments **must** connect to a persistent managed PostgreSQL database using the `DATABASE_URL` environment variable.

2. **Database Connection String Handling**:
   - `config.py` automatically normalizes `postgres://` connection strings (commonly provided by older platforms/Supabase) to `postgresql://` as required by modern SQLAlchemy 2.0+ and `psycopg2-binary`.

3. **Safe Idempotent Startup**:
   - On cold start, `app.py` executes `db.create_all()` which creates missing tables without modifying or dropping existing production records.
   - Administrator bootstrap is executed idempotently using `AuthService.bootstrap_admin_from_env()`. Existing admin accounts and passwords are preserved.

---

## 3. Production Prerequisites

Before deploying to Vercel, ensure you have:
1. A **Vercel Account** ([vercel.com](https://vercel.com))
2. A **PostgreSQL Database** instance from a cloud provider:
   - **Neon** (Recommended - [neon.tech](https://neon.tech) / Vercel Marketplace)
   - **Supabase** ([supabase.com](https://supabase.com) / Vercel Marketplace)
3. A strong 32+ character random `SECRET_KEY`.

---

## 4. Environment Variables Reference

Configure the following environment variables in your Vercel Project Settings (**Settings > Environment Variables**):

| Variable Name | Required | Example / Description |
|---|---|---|
| `FLASK_APP` | Yes | `app.py` |
| `FLASK_ENV` | Yes | `production` |
| `SECRET_KEY` | Yes | `f7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0` (Generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | Yes | `postgresql://neondb_owner:password@ep-sample-123.us-east-2.aws.neon.tech/neondb?sslmode=require` |
| `ADMIN_EMAIL` | Yes | `admin@portal.com` (Your secure admin login email) |
| `ADMIN_INITIAL_PASSWORD` | Yes | `YourStrongAdminPassword2026!` (Used only for initial creation) |
| `ADMIN_BOOTSTRAP_SECRET` | Optional | Optional token for programmatic admin provisioning |
| `SESSION_COOKIE_SECURE` | Yes | `True` (Enforces HTTPS-only cookies in production) |

---

## 5. Step-by-Step Deployment Workflows

### Method A: Deploy via GitHub & Vercel Dashboard (Recommended)

1. **Push Codebase to GitHub**:
   ```bash
   git add .
   git commit -m "feat: production deployment readiness with PostgreSQL support"
   git push origin main
   ```

2. **Import to Vercel**:
   - Log into [Vercel Dashboard](https://vercel.com).
   - Click **Add New... > Project**.
   - Select your GitHub repository.

3. **Configure Project Settings**:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (leave default)
   - **Build Command**: Leave empty (handled by `@vercel/python`)
   - **Output Directory**: Leave empty

4. **Add Environment Variables**:
   - Add each variable from the table in Section 4.

5. **Deploy**:
   - Click **Deploy**.
   - Vercel will install dependencies from `requirements.txt`, configure `api/index.py` as a serverless function, and provision your live HTTPS URL.

---

### Method B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login and Link Project**:
   ```bash
   vercel login
   vercel link
   ```

3. **Set Environment Variables**:
   ```bash
   vercel env add SECRET_KEY
   vercel env add DATABASE_URL
   vercel env add ADMIN_EMAIL
   vercel env add ADMIN_INITIAL_PASSWORD
   vercel env add SESSION_COOKIE_SECURE
   ```

4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## 6. Post-Deployment Verification & Smoke Testing

Once deployed, perform the following verification checks on your production URL:

1. **Public Catalog Access**:
   - Visit `https://your-app.vercel.app/`
   - Visit `https://your-app.vercel.app/scholarships`
   - Visit `https://your-app.vercel.app/internships`
   - Visit `https://your-app.vercel.app/courses`

2. **Student Registration & Session**:
   - Register a new student account at `/register`.
   - Update academic details on `/profile`.
   - Add technical skills and capstone projects.
   - Verify that the Profile Strength Meter updates.

3. **Opportunity Applications & Bookmarks**:
   - Apply for a scholarship.
   - Navigate to `/applications` and verify the status pipeline.
   - Bookmark an internship and view it under `/saved`.

4. **Admin Authentication & Management**:
   - Visit `/admin/login` and log in with your `ADMIN_EMAIL` and `ADMIN_INITIAL_PASSWORD`.
   - Verify KPI counts on `/admin/dashboard`.
   - Create a test scholarship and verify it is visible on `/scholarships`.
   - Inspect `/admin/audit-logs` to confirm the creation event was cryptographically logged.

5. **Data Persistence Verification**:
   - Log out of your session.
   - Clear your browser cookies or open a private window.
   - Log back in with the student account created in Step 2.
   - Verify that all profile fields, skills, and applications remain fully intact.

---

## 7. Seeding Production Database with Demo Data (Optional)

To populate an initial catalog of scholarships, internships, and courses on a fresh PostgreSQL database:

```bash
# Run the seed script locally pointing to your production DATABASE_URL
DATABASE_URL="postgresql://user:password@your-postgres-host/neondb?sslmode=require" python seed.py
```

The script runs safely and reports:
- Administrator account provisioned
- 16 verified demo scholarships
- 16 industry internships
- 16 curated courses
- Sample application workflows

---

## 8. Troubleshooting & Maintenance

| Symptom | Probable Root Cause | Resolution |
|---|---|---|
| `500 Internal Server Error` on cold start | `DATABASE_URL` is invalid or unreachable from Vercel lambda | Ensure PostgreSQL host permits external SSL connections (`sslmode=require`). Verify credentials. |
| SQLAlchemy error: `NoSuchModuleError: postgres` | Older `postgres://` URL scheme passed | `config.py` automatically normalizes to `postgresql://`. Ensure latest code is deployed. |
| Admin login fails after redeployment | Admin credentials altered | Verify `ADMIN_EMAIL` in Vercel settings. Passwords are hash-verified with Werkzeug PBKDF2. |
| Static files return 404 | Incorrect Vercel routing rule | Verify `vercel.json` contains `/static/(.*)` route mapping. |
