"""
Vercel Serverless Entrypoint
Student Career & Scholarship Portal
Exposes the WSGI Flask application object for Vercel's Python runtime.
"""

import sys
import os

# Add root project directory to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app

flask_app = create_app()

class StripVercelPrefixMiddleware:
    """
    WSGI Middleware to ensure PATH_INFO is cleanly normalized
    regardless of how Vercel routes incoming requests.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path in ('/api/index.py', '/api/index', '/api/index/'):
            environ['PATH_INFO'] = '/'
        elif path.startswith('/api/index.py/'):
            environ['PATH_INFO'] = path[len('/api/index.py'):]
        elif path.startswith('/api/index/'):
            environ['PATH_INFO'] = path[len('/api/index'):]
        return self.wsgi_app(environ, start_response)

# Expose WSGI application callable for Vercel
app = StripVercelPrefixMiddleware(flask_app.wsgi_app)

if __name__ == "__main__":
    flask_app.run()
