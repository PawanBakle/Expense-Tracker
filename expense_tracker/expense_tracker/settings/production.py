from .base import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    print("WARNING: SECRET_KEY not set in environment, using fallback for testing")
    SECRET_KEY = 'django-insecure-test-key-do-not-use-in-production'

# Allowed hosts
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.railway.app', 
    '.up.railway.app',
    'expense-tracker-production-a52b.up.railway.app'
]

# Database - Optimized for Railway

# Database - Optimized for Railway
# Database - Optimized for Railway Internal Network
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"DEBUG: DATABASE_URL found: {'Yes' if DATABASE_URL else 'No'}")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=0,  # Turn off max age temporarily to prevent pooled connection freezes
            conn_health_checks=False,
        )
    }
    # For Railway's internal networks, disabling sslmode prevents the 15s handshake timeout
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'disable',
        'connect_timeout': 10,
    }
else:
    # Fallback to local PostgreSQL / SQLite
    print("WARNING: DATABASE_URL not found, using fallback local settings")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'expense_db'),
            'USER': os.environ.get('DB_USER', 'expense_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Security headers - disable for now
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 0

# CORS
CORS_ALLOW_ALL_ORIGINS = False
cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
cors_origins.extend(['https://*.railway.app', 'https://*.up.railway.app'])
CORS_ALLOWED_ORIGINS = cors_origins

# CSRF
csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
csrf_origins = [origin.strip() for origin in csrf_origins if origin.strip()]
csrf_origins.extend(['https://*.railway.app', 'https://*.up.railway.app'])
CSRF_TRUSTED_ORIGINS = csrf_origins

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
STATICFILES_DIRS = []
# Modern WhiteNoise configuration - avoids manifest generation freezes
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
# Logging - More verbose for debugging
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
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['console'],
            'level': 'DEBUG',
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
SPECTACULAR_SETTINGS = {
    'TITLE': 'Expense Tracker API',
    'DESCRIPTION': 'API documentation for Expense Tracker Backend',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    
    # This line completely removes Swagger's reliance on local Django static files:
    'SWAGGER_UI_DIST': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5',
}