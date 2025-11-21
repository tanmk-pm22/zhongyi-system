"""
AI Assistant for TCM Diagnosis and Prescription
AI辅助中医诊断和处方系统

This module provides AI-powered assistance for:
1. Syndrome differentiation based on Four Examinations
2. Herbal prescription recommendations
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
import json


class TCMAIAssistant:
    """
    Traditional Chinese Medicine AI Assistant
    中医智能辅助系统
    """

    # Syndrome patterns based on tongue and pulse (simplified rule-based system)
    SYNDROME_RULES = {
        # Qi Deficiency patterns
        'qi_deficiency': {
            'keywords': ['fatigue', 'tired', '乏力', '气短', '懒言'],
            'tongue': ['pale', '淡', '胖大'],
            'pulse': ['weak', 'deficient', '虚', '弱'],
            'syndrome_code': 'SYN001',  # Qi Deficiency
            'confidence': 0.8,
        },
        # Blood Deficiency
        'blood_deficiency': {
            'keywords': ['dizziness', 'pale', '头晕', '面色苍白', '心悸'],
            'tongue': ['pale', 'thin', '淡', '薄'],
            'pulse': ['thready', 'weak', '细', '弱'],
            'syndrome_code': 'SYN002',  # Blood Deficiency
            'confidence': 0.75,
        },
        # Yang Deficiency
        'yang_deficiency': {
            'keywords': ['cold', 'chills', '畏寒', '肢冷', '腰膝酸软'],
            'tongue': ['pale', 'wet', '淡', '湿润'],
            'pulse': ['deep', 'slow', '沉', '迟'],
            'syndrome_code': 'SYN003',  # Yang Deficiency
            'confidence': 0.8,
        },
        # Yin Deficiency
        'yin_deficiency': {
            'keywords': ['night sweat', 'heat', '盗汗', '五心烦热', '口干'],
            'tongue': ['red', 'little coating', '红', '少苔'],
            'pulse': ['thready', 'rapid', '细', '数'],
            'syndrome_code': 'SYN004',  # Yin Deficiency
            'confidence': 0.8,
        },
        # Heat patterns
        'heat_pattern': {
            'keywords': ['fever', 'thirst', '发热', '口渴', '烦躁'],
            'tongue': ['red', 'yellow coating', '红', '黄苔'],
            'pulse': ['rapid', 'full', '数', '洪'],
            'syndrome_code': 'SYN005',  # Heat Pattern
            'confidence': 0.85,
        },
        # Cold patterns
        'cold_pattern': {
            'keywords': ['cold', 'aversion to cold', '恶寒', '喜温', '腹痛'],
            'tongue': ['pale', 'white coating', '淡', '白苔'],
            'pulse': ['tight', 'slow', '紧', '迟'],
            'syndrome_code': 'SYN006',  # Cold Pattern
            'confidence': 0.8,
        },
        # Dampness
        'dampness': {
            'keywords': ['heavy', 'bloating', '身重', '胸闷', '纳呆'],
            'tongue': ['thick coating', 'greasy', '厚苔', '腻'],
            'pulse': ['slippery', 'soft', '滑', '濡'],
            'syndrome_code': 'SYN007',  # Dampness
            'confidence': 0.75,
        },
        # Blood Stasis
        'blood_stasis': {
            'keywords': ['pain', 'fixed', '刺痛', '痛处固定', '瘀斑'],
            'tongue': ['purple', 'dark spots', '紫', '瘀点'],
            'pulse': ['choppy', 'wiry', '涩', '弦'],
            'syndrome_code': 'SYN008',  # Blood Stasis
            'confidence': 0.8,
        },
    }

    # Classic formulas for common syndromes
    FORMULA_RECOMMENDATIONS = {
        'SYN001': {  # Qi Deficiency
            'formula_code': 'F001',
            'formula_name': '四君子汤 | Si Jun Zi Tang',
            'herbs': [
                {'code': 'H007', 'name': '人参', 'dosage': 9.0},
                {'code': 'H008', 'name': '白术', 'dosage': 9.0},
                {'code': 'H009', 'name': '茯苓', 'dosage': 9.0},
                {'code': 'H010', 'name': '炙甘草', 'dosage': 6.0},
            ],
            'functions': '益气健脾 | Tonify Qi and Strengthen Spleen',
        },
        'SYN002': {  # Blood Deficiency
            'formula_code': 'F002',
            'formula_name': '四物汤 | Si Wu Tang',
            'herbs': [
                {'code': 'H011', 'name': '当归', 'dosage': 9.0},
                {'code': 'H012', 'name': '川芎', 'dosage': 6.0},
                {'code': 'H013', 'name': '白芍', 'dosage': 9.0},
                {'code': 'H014', 'name': '熟地黄', 'dosage': 12.0},
            ],
            'functions': '补血调经 | Nourish Blood and Regulate Menstruation',
        },
        'SYN003': {  # Yang Deficiency
            'formula_code': 'F003',
            'formula_name': '金匮肾气丸加减 | Modified Jin Gui Shen Qi Wan',
            'herbs': [
                {'code': 'H014', 'name': '熟地黄', 'dosage': 15.0},
                {'code': 'H015', 'name': '山药', 'dosage': 12.0},
                {'code': 'H016', 'name': '山茱萸', 'dosage': 9.0},
                {'code': 'H017', 'name': '附子', 'dosage': 6.0, 'preparation': '先煎'},
                {'code': 'H018', 'name': '肉桂', 'dosage': 3.0, 'preparation': '后下'},
            ],
            'functions': '温补肾阳 | Warm and Tonify Kidney Yang',
        },
        'SYN004': {  # Yin Deficiency
            'formula_code': 'F004',
            'formula_name': '六味地黄丸加减 | Modified Liu Wei Di Huang Wan',
            'herbs': [
                {'code': 'H014', 'name': '熟地黄', 'dosage': 15.0},
                {'code': 'H015', 'name': '山药', 'dosage': 12.0},
                {'code': 'H016', 'name': '山茱萸', 'dosage': 9.0},
                {'code': 'H019', 'name': '泽泻', 'dosage': 9.0},
                {'code': 'H020', 'name': '牡丹皮', 'dosage': 9.0},
                {'code': 'H009', 'name': '茯苓', 'dosage': 9.0},
            ],
            'functions': '滋阴补肾 | Nourish Yin and Tonify Kidney',
        },
        'SYN005': {  # Heat Pattern
            'formula_code': 'F005',
            'formula_name': '白虎汤加减 | Modified Bai Hu Tang',
            'herbs': [
                {'code': 'H021', 'name': '石膏', 'dosage': 30.0, 'preparation': '先煎'},
                {'code': 'H022', 'name': '知母', 'dosage': 9.0},
                {'code': 'H023', 'name': '粳米', 'dosage': 15.0},
                {'code': 'H010', 'name': '甘草', 'dosage': 6.0},
            ],
            'functions': '清热生津 | Clear Heat and Generate Fluids',
        },
        'SYN006': {  # Cold Pattern
            'formula_code': 'F006',
            'formula_name': '理中汤 | Li Zhong Tang',
            'herbs': [
                {'code': 'H007', 'name': '人参', 'dosage': 9.0},
                {'code': 'H008', 'name': '白术', 'dosage': 9.0},
                {'code': 'H024', 'name': '干姜', 'dosage': 6.0},
                {'code': 'H010', 'name': '炙甘草', 'dosage': 6.0},
            ],
            'functions': '温中祛寒 | Warm the Middle and Dispel Cold',
        },
        'SYN007': {  # Dampness
            'formula_code': 'F007',
            'formula_name': '平胃散加减 | Modified Ping Wei San',
            'herbs': [
                {'code': 'H025', 'name': '苍术', 'dosage': 9.0},
                {'code': 'H026', 'name': '厚朴', 'dosage': 9.0},
                {'code': 'H027', 'name': '陈皮', 'dosage': 6.0},
                {'code': 'H010', 'name': '甘草', 'dosage': 3.0},
            ],
            'functions': '燥湿运脾 | Dry Dampness and Strengthen Spleen',
        },
        'SYN008': {  # Blood Stasis
            'formula_code': 'F008',
            'formula_name': '血府逐瘀汤加减 | Modified Xue Fu Zhu Yu Tang',
            'herbs': [
                {'code': 'H028', 'name': '桃仁', 'dosage': 9.0},
                {'code': 'H029', 'name': '红花', 'dosage': 6.0},
                {'code': 'H011', 'name': '当归', 'dosage': 9.0},
                {'code': 'H012', 'name': '川芎', 'dosage': 6.0},
                {'code': 'H013', 'name': '赤芍', 'dosage': 9.0},
            ],
            'functions': '活血化瘀 | Invigorate Blood and Resolve Stasis',
        },
    }

    def analyze_diagnosis(
        self,
        chief_complaint: str,
        tongue_body_color: str,
        tongue_coating_color: str,
        pulse_overall: str,
        symptoms: List[str] = None,
        additional_notes: str = ""
    ) -> Dict:
        """
        Analyze patient data and suggest syndrome differentiation
        分析患者数据并提供辨证建议

        Args:
            chief_complaint: Main complaint
            tongue_body_color: Tongue body color
            tongue_coating_color: Tongue coating color
            pulse_overall: Overall pulse quality
            symptoms: List of symptom descriptions
            additional_notes: Additional clinical notes

        Returns:
            Dictionary with syndrome suggestions and confidence scores
        """
        results = {
            'syndromes': [],
            'confidence': 0.0,
            'explanation': '',
            'treatment_principle': '',
        }

        # Combine all text for analysis
        all_text = f"{chief_complaint} {additional_notes}"
        if symptoms:
            all_text += " " + " ".join(symptoms)

        all_text_lower = all_text.lower()

        # Tongue and pulse analysis
        tongue_text = f"{tongue_body_color} {tongue_coating_color}".lower()
        pulse_text = pulse_overall.lower()

        # Score each syndrome pattern
        pattern_scores = []

        for pattern_name, pattern_rules in self.SYNDROME_RULES.items():
            score = 0.0
            matches = []

            # Check keywords in complaints and symptoms
            for keyword in pattern_rules['keywords']:
                if keyword.lower() in all_text_lower:
                    score += 0.2
                    matches.append(f"症状匹配: {keyword}")

            # Check tongue characteristics
            for tongue_char in pattern_rules['tongue']:
                if tongue_char.lower() in tongue_text:
                    score += 0.3
                    matches.append(f"舌象匹配: {tongue_char}")

            # Check pulse characteristics
            for pulse_char in pattern_rules['pulse']:
                if pulse_char.lower() in pulse_text:
                    score += 0.3
                    matches.append(f"脉象匹配: {pulse_char}")

            # Normalize score
            if score > 0:
                confidence = min(score * pattern_rules['confidence'], 1.0)
                pattern_scores.append({
                    'pattern': pattern_name,
                    'syndrome_code': pattern_rules['syndrome_code'],
                    'confidence': round(confidence, 2),
                    'matches': matches,
                })

        # Sort by confidence
        pattern_scores.sort(key=lambda x: x['confidence'], reverse=True)

        # Take top 3 patterns
        results['syndromes'] = pattern_scores[:3]

        if results['syndromes']:
            top_syndrome = results['syndromes'][0]
            results['confidence'] = top_syndrome['confidence']
            results['explanation'] = f"基于四诊资料分析，患者可能存在{top_syndrome['pattern']}证型。" + \
                                   f"匹配特征：{', '.join(top_syndrome['matches'][:3])}"

            # Generate treatment principle
            if 'deficiency' in top_syndrome['pattern']:
                results['treatment_principle'] = '扶正补虚 | Support Normal Qi and Tonify Deficiency'
            elif 'heat' in top_syndrome['pattern']:
                results['treatment_principle'] = '清热泻火 | Clear Heat and Drain Fire'
            elif 'cold' in top_syndrome['pattern']:
                results['treatment_principle'] = '温阳散寒 | Warm Yang and Dispel Cold'
            elif 'dampness' in top_syndrome['pattern']:
                results['treatment_principle'] = '健脾化湿 | Strengthen Spleen and Resolve Dampness'
            elif 'stasis' in top_syndrome['pattern']:
                results['treatment_principle'] = '活血化瘀 | Invigorate Blood and Resolve Stasis'
            else:
                results['treatment_principle'] = '辨证施治 | Treat According to Pattern Differentiation'

        return results

    def recommend_prescription(
        self,
        syndrome_code: str,
        patient_age: int = None,
        patient_gender: str = None,
        modifications: Dict = None
    ) -> Dict:
        """
        Recommend herbal prescription based on syndrome
        根据证型推荐中药处方

        Args:
            syndrome_code: Syndrome code (e.g., 'SYN001')
            patient_age: Patient age for dosage adjustment
            patient_gender: Patient gender for formula selection
            modifications: Additional modifications

        Returns:
            Dictionary with formula and herb recommendations
        """
        recommendation = {
            'formula': None,
            'herbs': [],
            'modifications': [],
            'dosage_notes': '',
            'decoction_method': '水煎服，每日一剂，分两次温服。\nDecoct with water, one dose per day, take warm twice daily.',
        }

        # Get base formula
        if syndrome_code in self.FORMULA_RECOMMENDATIONS:
            formula_data = self.FORMULA_RECOMMENDATIONS[syndrome_code]
            recommendation['formula'] = formula_data['formula_name']
            recommendation['herbs'] = formula_data['herbs'].copy()
            recommendation['functions'] = formula_data['functions']

            # Age-based dosage adjustment
            if patient_age:
                if patient_age < 12:
                    # Reduce dosage for children
                    dosage_factor = 0.5
                    recommendation['dosage_notes'] = '儿童剂量减半 | Children: half dosage'
                elif patient_age > 65:
                    # Slightly reduce for elderly
                    dosage_factor = 0.8
                    recommendation['dosage_notes'] = '老年患者酌减 | Elderly: slightly reduced dosage'
                else:
                    dosage_factor = 1.0

                # Adjust herb dosages
                for herb in recommendation['herbs']:
                    herb['dosage'] = round(herb['dosage'] * dosage_factor, 1)

            # Add modification suggestions
            if syndrome_code == 'SYN001':  # Qi Deficiency
                recommendation['modifications'] = [
                    '若气虚明显，可加黄芪15克 | If severe Qi deficiency, add Huang Qi 15g',
                    '若兼有食欲不振，可加神曲9克 | If poor appetite, add Shen Qu 9g',
                ]
            elif syndrome_code == 'SYN004':  # Yin Deficiency
                recommendation['modifications'] = [
                    '若口干明显，可加麦冬9克 | If severe dry mouth, add Mai Dong 9g',
                    '若失眠多梦，可加酸枣仁12克 | If insomnia, add Suan Zao Ren 12g',
                ]

        return recommendation

    def get_ai_suggestions(
        self,
        diagnosis_data: Dict,
        patient_data: Dict = None
    ) -> Dict:
        """
        Get comprehensive AI suggestions for diagnosis and prescription
        获取完整的AI诊断和处方建议

        Args:
            diagnosis_data: Diagnosis session data
            patient_data: Patient information

        Returns:
            Complete AI suggestion with diagnosis and prescription
        """
        # Analyze diagnosis
        diagnosis_result = self.analyze_diagnosis(
            chief_complaint=diagnosis_data.get('chief_complaint', ''),
            tongue_body_color=diagnosis_data.get('tongue_body_color', ''),
            tongue_coating_color=diagnosis_data.get('tongue_coating_color', ''),
            pulse_overall=diagnosis_data.get('pulse_overall', ''),
            symptoms=diagnosis_data.get('symptoms', []),
            additional_notes=diagnosis_data.get('notes', ''),
        )

        # Get prescription recommendation for top syndrome
        prescription_recommendation = None
        if diagnosis_result['syndromes']:
            top_syndrome_code = diagnosis_result['syndromes'][0]['syndrome_code']

            patient_age = None
            patient_gender = None
            if patient_data:
                patient_age = patient_data.get('age')
                patient_gender = patient_data.get('gender')

            prescription_recommendation = self.recommend_prescription(
                syndrome_code=top_syndrome_code,
                patient_age=patient_age,
                patient_gender=patient_gender,
            )

        # Get patent medicine recommendations
        patent_medicine_recommendations = None
        if diagnosis_result['syndromes']:
            top_syndrome_code = diagnosis_result['syndromes'][0]['syndrome_code']
            patent_medicine_recommendations = self.recommend_patent_medicines(
                syndrome_code=top_syndrome_code,
                patient_age=patient_age if patient_data else None,
            )

        return {
            'diagnosis': diagnosis_result,
            'prescription': prescription_recommendation,
            'patent_medicines': patent_medicine_recommendations,
            'timestamp': None,  # Will be set by view
            'disclaimer': '⚠️ AI建议仅供参考，需要执业医师审核确认 | AI suggestions are for reference only and require practitioner review.',
        }

    def recommend_patent_medicines(
        self,
        syndrome_code: str,
        patient_age: int = None
    ) -> List[Dict]:
        """
        Recommend modern Chinese patent medicines based on syndrome
        根据证型推荐现代中成药

        Args:
            syndrome_code: Syndrome code (e.g., 'SYN001')
            patient_age: Patient age for dosage consideration

        Returns:
            List of patent medicine recommendations
        """
        # Patent medicine recommendations by syndrome
        PATENT_MEDICINE_RECOMMENDATIONS = {
            'SYN001': [  # Qi Deficiency
                {
                    'code': 'PM002',
                    'name': '补中益气丸 | Bu Zhong Yi Qi Wan',
                    'reason': '适用于脾胃气虚、中气下陷 | Suitable for Spleen-Stomach Qi deficiency',
                    'priority': 1,
                },
                {
                    'code': 'PM008',
                    'name': '归脾丸 | Gui Pi Wan',
                    'reason': '适用于心脾两虚、气短心悸 | Suitable for Heart-Spleen deficiency',
                    'priority': 2,
                },
            ],
            'SYN002': [  # Blood Deficiency
                {
                    'code': 'PM008',
                    'name': '归脾丸 | Gui Pi Wan',
                    'reason': '养血安神，益气健脾 | Nourish Blood, Calm Spirit',
                    'priority': 1,
                },
            ],
            'SYN003': [  # Yang Deficiency
                {
                    'code': 'PM010',
                    'name': '金匮肾气丸 | Jin Gui Shen Qi Wan',
                    'reason': '温补肾阳，适用于肾阳不足 | Warm Kidney Yang',
                    'priority': 1,
                },
            ],
            'SYN004': [  # Yin Deficiency
                {
                    'code': 'PM001',
                    'name': '六味地黄丸 | Liu Wei Di Huang Wan',
                    'reason': '滋阴补肾，适用于肾阴虚 | Nourish Kidney Yin',
                    'priority': 1,
                },
            ],
            'SYN005': [  # Heat Pattern
                {
                    'code': 'PM007',
                    'name': '板蓝根颗粒 | Ban Lan Gen Ke Li',
                    'reason': '清热解毒，适用于肺胃热盛 | Clear Heat and Resolve Toxicity',
                    'priority': 1,
                },
            ],
            'SYN006': [  # Cold Pattern
                {
                    'code': 'PM003',
                    'name': '感冒清热颗粒 | Gan Mao Qing Re Ke Li',
                    'reason': '疏风散寒，解表清热 | Disperse Wind-Cold',
                    'priority': 1,
                },
            ],
            'SYN007': [  # Dampness
                {
                    'code': 'PM009',
                    'name': '藿香正气口服液 | Huo Xiang Zheng Qi Oral Liquid',
                    'reason': '解表化湿，理气和中 | Transform Dampness',
                    'priority': 1,
                },
            ],
            'SYN008': [  # Blood Stasis
                {
                    'code': 'PM006',
                    'name': '复方丹参片 | Compound Danshen Tablets',
                    'reason': '活血化瘀，理气止痛 | Invigorate Blood and Resolve Stasis',
                    'priority': 1,
                },
                {
                    'code': 'PM005',
                    'name': '云南白药胶囊 | Yunnan Baiyao Capsules',
                    'reason': '化瘀止血，活血止痛 | Transform Stasis, Stop Bleeding',
                    'priority': 2,
                },
            ],
        }

        recommendations = []

        if syndrome_code in PATENT_MEDICINE_RECOMMENDATIONS:
            medicines = PATENT_MEDICINE_RECOMMENDATIONS[syndrome_code]

            for med in medicines:
                rec = {
                    'code': med['code'],
                    'name': med['name'],
                    'reason': med['reason'],
                    'priority': med['priority'],
                }

                # Add age-specific notes
                if patient_age:
                    if patient_age < 12:
                        rec['age_note'] = '儿童用量请遵医嘱 | Children: follow practitioner instructions'
                    elif patient_age > 65:
                        rec['age_note'] = '老年患者请在医师指导下使用 | Elderly: use under guidance'

                recommendations.append(rec)

        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'])

        return recommendations
