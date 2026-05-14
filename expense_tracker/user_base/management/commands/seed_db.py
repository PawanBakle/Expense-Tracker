from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from user_base.models import Group, GroupMember

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with test users and a group"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        
        # 1. Clear existing data to avoid unique crashes
        User.objects.all().delete()
        Group.objects.all().delete()

        # 2. Create users
        alice = User.objects.create_user(email="alice@example.com", password="Password123!", mobile_number="123")
        bob = User.objects.create_user(email="bob@example.com", password="Password123!", mobile_number="456")
        charlie = User.objects.create_user(email="charlie@example.com", password="Password123!", mobile_number="789")

        # 3. Create group
        group = Group.objects.create(name="Ski Trip 2026", created_by=alice)
        
        # 4. Add memberships
        GroupMember.objects.create(_group=group, name=alice, is_admin=True)
        GroupMember.objects.create(_group=group, name=bob, is_admin=False)
        GroupMember.objects.create(_group=group, name=charlie, is_admin=False)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with Alice, Bob, and Charlie!"))