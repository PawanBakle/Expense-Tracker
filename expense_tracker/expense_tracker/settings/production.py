from .base import *
from decouple import config
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings
SECRET_KEY = config('SECRET_KEY')  # Must be set in environment

# Allowed hosts - comma separated in environment variable
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Add Railway's domain
ALLOWED_HOSTS.append('*.railway.app')
ALLOWED_HOSTS.append('*.up.railway.app')
# Database - PostgreSQL using DATABASE_URL
# DATABASE_URL = config('DATABASE_URL', default=None)
# if DATABASE_URL:
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=DATABASE_URL,
#             conn_max_age=600,
#             ssl_require=True  # Set to False for some hosting providers
#         )
#     }
# else:
    # Fallback to individual settings if DATABASE_URL is not provided
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': config('DB_NAME'),
    #         'USER': config('DB_USER'),
    #         'PASSWORD': config('DB_PASSWORD'),
    #         'HOST': config('DB_HOST'),
    #         'PORT': config('DB_PORT', default='5432'),
    #         'CONN_MAX_AGE': 600,
    #     }
    # }

DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
# Security headers
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS - Restricted

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in config('CORS_ALLOWED_ORIGINS', default='').split(',') if origin.strip()]
# Static files with Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

# Logging for production
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
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': '/var/log/django/expense_tracker.log',  
        #     'formatter': 'verbose',
        # },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'expense_tracker': { 
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourapp.com')

# Cache (Redis for production, optional)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
}

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# CSRF settings
# CSRF Trusted Origin, Filter out empty values
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if origin.strip()]
# Ensure all origins have a scheme
CSRF_TRUSTED_ORIGINS = [f'https://{origin}' if not origin.startswith(('http://', 'https://')) else origin for origin in CSRF_TRUSTED_ORIGINS]
# Security middleware
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')