"""AI Analysis Engine for TCM Syndrome Differentiation."""
from typing import List, Dict, Tuple
from .models import Symptom, Syndrome, SyndromeSysmptomWeight


def analyze_symptoms(symptom_codes: List[str], tongue_data: Dict = None, pulse_data: Dict = None) -> List[Dict]:
    """
    Analyze symptoms and return suggested syndromes with confidence scores.

    Args:
        symptom_codes: List of symptom codes selected by practitioner
        tongue_data: Dict with tongue appearance data
        pulse_data: Dict with pulse quality data

    Returns:
        List of dicts with syndrome info and confidence scores
    """
    if not symptom_codes:
        return []

    # Get all active syndromes with their symptom weights
    syndromes = Syndrome.objects.filter(is_active=True).prefetch_related(
        'syndromesysmptomweight_set__symptom'
    )

    results = []

    for syndrome in syndromes:
        score = 0.0
        matched_symptoms = []
        total_possible = 0.0
        primary_matched = 0
        primary_total = 0

        # Calculate score based on symptom matches
        for sw in syndrome.syndromesysmptomweight_set.all():
            total_possible += sw.weight
            if sw.is_primary:
                primary_total += 1

            if sw.symptom.code in symptom_codes:
                score += sw.weight
                matched_symptoms.append({
                    'code': sw.symptom.code,
                    'name_en': sw.symptom.name_en,
                    'name_cn': sw.symptom.name_cn,
                    'is_primary': sw.is_primary,
                })
                if sw.is_primary:
                    primary_matched += 1

        # Skip if no matches
        if not matched_symptoms:
            continue

        # Calculate confidence
        if total_possible > 0:
            base_confidence = (score / total_possible) * 100
        else:
            base_confidence = 0

        # Boost confidence if primary symptoms are matched
        if primary_total > 0:
            primary_ratio = primary_matched / primary_total
            confidence = base_confidence * (0.7 + 0.3 * primary_ratio)
        else:
            confidence = base_confidence

        # Additional scoring based on tongue and pulse
        if tongue_data:
            tongue_match = check_tongue_match(syndrome, tongue_data)
            if tongue_match:
                confidence = min(100, confidence * 1.1)

        if pulse_data:
            pulse_match = check_pulse_match(syndrome, pulse_data)
            if pulse_match:
                confidence = min(100, confidence * 1.1)

        results.append({
            'syndrome_id': syndrome.id,
            'code': syndrome.code,
            'name_en': syndrome.name_en,
            'name_cn': syndrome.name_cn,
            'category': syndrome.get_category_display(),
            'confidence': round(confidence, 1),
            'matched_symptoms': matched_symptoms,
            'matched_count': len(matched_symptoms),
            'primary_matched': primary_matched,
            'primary_total': primary_total,
            'treatment_principle': syndrome.treatment_principle,
            'tongue_signs': syndrome.tongue_signs,
            'pulse_signs': syndrome.pulse_signs,
        })

    # Sort by confidence and return top results
    results.sort(key=lambda x: x['confidence'], reverse=True)
    return results[:5]


def check_tongue_match(syndrome: Syndrome, tongue_data: Dict) -> bool:
    """Check if tongue appearance matches syndrome."""
    if not syndrome.tongue_signs:
        return False

    tongue_signs_lower = syndrome.tongue_signs.lower()

    # Check body color
    body_color = tongue_data.get('body_color', '')
    if body_color:
        color_mappings = {
            'pale': ['pale', '淡白', '淡'],
            'light_red': ['light red', '淡红'],
            'red': ['red', '红'],
            'deep_red': ['deep red', '绛', '绛红'],
            'purple': ['purple', '紫'],
        }
        for key, values in color_mappings.items():
            if body_color == key:
                if any(v in tongue_signs_lower for v in values):
                    return True

    # Check coating
    coating_color = tongue_data.get('coating_color', '')
    if coating_color:
        coating_mappings = {
            'white': ['white', '白'],
            'yellow': ['yellow', '黄'],
            'gray': ['gray', '灰'],
            'black': ['black', '黑'],
        }
        for key, values in coating_mappings.items():
            if coating_color == key:
                if any(v in tongue_signs_lower for v in values):
                    return True

    return False


def check_pulse_match(syndrome: Syndrome, pulse_data: Dict) -> bool:
    """Check if pulse quality matches syndrome."""
    if not syndrome.pulse_signs:
        return False

    pulse_signs_lower = syndrome.pulse_signs.lower()
    overall_pulse = pulse_data.get('overall', '')

    if overall_pulse:
        pulse_mappings = {
            'floating': ['floating', '浮'],
            'deep': ['deep', '沉'],
            'slow': ['slow', '迟'],
            'rapid': ['rapid', '数'],
            'deficient': ['deficient', '虚'],
            'excess': ['excess', '实'],
            'slippery': ['slippery', '滑'],
            'wiry': ['wiry', '弦'],
            'thready': ['thready', '细'],
            'weak': ['weak', '弱'],
        }
        for key, values in pulse_mappings.items():
            if key in overall_pulse.lower():
                if any(v in pulse_signs_lower for v in values):
                    return True

    return False


def get_treatment_suggestions(syndrome_codes: List[str]) -> Dict:
    """
    Get treatment suggestions based on identified syndromes.

    Args:
        syndrome_codes: List of identified syndrome codes

    Returns:
        Dict with treatment principles and recommendations
    """
    syndromes = Syndrome.objects.filter(code__in=syndrome_codes, is_active=True)

    principles = []
    for syndrome in syndromes:
        if syndrome.treatment_principle:
            principles.append({
                'syndrome': f"{syndrome.name_en} ({syndrome.name_cn})",
                'principle': syndrome.treatment_principle,
            })

    return {
        'treatment_principles': principles,
        'note': 'These are AI-generated suggestions. Please verify and adjust based on clinical judgment.',
    }
