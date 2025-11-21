"""Final System Verification - All Features"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from prescriptions.models import PatentMedicine, Herb, ClassicFormula
from django.template.loader import get_template
from django.urls import reverse

print("=" * 80)
print("FINAL SYSTEM VERIFICATION")
print("=" * 80)

# Test 1: Database Content
print("\n[Test 1] Database Content")
print("-" * 80)
patent_count = PatentMedicine.objects.count()
herb_count = Herb.objects.count()
formula_count = ClassicFormula.objects.count()

print(f"Patent Medicines: {patent_count} (Expected: 10)")
print(f"Herbs: {herb_count} (Expected: 40)")
print(f"Classic Formulas: {formula_count} (Expected: 15)")

status_1 = "PASS" if patent_count == 10 and herb_count == 40 and formula_count == 15 else "FAIL"
print(f"Status: {status_1}")

# Test 2: Template Files
print("\n[Test 2] Template Files")
print("-" * 80)
templates_to_check = [
    'prescriptions/herb_list.html',
    'prescriptions/formula_list.html',
    'prescriptions/patentmedicine_list.html',
    'prescriptions/prescription_list.html',
    'prescriptions/create_prescription.html',
]

template_status = True
for template_name in templates_to_check:
    try:
        get_template(template_name)
        print(f"  [{template_name}] OK")
    except Exception as e:
        print(f"  [{template_name}] MISSING")
        template_status = False

status_2 = "PASS" if template_status else "FAIL"
print(f"Status: {status_2}")

# Test 3: URL Configuration
print("\n[Test 3] URL Configuration")
print("-" * 80)
urls_to_check = [
    ('prescriptions:herb_list', 'Herb List'),
    ('prescriptions:formula_list', 'Formula List'),
    ('prescriptions:patentmedicine_list', 'Patent Medicine List'),
    ('prescriptions:list', 'Prescription List'),
]

url_status = True
for url_name, description in urls_to_check:
    try:
        url = reverse(url_name)
        print(f"  [{description}] {url} - OK")
    except Exception as e:
        print(f"  [{description}] ERROR: {e}")
        url_status = False

status_3 = "PASS" if url_status else "FAIL"
print(f"Status: {status_3}")

# Test 4: Model Imports
print("\n[Test 4] Model Imports")
print("-" * 80)
try:
    from prescriptions.models import (
        Herb, HerbCategory, ClassicFormula, FormulaHerb,
        Prescription, PrescriptionItem,
        PatentMedicine, PrescriptionPatentMedicine
    )
    print("  All models imported successfully")
    status_4 = "PASS"
except Exception as e:
    print(f"  Import error: {e}")
    status_4 = "FAIL"

print(f"Status: {status_4}")

# Test 5: Views
print("\n[Test 5] Views Configuration")
print("-" * 80)
try:
    from prescriptions.views import (
        HerbListView, FormulaListView, PatentMedicineListView,
        PrescriptionListView
    )
    print("  HerbListView - OK")
    print("  FormulaListView - OK")
    print("  PatentMedicineListView - OK")
    print("  PrescriptionListView - OK")
    status_5 = "PASS"
except Exception as e:
    print(f"  View import error: {e}")
    status_5 = "FAIL"

print(f"Status: {status_5}")

# Test 6: AI Integration
print("\n[Test 6] AI Integration")
print("-" * 80)
try:
    from diagnosis.ai_assistant import TCMAIAssistant
    ai = TCMAIAssistant()

    # Test patent medicine recommendations
    recommendations = ai.recommend_patent_medicines('SYN001', patient_age=45)
    print(f"  AI Patent Medicine Recommendations: {len(recommendations)} medicines")

    # Test full AI suggestions
    diagnosis_data = {
        'chief_complaint': 'Test',
        'tongue_body_color': 'pale',
        'tongue_coating_color': 'white',
        'pulse_overall': 'weak',
    }
    patient_data = {'age': 45, 'gender': 'M'}

    result = ai.get_ai_suggestions(diagnosis_data, patient_data)
    has_patent_meds = 'patent_medicines' in result and result['patent_medicines'] is not None

    print(f"  AI returns patent medicine recommendations: {has_patent_meds}")
    status_6 = "PASS" if has_patent_meds else "FAIL"
except Exception as e:
    print(f"  AI error: {e}")
    status_6 = "FAIL"

print(f"Status: {status_6}")

# Test 7: Sample Data Check
print("\n[Test 7] Sample Data Check")
print("-" * 80)
try:
    # Check patent medicine details
    pm = PatentMedicine.objects.first()
    print(f"  Sample Patent Medicine: {pm.code}")
    print(f"  Has name: {bool(pm.name_cn)}")
    print(f"  Has dosage form: {bool(pm.dosage_form)}")
    print(f"  Has price: {pm.price_per_box is not None}")

    # Check herb details
    herb = Herb.objects.first()
    print(f"  Sample Herb: {herb.code}")
    print(f"  Has name: {bool(herb.name_cn)}")
    print(f"  Has nature: {bool(herb.nature)}")

    status_7 = "PASS"
except Exception as e:
    print(f"  Data check error: {e}")
    status_7 = "FAIL"

print(f"Status: {status_7}")

# Final Summary
print("\n" + "=" * 80)
print("FINAL RESULTS")
print("=" * 80)

all_tests = [status_1, status_2, status_3, status_4, status_5, status_6, status_7]
passed = all_tests.count("PASS")
total = len(all_tests)

print(f"\nTests Passed: {passed}/{total}")
print("\nTest Results:")
print(f"  [1] Database Content: {status_1}")
print(f"  [2] Template Files: {status_2}")
print(f"  [3] URL Configuration: {status_3}")
print(f"  [4] Model Imports: {status_4}")
print(f"  [5] Views Configuration: {status_5}")
print(f"  [6] AI Integration: {status_6}")
print(f"  [7] Sample Data: {status_7}")

if passed == total:
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED - SYSTEM READY FOR USE!")
    print("=" * 80)
    print("\nYou can now access:")
    print("  - Herb Library: http://127.0.0.1:8000/zh-hans/prescriptions/herbs/")
    print("  - Patent Medicines: http://127.0.0.1:8000/zh-hans/prescriptions/patent-medicines/")
    print("  - Classic Formulas: http://127.0.0.1:8000/zh-hans/prescriptions/formulas/")
    print("  - Admin Panel: http://127.0.0.1:8000/admin/")
    print("=" * 80)
else:
    print("\n" + "=" * 80)
    print(f"WARNING: {total - passed} test(s) failed")
    print("=" * 80)
