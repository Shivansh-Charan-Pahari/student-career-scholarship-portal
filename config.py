"""
Configuration Module for Student Career & Scholarship Portal
Handles environment-specific settings for Development, Testing, and Production.
Includes secure session cookie parameters, database connection normalization,
and admin bootstrap parameters.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Read .env file if it exists without requiring external dependencies
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def get_normalized_database_uri():
    """
    Returns normalized database URI.
    Fixes 'postgres://' (used by older providers/Supabase/Neon) to 'postgresql://' for SQLAlchemy.
    Falls back to SQLite for local development.
    """
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url
    
    # Check if running on Vercel or any serverless execution environment
    if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or os.environ.get('LAMBDA_TASK_ROOT') or not os.access(BASE_DIR, os.W_OK):
        # On Vercel serverless, /tmp is the only writable directory for ephemeral SQLite
        print("[INFO] Running on Vercel serverless using /tmp SQLite storage fallback.", file=sys.stderr)
        return "sqlite:////tmp/database.db"

    return f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-student-career-portal-secret-key-2026-cse')
    SQLALCHEMY_DATABASE_URI = get_normalized_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security & Cookie Parameters
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # Admin Bootstrap Parameters
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@portal.com')
    ADMIN_INITIAL_PASSWORD = os.environ.get('ADMIN_INITIAL_PASSWORD', 'Admin@123')
    ADMIN_BOOTSTRAP_SECRET = os.environ.get('ADMIN_BOOTSTRAP_SECRET', '')

    # Pagination
    ITEMS_PER_PAGE = 12


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
