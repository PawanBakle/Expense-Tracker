import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings.production')
django.setup()

from django.core.management import call_command

print("Running migrations...")
try:
    call_command('migrate', verbosity=3)
    print("✅ Migrations completed successfully!")
except Exception as e:
    print(f"❌ Migration failed: {e}")
    sys.exit(1)