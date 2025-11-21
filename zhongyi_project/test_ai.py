"""Test AI Assistant functionality"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from diagnosis.ai_assistant import TCMAIAssistant

# Test 1: Syndrome Analysis
print("=" * 50)
print("Test 1: AI Syndrome Differentiation")
print("=" * 50)

ai = TCMAIAssistant()

# Test case: Qi Deficiency patient
result = ai.analyze_diagnosis(
    chief_complaint="Fatigue and shortness of breath",
    tongue_body_color="pale",
    tongue_coating_color="white",
    pulse_overall="weak",
    symptoms=["tired", "fatigue"],
    additional_notes="Patient reports feeling weak all day"
)

print("\nInput:")
print(f"  Chief Complaint: Fatigue and shortness of breath")
print(f"  Tongue: pale body, white coating")
print(f"  Pulse: weak")
print(f"  Symptoms: tired, fatigue")

print("\nAI Analysis:")
if result['syndromes']:
    print(f"  Top Syndrome: {result['syndromes'][0]['syndrome_code']}")
    print(f"  Confidence: {result['syndromes'][0]['confidence']}")
    print(f"  Number of Matches: {len(result['syndromes'][0]['matches'])}")
else:
    print("  No syndrome patterns matched")
print(f"  Has Explanation: {len(result['explanation']) > 0}")
print(f"  Has Treatment Principle: {len(result['treatment_principle']) > 0}")

# Test 2: Prescription Recommendation
print("\n" + "=" * 50)
print("Test 2: AI Prescription Recommendation")
print("=" * 50)

recommendation = ai.recommend_prescription(
    syndrome_code='SYN001',  # Qi Deficiency
    patient_age=45,
    patient_gender='M'
)

print("\nInput:")
print(f"  Syndrome Code: SYN001 (Qi Deficiency)")
print(f"  Patient Age: 45")
print(f"  Patient Gender: Male")

print("\nRecommendation:")
print(f"  Formula Code: {recommendation.get('formula_code', 'N/A')}")
print(f"  Herb Count: {len(recommendation['herbs'])}")
print(f"  First Herb Dosage: {recommendation['herbs'][0]['dosage']}g")
print(f"  Modifications Count: {len(recommendation['modifications'])}")
print(f"  Has Decoction Method: {len(recommendation['decoction_method']) > 0}")

# Test 3: Different age groups
print("\n" + "=" * 50)
print("Test 3: Age-based Dosage Adjustment")
print("=" * 50)

for age, label in [(5, "Child"), (45, "Adult"), (75, "Elderly")]:
    rec = ai.recommend_prescription('SYN001', patient_age=age)
    first_herb = rec['herbs'][0]
    print(f"\n{label} (age {age}): First herb dosage = {first_herb['dosage']}g")

print("\n" + "=" * 50)
print("All tests completed successfully!")
print("=" * 50)
