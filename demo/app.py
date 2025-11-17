"""
AI增强中医诊疗系统 - 演示版本
Demo version of AI-Enhanced TCM Clinical System
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# 加载模拟数据
def load_data(filename):
    data_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ==================== 页面路由 ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnosis')
def diagnosis_page():
    return render_template('diagnosis.html')

@app.route('/prescription')
def prescription_page():
    return render_template('prescription.html')

@app.route('/acupuncture')
def acupuncture_page():
    return render_template('acupuncture.html')

@app.route('/alerts')
def alerts_page():
    return render_template('alerts.html')

# ==================== API路由 ====================

@app.route('/api/ai/diagnosis', methods=['POST'])
def ai_diagnosis():
    """AI辅助诊断 - 分析症状，推荐证型"""
    data = request.json
    symptoms = data.get('symptoms', [])
    tongue = data.get('tongue', '')
    pulse = data.get('pulse', '')

    # 模拟AI分析
    syndromes = load_data('syndromes.json')

    # 简单的症状-证型匹配逻辑
    result = analyze_symptoms(symptoms, tongue, pulse, syndromes)

    return jsonify(result)

@app.route('/api/ai/prescription', methods=['POST'])
def ai_prescription():
    """AI辅助开方 - 根据证型推荐方剂"""
    data = request.json
    syndrome = data.get('syndrome', '')
    symptoms = data.get('symptoms', [])

    formulas = load_data('formulas.json')
    herbs = load_data('herbs.json')

    result = recommend_formula(syndrome, symptoms, formulas, herbs)

    return jsonify(result)

@app.route('/api/ai/acupoints', methods=['POST'])
def ai_acupoints():
    """AI辅助选穴 - 根据证型推荐穴位"""
    data = request.json
    syndrome = data.get('syndrome', '')
    symptoms = data.get('symptoms', [])

    acupoints = load_data('acupoints.json')

    result = recommend_acupoints(syndrome, symptoms, acupoints)

    return jsonify(result)

@app.route('/api/acupoints/search', methods=['GET'])
def search_acupoints():
    """搜索穴位"""
    query = request.args.get('q', '')
    acupoints = load_data('acupoints.json')

    results = []
    for point in acupoints:
        if (query.lower() in point['name_chinese'].lower() or
            query.lower() in point['name_pinyin'].lower() or
            query.lower() in point['code'].lower()):
            results.append(point)

    return jsonify(results[:10])

@app.route('/api/acupoints/<code>', methods=['GET'])
def get_acupoint(code):
    """获取穴位详情"""
    acupoints = load_data('acupoints.json')

    for point in acupoints:
        if point['code'].upper() == code.upper():
            return jsonify(point)

    return jsonify({'error': 'Acupoint not found'}), 404

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """获取传染病预警和更新提醒"""
    alerts = load_data('alerts.json')
    return jsonify(alerts)

@app.route('/api/herbs/search', methods=['GET'])
def search_herbs():
    """搜索中药"""
    query = request.args.get('q', '')
    herbs = load_data('herbs.json')

    results = []
    for herb in herbs:
        if (query.lower() in herb['name_chinese'].lower() or
            query.lower() in herb['name_pinyin'].lower()):
            results.append(herb)

    return jsonify(results[:10])

@app.route('/api/safety-check', methods=['POST'])
def safety_check():
    """处方安全检查"""
    data = request.json
    herbs = data.get('herbs', [])
    patient_meds = data.get('patient_medications', [])

    warnings = check_prescription_safety(herbs, patient_meds)

    return jsonify(warnings)

# ==================== AI分析函数 ====================

def analyze_symptoms(symptoms, tongue, pulse, syndromes):
    """分析症状，推荐证型"""

    # 症状关键词映射
    symptom_keywords = {
        '发热': ['风热', '实热', '阴虚'],
        '恶寒': ['风寒', '阳虚'],
        '头痛': ['风寒', '风热', '肝阳上亢'],
        '咳嗽': ['风寒', '风热', '肺热'],
        '口干': ['阴虚', '热证'],
        '口苦': ['肝胆湿热', '少阳病'],
        '失眠': ['心肾不交', '肝郁化火'],
        '腰酸': ['肾虚', '肾阳虚', '肾阴虚'],
        '乏力': ['气虚', '脾虚'],
        '胸闷': ['气滞', '痰湿'],
        '胁痛': ['肝气郁结', '肝胆湿热'],
        '腹胀': ['脾虚', '食滞'],
        '便秘': ['热结', '阴虚'],
        '腹泻': ['脾虚', '湿热'],
        '多梦': ['心肾不交', '心血虚'],
        '盗汗': ['阴虚'],
        '自汗': ['气虚', '阳虚'],
    }

    # 舌象分析
    tongue_patterns = {
        '淡白': ['气虚', '血虚', '阳虚'],
        '红': ['热证', '阴虚'],
        '绛': ['热入营血', '阴虚火旺'],
        '紫': ['瘀血'],
        '薄白苔': ['表证', '正常'],
        '白腻苔': ['寒湿', '痰湿'],
        '黄苔': ['热证'],
        '黄腻苔': ['湿热'],
        '少苔': ['阴虚'],
        '无苔': ['胃阴虚'],
    }

    # 脉象分析
    pulse_patterns = {
        '浮': ['表证'],
        '沉': ['里证'],
        '迟': ['寒证'],
        '数': ['热证'],
        '虚': ['虚证'],
        '实': ['实证'],
        '弦': ['肝病', '痛证'],
        '滑': ['痰湿', '食滞'],
        '涩': ['瘀血', '精血亏虚'],
        '细': ['血虚', '阴虚'],
        '洪': ['热盛'],
    }

    # 计算证型得分
    syndrome_scores = {}

    # 分析症状
    for symptom in symptoms:
        for keyword, patterns in symptom_keywords.items():
            if keyword in symptom:
                for pattern in patterns:
                    syndrome_scores[pattern] = syndrome_scores.get(pattern, 0) + 1

    # 分析舌象
    for keyword, patterns in tongue_patterns.items():
        if keyword in tongue:
            for pattern in patterns:
                syndrome_scores[pattern] = syndrome_scores.get(pattern, 0) + 2

    # 分析脉象
    for keyword, patterns in pulse_patterns.items():
        if keyword in pulse:
            for pattern in patterns:
                syndrome_scores[pattern] = syndrome_scores.get(pattern, 0) + 2

    # 排序获取最可能的证型
    sorted_syndromes = sorted(syndrome_scores.items(), key=lambda x: x[1], reverse=True)

    # 生成病因病机分析
    if sorted_syndromes:
        primary_syndrome = sorted_syndromes[0][0]
        confidence = min(95, sorted_syndromes[0][1] * 10)
    else:
        primary_syndrome = "待定"
        confidence = 0

    # 从数据库获取详细信息
    syndrome_details = None
    for s in syndromes:
        if s['name'] == primary_syndrome or primary_syndrome in s['name']:
            syndrome_details = s
            break

    result = {
        'primary_syndrome': primary_syndrome,
        'confidence': confidence,
        'syndrome_scores': dict(sorted_syndromes[:5]),
        'etiology_analysis': generate_etiology(symptoms, tongue, pulse, primary_syndrome),
        'pathogenesis': generate_pathogenesis(primary_syndrome),
        'treatment_principle': get_treatment_principle(primary_syndrome),
        'suggested_inquiries': generate_suggested_inquiries(symptoms, primary_syndrome),
        'syndrome_details': syndrome_details
    }

    return result

def generate_etiology(symptoms, tongue, pulse, syndrome):
    """生成病因分析"""
    etiology_map = {
        '风寒': '外感风寒之邪，束表闭肺',
        '风热': '外感风热之邪，侵袭肺卫',
        '肝气郁结': '情志不遂，肝失疏泄',
        '脾虚': '饮食不节，劳倦过度，损伤脾气',
        '肾虚': '先天不足或房劳过度，肾精亏虚',
        '阴虚': '热病伤阴或久病耗阴',
        '阳虚': '久病伤阳或年老体衰',
        '气虚': '久病体虚，脾肺气虚',
        '血虚': '失血过多或生化不足',
        '痰湿': '脾失健运，痰湿内生',
        '湿热': '外感湿热或饮食不洁',
        '瘀血': '气滞血瘀或外伤',
    }

    for key, value in etiology_map.items():
        if key in syndrome:
            return value

    return '病因待进一步分析'

def generate_pathogenesis(syndrome):
    """生成病机分析"""
    pathogenesis_map = {
        '风寒': '风寒束表，卫阳被遏，肺气不宣',
        '风热': '风热犯表，肺失清肃，卫气失和',
        '肝气郁结': '肝失疏泄，气机郁滞，横逆犯脾',
        '脾虚': '脾失健运，水谷不化，清阳不升',
        '肾虚': '肾精亏虚，髓海不足，腰府失养',
        '阴虚': '阴液亏虚，虚热内生，脏腑失润',
        '阳虚': '阳气亏虚，温煦失职，阴寒内生',
        '气虚': '元气亏虚，脏腑功能减退',
        '血虚': '血液亏虚，脏腑经络失养',
        '痰湿': '痰湿中阻，气机不畅',
        '湿热': '湿热蕴结，气机阻滞',
        '瘀血': '瘀血阻络，不通则痛',
    }

    for key, value in pathogenesis_map.items():
        if key in syndrome:
            return value

    return '病机待进一步分析'

def get_treatment_principle(syndrome):
    """获取治则治法"""
    principles = {
        '风寒': '辛温解表，宣肺散寒',
        '风热': '辛凉解表，清热宣肺',
        '肝气郁结': '疏肝理气，解郁和胃',
        '脾虚': '健脾益气，升阳举陷',
        '肾虚': '补肾填精，温阳益气',
        '阴虚': '滋阴清热，养阴生津',
        '阳虚': '温补阳气，散寒通络',
        '气虚': '补气健脾，益气固表',
        '血虚': '补血养血，滋阴润燥',
        '痰湿': '燥湿化痰，理气和中',
        '湿热': '清热利湿，分消走泄',
        '瘀血': '活血化瘀，通络止痛',
    }

    for key, value in principles.items():
        if key in syndrome:
            return value

    return '治则待进一步确定'

def generate_suggested_inquiries(symptoms, syndrome):
    """生成建议问诊内容"""
    inquiries = []

    # 基于证型的问诊建议
    syndrome_inquiries = {
        '风寒': ['是否恶寒重发热轻？', '有无头身疼痛？', '鼻塞流涕情况？'],
        '风热': ['是否发热重恶寒轻？', '咽喉是否红肿疼痛？', '口渴情况？'],
        '肝气郁结': ['情志是否抑郁？', '胸胁是否胀满？', '月经情况（女性）？'],
        '脾虚': ['食欲如何？', '大便情况？', '是否腹胀？'],
        '肾虚': ['腰膝是否酸软？', '小便情况？', '性功能情况？'],
        '阴虚': ['是否有五心烦热？', '盗汗情况？', '口干咽燥？'],
        '阳虚': ['是否畏寒肢冷？', '小便清长？', '大便溏薄？'],
    }

    for key, questions in syndrome_inquiries.items():
        if key in syndrome:
            inquiries.extend(questions)
            break

    # 通用问诊
    if not inquiries:
        inquiries = [
            '睡眠质量如何？',
            '饮食情况？',
            '二便情况？',
            '有无其他不适？'
        ]

    return inquiries

def recommend_formula(syndrome, symptoms, formulas, herbs):
    """根据证型推荐方剂"""

    # 证型-方剂映射
    syndrome_formula_map = {
        '风寒': ['麻黄汤', '桂枝汤', '荆防败毒散'],
        '风热': ['银翘散', '桑菊饮'],
        '肝气郁结': ['逍遥散', '柴胡疏肝散'],
        '脾虚': ['四君子汤', '参苓白术散', '补中益气汤'],
        '肾阳虚': ['金匮肾气丸', '右归丸'],
        '肾阴虚': ['六味地黄丸', '左归丸'],
        '阴虚': ['六味地黄丸', '知柏地黄丸'],
        '阳虚': ['金匮肾气丸', '附子理中丸'],
        '气虚': ['四君子汤', '补中益气汤'],
        '血虚': ['四物汤', '归脾汤'],
        '痰湿': ['二陈汤', '平胃散'],
        '湿热': ['龙胆泻肝汤', '茵陈蒿汤'],
        '瘀血': ['血府逐瘀汤', '桃红四物汤'],
        '肝阳上亢': ['天麻钩藤饮', '镇肝熄风汤'],
    }

    # 查找匹配的方剂
    recommended_formulas = []
    for key, formula_names in syndrome_formula_map.items():
        if key in syndrome:
            for fname in formula_names:
                for f in formulas:
                    if f['name'] == fname:
                        recommended_formulas.append(f)

    if not recommended_formulas and formulas:
        # 默认返回第一个方剂作为示例
        recommended_formulas = [formulas[0]]

    # 主方
    primary_formula = recommended_formulas[0] if recommended_formulas else None

    # 加减建议
    modifications = generate_modifications(symptoms)

    # 安全检查
    safety_warnings = []
    if primary_formula:
        for herb in primary_formula.get('composition', []):
            herb_name = herb['herb']
            # 检查特殊禁忌
            if herb_name == '麻黄':
                safety_warnings.append({
                    'herb': '麻黄',
                    'warning': '高血压、心脏病患者慎用',
                    'severity': 'medium'
                })
            if herb_name == '附子':
                safety_warnings.append({
                    'herb': '附子',
                    'warning': '有毒，须先煎30-60分钟',
                    'severity': 'high'
                })

    result = {
        'primary_formula': primary_formula,
        'alternative_formulas': recommended_formulas[1:3] if len(recommended_formulas) > 1 else [],
        'modifications': modifications,
        'safety_warnings': safety_warnings,
        'modern_research': get_modern_research(primary_formula['name'] if primary_formula else ''),
        'match_score': 85 if primary_formula else 0
    }

    return result

def generate_modifications(symptoms):
    """生成加减建议"""
    modifications = []

    symptom_mods = {
        '头痛': {'add': [{'herb': '白芷', 'dosage': '10g', 'reason': '祛风止痛'}]},
        '咳嗽': {'add': [{'herb': '杏仁', 'dosage': '10g', 'reason': '止咳平喘'}]},
        '痰多': {'add': [{'herb': '半夏', 'dosage': '9g', 'reason': '燥湿化痰'}]},
        '口渴': {'add': [{'herb': '天花粉', 'dosage': '15g', 'reason': '生津止渴'}]},
        '失眠': {'add': [{'herb': '酸枣仁', 'dosage': '15g', 'reason': '养心安神'}]},
        '便秘': {'add': [{'herb': '大黄', 'dosage': '6g', 'reason': '泻热通便'}]},
    }

    for symptom in symptoms:
        for key, mod in symptom_mods.items():
            if key in symptom:
                modifications.append({
                    'condition': symptom,
                    'add_herbs': mod.get('add', []),
                    'remove_herbs': mod.get('remove', [])
                })

    return modifications

def get_modern_research(formula_name):
    """获取现代研究信息"""
    research_data = {
        '麻黄汤': {
            'pharmacology': ['麻黄碱具有发汗、平喘作用', '桂枝有解热镇痛作用'],
            'clinical_studies': ['治疗流感有效率85%', '缩短病程2-3天'],
            'evidence_level': 'B级'
        },
        '银翘散': {
            'pharmacology': ['金银花具有广谱抗菌作用', '连翘有抗病毒作用'],
            'clinical_studies': ['治疗上呼吸道感染有效率90%'],
            'evidence_level': 'A级'
        },
        '逍遥散': {
            'pharmacology': ['柴胡具有抗抑郁作用', '白芍有镇静作用'],
            'clinical_studies': ['治疗肝郁脾虚证有效率88%'],
            'evidence_level': 'B级'
        },
        '六味地黄丸': {
            'pharmacology': ['熟地黄有滋补作用', '山茱萸有抗衰老作用'],
            'clinical_studies': ['调节免疫功能', '改善肾功能'],
            'evidence_level': 'A级'
        },
    }

    return research_data.get(formula_name, {
        'pharmacology': ['研究进行中'],
        'clinical_studies': ['临床研究进行中'],
        'evidence_level': '待定'
    })

def recommend_acupoints(syndrome, symptoms, acupoints):
    """根据证型推荐穴位"""

    # 证型-穴位映射
    syndrome_points = {
        '风寒': {
            'primary': ['LU7', 'LI4', 'BL12', 'GV14'],
            'reason': '宣肺解表，祛风散寒'
        },
        '风热': {
            'primary': ['LI4', 'LI11', 'GV14', 'LU11'],
            'reason': '清热解表，宣肺利咽'
        },
        '肝气郁结': {
            'primary': ['LR3', 'LR14', 'PC6', 'GB34'],
            'reason': '疏肝理气，调畅气机'
        },
        '脾虚': {
            'primary': ['ST36', 'SP6', 'CV12', 'BL20'],
            'reason': '健脾益气，和胃调中'
        },
        '肾虚': {
            'primary': ['KI3', 'BL23', 'GV4', 'CV4'],
            'reason': '补肾益精，温阳固本'
        },
        '阴虚': {
            'primary': ['KI3', 'KI6', 'SP6', 'LU7'],
            'reason': '滋阴清热，养阴润燥'
        },
        '肝阳上亢': {
            'primary': ['LR3', 'GB20', 'LI11', 'KI1'],
            'reason': '平肝潜阳，清热熄风'
        },
    }

    # 查找对应穴位
    primary_points = []
    selection_reason = ''

    for key, value in syndrome_points.items():
        if key in syndrome:
            for code in value['primary']:
                for point in acupoints:
                    if point['code'] == code:
                        primary_points.append({
                            **point,
                            'technique': get_needling_technique(syndrome, code)
                        })
            selection_reason = value['reason']
            break

    # 配穴建议
    secondary_points = get_secondary_points(symptoms, acupoints)

    # 随症加减
    symptom_additions = get_symptom_point_additions(symptoms, acupoints)

    result = {
        'primary_points': primary_points,
        'secondary_points': secondary_points,
        'symptom_additions': symptom_additions,
        'selection_reason': selection_reason,
        'treatment_plan': {
            'frequency': '隔日1次',
            'sessions': 10,
            'duration': '30分钟',
            'precautions': ['留针期间注意保暖', '针后避免当风']
        },
        'classic_references': get_classic_references(syndrome)
    }

    return result

def get_needling_technique(syndrome, point_code):
    """获取针刺手法"""
    # 虚证用补法，实证用泻法
    if any(x in syndrome for x in ['虚', '阴虚', '阳虚', '气虚', '血虚']):
        return {
            'method': '补法',
            'manipulation': '轻刺激，慢捻转',
            'retention': '20-30分钟'
        }
    else:
        return {
            'method': '泻法',
            'manipulation': '强刺激，快捻转',
            'retention': '15-20分钟'
        }

def get_secondary_points(symptoms, acupoints):
    """获取配穴"""
    secondary = []

    # 四关穴常配
    four_gates = ['LI4', 'LR3']
    for code in four_gates:
        for point in acupoints:
            if point['code'] == code:
                secondary.append({
                    **point,
                    'pairing_reason': '四关穴，行气活血'
                })

    return secondary[:2]

def get_symptom_point_additions(symptoms, acupoints):
    """随症加减穴位"""
    additions = []

    symptom_points = {
        '头痛': ['GV20', 'GB20'],
        '失眠': ['HT7', 'SP6'],
        '便秘': ['ST25', 'SJ6'],
        '腹泻': ['ST25', 'CV6'],
        '咳嗽': ['LU7', 'CV22'],
    }

    for symptom in symptoms:
        for key, codes in symptom_points.items():
            if key in symptom:
                points = []
                for code in codes:
                    for point in acupoints:
                        if point['code'] == code:
                            points.append(point)
                if points:
                    additions.append({
                        'symptom': symptom,
                        'add_points': points
                    })

    return additions

def get_classic_references(syndrome):
    """获取经典依据"""
    references = {
        '风寒': [
            {'source': '《针灸甲乙经》', 'content': '风寒伤卫，取风池、风门、合谷'},
        ],
        '肝气郁结': [
            {'source': '《针灸大成》', 'content': '肝郁气滞，取太冲、期门、内关'},
        ],
        '脾虚': [
            {'source': '《难经》', 'content': '虚则补其母，脾土虚取足三里'},
        ],
    }

    for key, refs in references.items():
        if key in syndrome:
            return refs

    return [{'source': '《针灸学》', 'content': '辨证取穴，因症施治'}]

def check_prescription_safety(herbs, patient_meds):
    """处方安全检查"""
    warnings = []

    # 十八反
    incompatible_pairs = [
        (['甘草'], ['甘遂', '大戟', '海藻', '芫花']),
        (['乌头', '附子'], ['半夏', '瓜蒌', '贝母', '白蔹', '白及']),
        (['藜芦'], ['人参', '沙参', '丹参', '玄参', '细辛', '芍药']),
    ]

    herb_names = [h['name'] if isinstance(h, dict) else h for h in herbs]

    for group1, group2 in incompatible_pairs:
        for h1 in group1:
            if h1 in herb_names:
                for h2 in group2:
                    if h2 in herb_names:
                        warnings.append({
                            'type': '十八反',
                            'herbs': [h1, h2],
                            'severity': 'high',
                            'message': f'{h1}与{h2}相反，不宜同用'
                        })

    # 中西药相互作用
    herb_drug_interactions = {
        '甘草': {
            'drugs': ['地高辛', '利尿剂', '降压药'],
            'effect': '可能导致低钾血症'
        },
        '丹参': {
            'drugs': ['华法林', '阿司匹林'],
            'effect': '增加出血风险'
        },
        '人参': {
            'drugs': ['华法林', '降糖药'],
            'effect': '影响药效'
        },
        '麻黄': {
            'drugs': ['降压药', 'MAOIs'],
            'effect': '可能升高血压'
        },
    }

    for herb_name in herb_names:
        if herb_name in herb_drug_interactions:
            interaction = herb_drug_interactions[herb_name]
            for drug in patient_meds:
                if any(d in drug for d in interaction['drugs']):
                    warnings.append({
                        'type': '中西药相互作用',
                        'herb': herb_name,
                        'drug': drug,
                        'severity': 'medium',
                        'message': f'{herb_name}与{drug}：{interaction["effect"]}'
                    })

    return {
        'has_warnings': len(warnings) > 0,
        'warnings': warnings,
        'checked_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
