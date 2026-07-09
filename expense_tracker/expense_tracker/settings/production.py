from .base import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings - Use os.environ.get() for ALL variables
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment")

# Allowed hosts - get from environment
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# Remove empty strings
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]
# Add Railway's domain
ALLOWED_HOSTS.extend(['*.railway.app', '*.up.railway.app', 'localhost', '127.0.0.1'])

# Database - Use DATABASE_URL from Railway
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"DEBUG: DATABASE_URL found: {'Yes' if DATABASE_URL else 'No'}")  # Debug line

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=False  # Disable SSL for now to test
        )
    }
else:
    # This should NOT happen on Railway
    print("ERROR: DATABASE_URL not found in environment!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Security headers - disable for now
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 0

# CORS - get from environment
CORS_ALLOW_ALL_ORIGINS = False
cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
# Add Railway domains
cors_origins.extend(['https://*.railway.app', 'https://*.up.railway.app'])
CORS_ALLOWED_ORIGINS = cors_origins

# CSRF - get from environment
csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
csrf_origins = [origin.strip() for origin in csrf_origins if origin.strip()]
# Add Railway domains
csrf_origins.extend(['https://*.railway.app', 'https://*.up.railway.app'])
CSRF_TRUSTED_ORIGINS = csrf_origins

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
STATICFILES_DIRS = []

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600

# Security middleware
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')