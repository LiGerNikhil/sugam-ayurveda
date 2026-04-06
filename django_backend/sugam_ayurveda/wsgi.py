"""
WSGI config for sugam_ayurveda project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sugam_ayurveda.settings')

application = get_wsgi_application()
