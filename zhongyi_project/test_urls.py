"""Test all URLs are working"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.urls import reverse, resolve
from django.test import Client

print("=" * 70)
print("URL CONFIGURATION TEST")
print("=" * 70)

# Test URLs
urls_to_test = [
    ('/', 'Root URL (no language prefix)'),
    ('/zh-hans/', 'Chinese homepage'),
    ('/en/', 'English homepage'),
    ('/admin/', 'Admin without language prefix'),
    ('/zh-hans/admin/', 'Admin with Chinese prefix'),
    ('/zh-hans/accounts/login/', 'Login page'),
    ('/zh-hans/patients/', 'Patients list'),
    ('/zh-hans/diagnosis/', 'Diagnosis list'),
    ('/zh-hans/prescriptions/', 'Prescriptions list'),
]

client = Client()

print("\nTesting URLs:")
print("-" * 70)

for url, description in urls_to_test:
    try:
        response = client.get(url, follow=True)
        status = "OK" if response.status_code == 200 else f"Status {response.status_code}"
        redirect = f" (redirected to {response.redirect_chain[0][0]})" if response.redirect_chain else ""
        print(f"[{status}] {url:30s} - {description}{redirect}")
    except Exception as e:
        print(f"[ERROR] {url:30s} - {description}: {str(e)}")

print("\n" + "=" * 70)
print("RECOMMENDED URLS FOR ACCESS")
print("=" * 70)
print("\nMain Application URLs:")
print("  Root (auto-redirect):    http://127.0.0.1:8000/")
print("  Chinese Homepage:        http://127.0.0.1:8000/zh-hans/")
print("  English Homepage:        http://127.0.0.1:8000/en/")
print("\nAdmin URLs:")
print("  Admin Panel:             http://127.0.0.1:8000/admin/")
print("                      OR:  http://127.0.0.1:8000/zh-hans/admin/")
print("\nUser Login:")
print("  Login Page:              http://127.0.0.1:8000/zh-hans/accounts/login/")
print("\nMain Features:")
print("  Patients:                http://127.0.0.1:8000/zh-hans/patients/")
print("  Diagnosis:               http://127.0.0.1:8000/zh-hans/diagnosis/")
print("  Prescriptions:           http://127.0.0.1:8000/zh-hans/prescriptions/")
print("=" * 70)

# Check language settings
from django.conf import settings
print("\nLanguage Configuration:")
print(f"  Default Language: {settings.LANGUAGE_CODE}")
print(f"  Available Languages: {[lang[0] for lang in settings.LANGUAGES]}")
print("=" * 70)
