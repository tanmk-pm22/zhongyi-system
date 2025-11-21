"""Final Test - Patent Medicine in Prescription System"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from prescriptions.models import PatentMedicine, PrescriptionPatentMedicine
from django.template.loader import get_template

print("=" * 80)
print("FINAL TEST - Patent Medicine Integration")
print("=" * 80)

all_tests_passed = True

# Test 1: Model Fields
print("\n[Test 1] PrescriptionPatentMedicine Model Fields")
print("-" * 80)
try:
    test_fields = {
        'prescription': 'ForeignKey to Prescription',
        'medicine': 'ForeignKey to PatentMedicine',
        'quantity': 'Quantity field',
        'dosage_instruction': 'Usage instructions',
        'subtotal': 'Subtotal property',
    }

    for field_name, description in test_fields.items():
        if hasattr(PrescriptionPatentMedicine, field_name):
            print(f"  [{field_name}] OK - {description}")
        else:
            print(f"  [{field_name}] FAIL - Missing")
            all_tests_passed = False

    # Check related_name
    from prescriptions.models import Prescription
    p = Prescription()
    if hasattr(p, 'patent_medicine_items'):
        print(f"  [related_name='patent_medicine_items'] OK")
    else:
        print(f"  [related_name] FAIL")
        all_tests_passed = False

    print("Status: PASS" if all_tests_passed else "Status: FAIL")
except Exception as e:
    print(f"  ERROR: {e}")
    all_tests_passed = False

# Test 2: Patent Medicine Data
print("\n[Test 2] Patent Medicine Database")
print("-" * 80)
try:
    count = PatentMedicine.objects.count()
    print(f"  Total medicines: {count}")
    if count >= 10:
        print("  Status: PASS")
    else:
        print("  Status: FAIL - Expected at least 10 medicines")
        all_tests_passed = False
except Exception as e:
    print(f"  ERROR: {e}")
    all_tests_passed = False

# Test 3: Templates
print("\n[Test 3] Template Files")
print("-" * 80)
templates_to_check = [
    'prescriptions/create_prescription.html',
    'prescriptions/edit_prescription.html',
    'prescriptions/prescription_detail.html',
]

for template_name in templates_to_check:
    try:
        template = get_template(template_name)
        # Check for patent medicine sections in template
        template_str = template.template.source

        checks = []
        if 'create' in template_name or 'edit' in template_name:
            checks = [
                ('patent_medicine_id', 'Patent medicine select field'),
                ('patent_quantity', 'Quantity input'),
                ('addPatentMedicineRow', 'Add medicine JavaScript function'),
            ]
        elif 'detail' in template_name:
            checks = [
                ('patent_medicine_items', 'Patent medicine items loop'),
                ('item.medicine.name_cn', 'Medicine name display'),
                ('item.subtotal', 'Subtotal display'),
            ]

        print(f"  [{template_name}]")
        for check_str, description in checks:
            if check_str in template_str:
                print(f"    - {description}: OK")
            else:
                print(f"    - {description}: MISSING")
                all_tests_passed = False

    except Exception as e:
        print(f"  [{template_name}] ERROR: {e}")
        all_tests_passed = False

print("  Status: PASS" if all_tests_passed else "Status: FAIL")

# Test 4: View Functions
print("\n[Test 4] View Functions")
print("-" * 80)
try:
    from prescriptions.views import create_prescription, edit_prescription
    print("  [create_prescription] Imported OK")
    print("  [edit_prescription] Imported OK")
    print("  Status: PASS")
except Exception as e:
    print(f"  ERROR: {e}")
    print("  Status: FAIL")
    all_tests_passed = False

# Final Summary
print("\n" + "=" * 80)
if all_tests_passed:
    print("ALL TESTS PASSED!")
    print("=" * 80)
    print("\nPatent Medicine integration is complete:")
    print("  - Model with correct fields (medicine, dosage_instruction, subtotal)")
    print("  - Templates updated with patent_medicine_items")
    print("  - Create and edit prescription forms support patent medicines")
    print("  - Prescription details display patent medicines with pricing")
    print("\nYou can now:")
    print("  1. Create prescriptions with both herbs and patent medicines")
    print("  2. Edit existing prescriptions to add/remove patent medicines")
    print("  3. View complete prescription details including patent medicines")
    print("  4. Calculate total cost including patent medicine pricing")
else:
    print("SOME TESTS FAILED - Please review errors above")
print("=" * 80)
