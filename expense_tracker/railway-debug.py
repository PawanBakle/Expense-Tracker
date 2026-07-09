import os
import sys

print("=" * 50)
print("RAILWAY ENVIRONMENT DEBUG")
print("=" * 50)

# Check critical environment variables
variables = [
    'DJANGO_ENV',
    'DATABASE_URL',
    'SECRET_KEY',
    'ALLOWED_HOSTS',
    'CORS_ALLOWED_ORIGINS',
    'CSRF_TRUSTED_ORIGINS',
    'DEBUG'
]

for var in variables:
    value = os.environ.get(var)
    if value:
        # Mask sensitive values
        if var in ['SECRET_KEY', 'DATABASE_URL']:
            print(f"✅ {var}: {value[:20]}... (set)")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: NOT SET")

print("=" * 50)
print("Testing PostgreSQL connection...")

# Try to connect to PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Successfully connected to PostgreSQL!")
        conn.close()
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
else:
    print("❌ DATABASE_URL not found!")