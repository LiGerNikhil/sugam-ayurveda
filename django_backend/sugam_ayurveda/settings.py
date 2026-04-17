"""
Django settings for sugam_ayurveda project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '187.127.147.152',
    'sugamayurvedaa.com',
    'www.sugamayurvedaa.com',
]

CSRF_TRUSTED_ORIGINS = [
    'http://187.127.147.152',
    'http://sugamayurvedaa.com',
    'http://www.sugamayurvedaa.com',
    'https://sugamayurvedaa.com',
    'https://www.sugamayurvedaa.com',
    'https://de32-103-12-133-93.ngrok-free.app',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
    'https://localhost',
    'https://127.0.0.1',
]

# Optional: Set custom site URL
SITE_URL = 'https://sugamayurvedaa.com'

# Optional: Force HTTPS (set to True after SSL is enabled on VPS)
USE_HTTPS = False

# If SSL is terminated at Nginx and proxied to Gunicorn over HTTP, enable this.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security defaults for VPS - SET TO FALSE UNTIL SSL IS CONFIGURED
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'sugam_ayurveda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'sugam_ayurveda.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'saakshinikhil@gmail.com'
EMAIL_HOST_PASSWORD = 'oqqq wqfu fncv jbgt'
DEFAULT_FROM_EMAIL = 'Sugam Ayurveda <saakshinikhil@gmail.com>'

# Cache settings for OTP
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Smart login system settings
LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL is handled by the smart login view based on user type
LOGOUT_REDIRECT_URL = '/login/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'admin_dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Razorpay Payment Gateway Settings
RAZORPAY_KEY_ID = 'rzp_test_SZ7O4UsIzQBDVI'
RAZORPAY_KEY_SECRET = 'sDXhikw5YhF5eRz5Lvc92PhZ'
