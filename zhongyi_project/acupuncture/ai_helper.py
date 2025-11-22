"""
AI助手模块 | AI Helper Module
Provides AI-powered acupoint recommendations based on symptoms and TCM diagnosis.
"""
from typing import Dict, List, Tuple


class AcupointAIHelper:
    """AI助手用于针灸穴位推荐 | AI Assistant for Acupuncture Point Recommendations"""

    # 症状到穴位映射数据库 | Symptom to Acupoint Mapping Database
    SYMPTOM_ACUPOINT_MAP = {
        # 头痛相关 | Headache related
        '头痛': ['GV20', 'GB20', 'LI4', 'LR3', 'BL2'],
        'headache': ['GV20', 'GB20', 'LI4', 'LR3', 'BL2'],
        '偏头痛': ['GB20', 'GB8', 'TB5', 'LR3'],
        'migraine': ['GB20', 'GB8', 'TB5', 'LR3'],
        
        # 颈肩疼痛 | Neck and shoulder pain
        '颈痛': ['GB20', 'GB21', 'SI3', 'BL10'],
        'neck pain': ['GB20', 'GB21', 'SI3', 'BL10'],
        '肩痛': ['GB21', 'LI15', 'SI9', 'TB14'],
        'shoulder pain': ['GB21', 'LI15', 'SI9', 'TB14'],
        
        # 失眠 | Insomnia
        '失眠': ['HT7', 'PC6', 'SP6', 'GV20', 'KI3'],
        'insomnia': ['HT7', 'PC6', 'SP6', 'GV20', 'KI3'],
        
        # 消化系统 | Digestive system
        '胃痛': ['ST36', 'PC6', 'CV12', 'ST25'],
        'stomach pain': ['ST36', 'PC6', 'CV12', 'ST25'],
        '腹痛': ['ST25', 'ST36', 'SP4', 'CV12'],
        'abdominal pain': ['ST25', 'ST36', 'SP4', 'CV12'],
        '便秘': ['ST25', 'ST36', 'ST37', 'LI4'],
        'constipation': ['ST25', 'ST36', 'ST37', 'LI4'],
        '腹泻': ['ST25', 'ST36', 'ST37', 'SP9'],
        'diarrhea': ['ST25', 'ST36', 'ST37', 'SP9'],
        
        # 呼吸系统 | Respiratory system
        '咳嗽': ['LU7', 'LU5', 'BL13', 'CV17'],
        'cough': ['LU7', 'LU5', 'BL13', 'CV17'],
        '哮喘': ['LU7', 'CV17', 'BL13', 'ST40'],
        'asthma': ['LU7', 'CV17', 'BL13', 'ST40'],
        
        # 疼痛 | Pain
        '腰痛': ['BL23', 'BL40', 'GV3', 'KI3'],
        'lower back pain': ['BL23', 'BL40', 'GV3', 'KI3'],
        '膝痛': ['ST35', 'SP9', 'SP10', 'GB34'],
        'knee pain': ['ST35', 'SP9', 'SP10', 'GB34'],
        
        # 情绪相关 | Emotional
        '焦虑': ['HT7', 'PC6', 'GV20', 'LR3'],
        'anxiety': ['HT7', 'PC6', 'GV20', 'LR3'],
        '抑郁': ['GV20', 'PC6', 'HT7', 'LR3', 'SP6'],
        'depression': ['GV20', 'PC6', 'HT7', 'LR3', 'SP6'],
        '压力': ['GV20', 'LI4', 'LR3', 'HT7'],
        'stress': ['GV20', 'LI4', 'LR3', 'HT7'],
        
        # 妇科 | Gynecology
        '痛经': ['SP6', 'SP8', 'CV4', 'LR3'],
        'dysmenorrhea': ['SP6', 'SP8', 'CV4', 'LR3'],
        '月经不调': ['SP6', 'CV4', 'ST36', 'LR3'],
        'irregular menstruation': ['SP6', 'CV4', 'ST36', 'LR3'],
    }

    # 中医辨证到穴位映射 | TCM Pattern to Acupoint Mapping
    TCM_PATTERN_MAP = {
        '气滞血瘀': ['LR3', 'SP6', 'SP10', 'LI4'],
        '肝阳上亢': ['LR3', 'GB20', 'GV20', 'KI3'],
        '肝郁气滞': ['LR3', 'LR14', 'GB34', 'PC6'],
        '脾胃虚弱': ['ST36', 'SP6', 'CV12', 'BL20'],
        '肾阳虚': ['KI3', 'BL23', 'CV4', 'GV4'],
        '肾阴虚': ['KI3', 'KI7', 'SP6', 'CV4'],
        '心脾两虚': ['HT7', 'SP6', 'ST36', 'BL15', 'BL20'],
        '痰湿': ['ST40', 'SP9', 'CV12', 'SP6'],
    }

    @classmethod
    def recommend_acupoints(
        cls,
        chief_complaint: str,
        tcm_diagnosis: str = ''
    ) -> tuple:
        recommended_points = set()
        reasoning_parts = []
        
        complaint_lower = chief_complaint.lower()
        for symptom, points in cls.SYMPTOM_ACUPOINT_MAP.items():
            if symptom in complaint_lower:
                recommended_points.update(points)
                reasoning_parts.append(
                    f"基于症状'{symptom}'推荐: {', '.join(points)}"
                )
        
        if tcm_diagnosis:
            diagnosis_lower = tcm_diagnosis.lower()
            for pattern, points in cls.TCM_PATTERN_MAP.items():
                if pattern in diagnosis_lower:
                    recommended_points.update(points)
                    reasoning_parts.append(
                        f"基于辨证'{pattern}'推荐: {', '.join(points)}"
                    )
        
        if len(recommended_points) == 0:
            recommended_points = {'LI4', 'LR3', 'ST36', 'SP6'}
            confidence = 30.0
            reasoning_parts.append("未找到特定匹配，推荐常用穴位")
        elif len(reasoning_parts) == 1:
            confidence = 70.0
        else:
            confidence = 85.0

        reasoning = '\n'.join(reasoning_parts)
        recommended_list = sorted(list(recommended_points))

        return recommended_list, confidence, reasoning
