"""
WSGI config for sugam_ayurveda project.

This module contains the WSGI application used by Django to serve
HTTP requests. It's used by Gunicorn to run the application in production.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

# Set Django settings module
# Use production settings if available, otherwise default to development
if os.environ.get('DJANGO_SETTINGS_MODULE'):
    # Use settings from environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ['DJANGO_SETTINGS_MODULE'])
else:
    # Default to production settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sugam_ayurveda.settings')

# Get the Django WSGI application
application = get_wsgi_application()

# Optional: Enable Django debug mode for development (comment out in production)
# os.environ.setdefault('DJANGO_DEBUG', 'True')

# Optional: Set up logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

# Log application startup
logger = logging.getLogger(__name__)
logger.info("Django WSGI application loaded successfully")
