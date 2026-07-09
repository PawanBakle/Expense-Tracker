from .base import *
from decouple import config
import dj_database_url
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings
SECRET_KEY = config('SECRET_KEY')  # Must be set in environment

# Allowed hosts - comma separated in environment variable
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
# Remove empty strings
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]
# Add Railway's domain
ALLOWED_HOSTS.extend(['*.railway.app', '*.up.railway.app', 'localhost', '127.0.0.1'])

# Database - Use environment variable directly
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=False  # Set to False initially, Railway handles SSL differently
        )
    }
else:
    # Fallback if DATABASE_URL is not set
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='railway'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default=''),
            'PORT': config('DB_PORT', default='5432'),
            'CONN_MAX_AGE': 600,
        }
    }

# Security headers - disable for now to test
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False  # Set to True after SSL is working
CSRF_COOKIE_SECURE = False  # Set to True after SSL is working
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 0  # Disable HSTS for now

# CORS - Restricted
CORS_ALLOW_ALL_ORIGINS = False

# Get CORS origins from environment or use defaults
cors_origins = config('CORS_ALLOWED_ORIGINS', default='').split(',')
cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
# Add Railway domains
cors_origins.extend(['https://*.railway.app', 'https://*.up.railway.app'])
CORS_ALLOWED_ORIGINS = cors_origins

# CSRF Trusted Origins
csrf_origins = config('CSRF_TRUSTED_ORIGINS', default='').split(',')
csrf_origins = [origin.strip() for origin in csrf_origins if origin.strip()]
# Add Railway domains
csrf_origins.extend(['https://*.railway.app', 'https://*.up.railway.app'])
CSRF_TRUSTED_ORIGINS = csrf_origins

# Static files with Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
STATICFILES_DIRS = []  # Override for production

# Logging - Set to DEBUG to see what's happening
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Set to DEBUG to see what's happening
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',  # To see SQL queries
            'propagate': False,
        },
    },
}

# Email backend - disable for now
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache - disable Redis for now
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# Security middleware
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')