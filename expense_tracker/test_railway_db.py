import os
import sys
import psycopg2
import urllib.parse

print("=" * 50)
print("TESTING RAILWAY DATABASE CONNECTION")
print("=" * 50)

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL: {'Found' if DATABASE_URL else 'Not Found'}")

if not DATABASE_URL:
    print("❌ DATABASE_URL is not set!")
    sys.exit(1)

print(f"URL: {DATABASE_URL[:30]}...")

try:
    # Parse the URL
    parsed = urllib.parse.urlparse(DATABASE_URL)
    
    print(f"Host: {parsed.hostname}")
    print(f"Port: {parsed.port}")
    print(f"Database: {parsed.path.lstrip('/')}")
    print(f"User: {parsed.username}")
    
    # Try to connect with different SSL options
    ssl_options = ['require', 'prefer', 'allow', 'disable']
    
    for sslmode in ssl_options:
        try:
            print(f"\nTrying sslmode={sslmode}...")
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                database=parsed.path.lstrip('/'),
                user=parsed.username,
                password=parsed.password,
                sslmode=sslmode,
                connect_timeout=10
            )
            print(f"✅ SUCCESS with sslmode={sslmode}!")
            conn.close()
            break
        except Exception as e:
            print(f"❌ Failed with sslmode={sslmode}: {str(e)[:100]}...")
    else:
        print("\n❌ All SSL modes failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    
print("=" * 50)