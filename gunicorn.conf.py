"""
Gunicorn Production Server Configuration
"""

import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
workers = min(4, multiprocessing.cpu_count() * 2 + 1)
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"

proc_name = "scholarship_portal"
