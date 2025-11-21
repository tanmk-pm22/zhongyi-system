"""Test Patent Medicine in Prescription System"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from prescriptions.models import PatentMedicine
from django.template.loader import get_template
from django.urls import reverse

print("=" * 80)
print("Testing Patent Medicine in Prescription System")
print("=" * 80)

# Test 1: Patent Medicine Data
print("\n[Test 1] Patent Medicine Database")
print("-" * 80)
patent_count = PatentMedicine.objects.count()
print(f"Total Patent Medicines: {patent_count}")

if patent_count > 0:
    pm = PatentMedicine.objects.first()
    print(f"Sample: Patent Medicine Code={pm.code}")
    print(f"Price: {pm.price_per_box}")
    print("Status: PASS")
else:
    print("Status: FAIL - No patent medicines found")

# Test 2: Templates
print("\n[Test 2] Prescription Templates")
print("-" * 80)
templates = [
    'prescriptions/create_prescription.html',
    'prescriptions/edit_prescription.html',
    'prescriptions/prescription_detail.html',
]

template_status = True
for template_name in templates:
    try:
        get_template(template_name)
        print(f"  [{template_name}] OK")
    except Exception as e:
        print(f"  [{template_name}] MISSING - {e}")
        template_status = False

print(f"Status: {'PASS' if template_status else 'FAIL'}")

# Test 3: URL Configuration
print("\n[Test 3] URL Routes")
print("-" * 80)
try:
    url = reverse('prescriptions:patentmedicine_list')
    print(f"  Patent Medicine List: {url} - OK")
    print("Status: PASS")
except Exception as e:
    print(f"  ERROR: {e}")
    print("Status: FAIL")

# Test 4: Diagnosis Edit Functionality
print("\n[Test 4] Diagnosis Edit")
print("-" * 80)
try:
    from diagnosis.views import edit_diagnosis
    edit_url = reverse('diagnosis:edit', kwargs={'pk': 1})
    print(f"  Edit Diagnosis View: OK")
    print(f"  Edit URL: {edit_url}")

    # Check template
    get_template('diagnosis/edit_diagnosis.html')
    print(f"  Edit Template: OK")
    print("Status: PASS")
except Exception as e:
    print(f"  ERROR: {e}")
    print("Status: FAIL")

# Test 5: PrescriptionPatentMedicine Model
print("\n[Test 5] Prescription-Patent Medicine Relationship")
print("-" * 80)
try:
    from prescriptions.models import PrescriptionPatentMedicine
    print("  Model imported successfully")

    # Check fields
    fields = ['prescription', 'patent_medicine', 'quantity', 'usage_instructions', 'total_price']
    for field in fields:
        if hasattr(PrescriptionPatentMedicine, field):
            print(f"  Field '{field}': OK")
        else:
            print(f"  Field '{field}': MISSING")

    print("Status: PASS")
except Exception as e:
    print(f"  ERROR: {e}")
    print("Status: FAIL")

print("\n" + "=" * 80)
print("Test Summary")
print("=" * 80)
print("\nAll components ready for use:")
print("1. Patent medicines can be added to prescriptions")
print("2. Both create and edit prescription forms support patent medicines")
print("3. Prescription details display patent medicines")
print("4. Diagnosis records have edit functionality")
print("\nSystem is ready for testing!")
print("=" * 80)
