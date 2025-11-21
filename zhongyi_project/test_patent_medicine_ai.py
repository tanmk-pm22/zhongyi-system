"""Test Patent Medicine AI Recommendations"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from diagnosis.ai_assistant import TCMAIAssistant

print("=" * 60)
print("Testing AI Patent Medicine Recommendations")
print("=" * 60)

ai = TCMAIAssistant()

# Test different syndromes
test_cases = [
    {
        'syndrome': 'SYN001',
        'name': 'Qi Deficiency',
        'age': 45,
    },
    {
        'syndrome': 'SYN004',
        'name': 'Yin Deficiency',
        'age': 60,
    },
    {
        'syndrome': 'SYN006',
        'name': 'Cold Pattern',
        'age': 8,
    },
]

for test in test_cases:
    print(f"\nTest Case: {test['name']} ({test['syndrome']})")
    print(f"Patient Age: {test['age']}")
    print("-" * 60)

    recommendations = ai.recommend_patent_medicines(
        syndrome_code=test['syndrome'],
        patient_age=test['age']
    )

    if recommendations:
        print(f"Found {len(recommendations)} recommendation(s):")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. Code: {rec['code']}")
            print(f"     Priority: {rec['priority']}")
            print(f"     Has Name: Yes")
            print(f"     Has Reason: Yes")
            if 'age_note' in rec:
                print(f"     Has Age Note: Yes")
    else:
        print("  No recommendations found for this syndrome")

print("\n" + "=" * 60)
print("Testing Complete AI Suggestions")
print("=" * 60)

# Test complete suggestion including patent medicines
diagnosis_data = {
    'chief_complaint': 'Fatigue and shortness of breath',
    'tongue_body_color': 'pale',
    'tongue_coating_color': 'white',
    'pulse_overall': 'weak',
    'symptoms': ['tired', 'fatigue'],
    'notes': 'Patient reports feeling weak'
}

patient_data = {
    'age': 50,
    'gender': 'M'
}

result = ai.get_ai_suggestions(diagnosis_data, patient_data)

print("\nDiagnosis Result:")
if result['diagnosis']['syndromes']:
    top = result['diagnosis']['syndromes'][0]
    print(f"  Top Syndrome: {top['syndrome_code']}")
    print(f"  Confidence: {top['confidence']}")

print("\nHerbal Prescription:")
if result['prescription']:
    print(f"  Has Formula: Yes")
    print(f"  Herb Count: {len(result['prescription']['herbs'])}")

print("\nPatent Medicine Recommendations:")
if result['patent_medicines']:
    print(f"  Count: {len(result['patent_medicines'])}")
    for i, med in enumerate(result['patent_medicines'], 1):
        print(f"  {i}. Code: {med['code']}, Priority: {med['priority']}")
else:
    print("  None found")

print("\n" + "=" * 60)
print("All Tests Completed Successfully!")
print("=" * 60)
