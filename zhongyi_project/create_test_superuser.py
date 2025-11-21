"""Create or reset test superuser account"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Reset admin password
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print("=" * 60)
    print("Admin password has been reset!")
    print("=" * 60)
    print("\nLogin credentials:")
    print("  URL: http://127.0.0.1:8000/admin/")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 60)
except User.DoesNotExist:
    print("Admin user not found. Creating new one...")
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    print("=" * 60)
    print("New admin user created!")
    print("=" * 60)
    print("\nLogin credentials:")
    print("  URL: http://127.0.0.1:8000/admin/")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 60)
