import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from django.db import connection

print(f"Connected to: {connection.vendor}")
print(f"Database name: {connection.settings_dict['NAME']}")
print(f"Database engine: {connection.settings_dict['ENGINE']}")