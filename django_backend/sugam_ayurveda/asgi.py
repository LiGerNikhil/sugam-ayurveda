"""
ASGI config for sugam_ayurveda project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sugam_ayurveda.settings')

application = get_asgi_application()
