# AI X光片读解、现代药物字典与Chiropractic手法系统技术规格

## 文档信息
- **版本**: 1.0
- **创建日期**: 2024年
- **适用范围**: 马来西亚中医诊所系统
- **合规标准**: Malaysia T&CM Act 2016, PDPA 2010, MDA (Medical Device Act)

---

## 目录
1. [AI X光片读解分析系统](#1-ai-x光片读解分析系统)
2. [现代AI药物字典系统](#2-现代ai药物字典系统)
3. [现代Chiropractic手法数据库](#3-现代chiropractic手法数据库)
4. [统一更新与提醒机制](#4-统一更新与提醒机制)
5. [数据库设计](#5-数据库设计)
6. [API接口设计](#6-api接口设计)
7. [界面设计](#7-界面设计)

---

## 1. AI X光片读解分析系统

### 1.1 系统概述

基于深度学习的医学影像AI分析系统，支持X光片智能读解，辅助医师诊断。

### 1.2 核心功能

#### 1.2.1 影像上传与处理

```yaml
支持格式:
  - DICOM (标准医学影像格式)
  - JPEG/PNG (普通图片格式)
  - CR/DR (数字X光)

预处理:
  - 自动图像增强
  - 对比度调整
  - 噪声消除
  - 边缘锐化
  - 标准化尺寸调整
```

#### 1.2.2 AI分析引擎

```python
class XRayAnalysisEngine:
    """X光片AI分析引擎"""

    def __init__(self):
        self.models = {
            'chest': ChestXRayModel(),      # 胸部X光
            'spine': SpineXRayModel(),       # 脊椎X光
            'bone': BoneXRayModel(),         # 骨骼X光
            'dental': DentalXRayModel(),     # 牙科X光
            'joint': JointXRayModel()        # 关节X光
        }

    def analyze(self, image, body_part):
        """分析X光片"""
        # 预处理图像
        processed = self.preprocess(image)

        # 选择对应模型
        model = self.models.get(body_part)

        # AI分析
        results = model.predict(processed)

        return {
            'findings': results['findings'],           # 发现
            'abnormalities': results['abnormalities'], # 异常
            'measurements': results['measurements'],   # 测量
            'confidence': results['confidence'],       # 置信度
            'suggestions': results['suggestions'],     # 建议
            'annotations': results['annotations']      # 标注
        }

    def generate_report(self, analysis_results):
        """生成分析报告"""
        return {
            'summary': self.summarize(analysis_results),
            'detailed_findings': analysis_results['findings'],
            'clinical_correlation': self.correlate_clinical(analysis_results),
            'tcm_implications': self.tcm_analysis(analysis_results),
            'recommendations': analysis_results['suggestions']
        }
```

#### 1.2.3 支持的X光类型

| 部位 | 检查项目 | AI功能 |
|------|----------|--------|
| **胸部** | 胸片PA/Lateral | 肺结节检测、心影大小、肺纹理分析 |
| **脊椎** | 颈/胸/腰椎 | 椎体排列、间隙测量、侧弯分析 |
| **骨骼** | 四肢骨骼 | 骨折检测、骨密度评估、关节炎 |
| **关节** | 膝/髋/肩/肘 | 关节间隙、骨赘、软组织肿胀 |
| **手部** | 手腕/手指 | 骨龄评估、关节炎、骨折 |
| **足部** | 足/踝 | 扁平足、骨刺、应力性骨折 |

#### 1.2.4 胸部X光AI分析

```python
class ChestXRayModel:
    """胸部X光AI模型"""

    def predict(self, image):
        """胸片分析"""
        results = {
            'findings': [],
            'abnormalities': [],
            'measurements': {},
            'confidence': 0.0,
            'suggestions': [],
            'annotations': []
        }

        # 1. 肺野分析
        lung_analysis = self.analyze_lungs(image)
        if lung_analysis['nodules']:
            results['findings'].append({
                'type': 'lung_nodule',
                'location': lung_analysis['nodule_location'],
                'size': lung_analysis['nodule_size'],
                'characteristics': lung_analysis['nodule_chars'],
                'confidence': lung_analysis['confidence']
            })

        # 2. 心脏分析
        cardiac_analysis = self.analyze_cardiac(image)
        results['measurements']['cardiothoracic_ratio'] = cardiac_analysis['ctr']
        if cardiac_analysis['ctr'] > 0.5:
            results['abnormalities'].append({
                'type': 'cardiomegaly',
                'severity': 'mild' if cardiac_analysis['ctr'] < 0.55 else 'moderate',
                'ctr_value': cardiac_analysis['ctr']
            })

        # 3. 骨骼结构
        bone_analysis = self.analyze_bones(image)
        results['findings'].extend(bone_analysis['findings'])

        # 4. 软组织
        soft_tissue = self.analyze_soft_tissue(image)
        results['findings'].extend(soft_tissue['findings'])

        return results

    def detectable_conditions(self):
        """可检测病变"""
        return [
            '肺结节/肿块',
            '肺炎/浸润',
            '肺不张',
            '气胸',
            '胸腔积液',
            '心脏扩大',
            '主动脉异常',
            '纵隔增宽',
            '肋骨骨折',
            '脊柱侧弯'
        ]
```

#### 1.2.5 脊椎X光AI分析

```python
class SpineXRayModel:
    """脊椎X光AI模型"""

    def predict(self, image):
        """脊椎分析"""
        results = {
            'findings': [],
            'abnormalities': [],
            'measurements': {},
            'confidence': 0.0,
            'suggestions': [],
            'annotations': []
        }

        # 1. 椎体排列分析
        alignment = self.analyze_alignment(image)
        results['measurements']['cervical_lordosis'] = alignment.get('cervical_angle')
        results['measurements']['lumbar_lordosis'] = alignment.get('lumbar_angle')
        results['measurements']['cobb_angle'] = alignment.get('cobb_angle')

        # 2. 椎间隙分析
        disc_spaces = self.analyze_disc_spaces(image)
        for disc in disc_spaces:
            if disc['narrowing']:
                results['abnormalities'].append({
                    'type': 'disc_space_narrowing',
                    'level': disc['level'],
                    'severity': disc['severity']
                })

        # 3. 椎体形态
        vertebral = self.analyze_vertebral_bodies(image)
        results['findings'].extend(vertebral['findings'])

        # 4. 骨赘检测
        osteophytes = self.detect_osteophytes(image)
        if osteophytes:
            results['abnormalities'].append({
                'type': 'osteophyte_formation',
                'locations': osteophytes['locations'],
                'severity': osteophytes['severity']
            })

        # 5. Chiropractic相关测量
        chiro_measurements = self.chiropractic_measurements(image)
        results['measurements'].update(chiro_measurements)

        return results

    def chiropractic_measurements(self, image):
        """脊骨神经科相关测量"""
        return {
            'atlas_alignment': self.measure_atlas(image),
            'cervical_curve': self.measure_cervical_curve(image),
            'lumbar_curve': self.measure_lumbar_curve(image),
            'pelvic_tilt': self.measure_pelvic_tilt(image),
            'leg_length_difference': self.estimate_leg_length(image),
            'subluxation_indicators': self.detect_subluxations(image)
        }
```

### 1.3 AI模型架构

```yaml
深度学习模型:
  基础架构:
    - ResNet-152 (特征提取)
    - DenseNet-121 (密集连接)
    - EfficientNet-B7 (高效网络)

  专业模型:
    - U-Net (图像分割)
    - Faster R-CNN (病变检测)
    - Vision Transformer (全局特征)

  集成策略:
    - 多模型投票
    - 加权平均
    - 级联决策

训练数据:
  - CheXpert (胸片数据集)
  - MURA (肌骨数据集)
  - VinDr-SpineXR (脊椎数据集)
  - 本地标注数据

性能指标:
  - 敏感性: >95%
  - 特异性: >90%
  - AUC: >0.95
```

### 1.4 中西医结合分析

```python
class IntegrativeXRayAnalysis:
    """中西医结合X光分析"""

    def tcm_correlation(self, xray_findings):
        """X光发现与中医关联"""
        correlations = []

        # 脊椎问题与经络关联
        spine_meridian_map = {
            'C1-C2': ['督脉', '膀胱经', '头面部症状'],
            'C3-C5': ['肺经', '心经', '上肢症状'],
            'C6-C7': ['大肠经', '小肠经', '肩颈症状'],
            'T1-T4': ['心经', '心包经', '胸闷心悸'],
            'T5-T8': ['肝经', '胆经', '脾经', '胃经'],
            'T9-T12': ['肾经', '三焦经', '腰腹症状'],
            'L1-L5': ['肾经', '膀胱经', '下肢症状'],
            'Sacrum': ['督脉', '任脉', '生殖泌尿']
        }

        for finding in xray_findings:
            if finding['type'] == 'disc_space_narrowing':
                level = finding['level']
                for spine_level, meridians in spine_meridian_map.items():
                    if level in spine_level:
                        correlations.append({
                            'western_finding': f'{level}椎间隙狭窄',
                            'tcm_meridians': meridians[:-1],
                            'tcm_symptoms': meridians[-1],
                            'treatment_points': self.get_treatment_points(level)
                        })

        return correlations

    def get_treatment_points(self, spine_level):
        """获取对应治疗穴位"""
        treatment_map = {
            'C': ['风池', '天柱', '大椎', '肩井'],
            'T': ['身柱', '至阳', '筋缩', '膈俞'],
            'L': ['肾俞', '大肠俞', '关元俞', '委中']
        }
        return treatment_map.get(spine_level[0], [])
```

### 1.5 报告生成

```python
class XRayReportGenerator:
    """X光报告生成器"""

    def generate_report(self, analysis, patient_info):
        """生成完整报告"""
        report = {
            'header': {
                'patient': patient_info,
                'exam_date': datetime.now(),
                'exam_type': analysis['exam_type'],
                'report_id': generate_uuid()
            },
            'technique': {
                'view': analysis['view'],
                'quality': analysis['image_quality']
            },
            'findings': {
                'summary': self.generate_summary(analysis),
                'detailed': analysis['findings'],
                'measurements': analysis['measurements']
            },
            'impression': self.generate_impression(analysis),
            'recommendations': {
                'western': analysis['suggestions'],
                'tcm': analysis['tcm_implications'],
                'follow_up': self.suggest_follow_up(analysis)
            },
            'ai_confidence': analysis['confidence'],
            'disclaimer': self.get_disclaimer()
        }

        return report

    def get_disclaimer(self):
        """AI辅助诊断免责声明"""
        return """
        本报告由AI辅助生成，仅供参考。
        最终诊断需由具有执照的医疗专业人员确认。
        AI分析不能替代专业医学判断。
        如有疑问，请咨询放射科医师。
        """
```

---

## 2. 现代AI药物字典系统

### 2.1 系统概述

全面的现代药物数据库，包含药物信息、相互作用、AI智能查询和中西药相互作用分析。

### 2.2 药物数据库结构

```python
class DrugDictionary:
    """现代药物字典"""

    drug_schema = {
        'basic_info': {
            'generic_name': str,           # 通用名
            'brand_names': list,           # 商品名列表
            'drug_class': str,             # 药物分类
            'atc_code': str,               # ATC分类码
            'cas_number': str,             # CAS号
            'molecular_formula': str,      # 分子式
            'molecular_weight': float      # 分子量
        },
        'clinical_info': {
            'indications': list,           # 适应症
            'contraindications': list,     # 禁忌症
            'dosage_forms': list,          # 剂型
            'routes': list,                # 给药途径
            'dosing': dict,                # 剂量信息
            'pharmacokinetics': dict,      # 药代动力学
            'pharmacodynamics': str        # 药效学
        },
        'safety_info': {
            'side_effects': list,          # 副作用
            'warnings': list,              # 警告
            'black_box_warning': str,      # 黑框警告
            'pregnancy_category': str,     # 妊娠分类
            'lactation': str               # 哺乳期
        },
        'interactions': {
            'drug_drug': list,             # 药物相互作用
            'drug_food': list,             # 药食相互作用
            'drug_herb': list,             # 中西药相互作用
            'drug_disease': list           # 药物疾病相互作用
        },
        'identifiers': {
            'ndc': list,                   # NDC码
            'rxcui': str,                  # RxNorm ID
            'drugbank_id': str,            # DrugBank ID
            'pubchem_cid': str             # PubChem ID
        },
        'regulatory': {
            'malaysia_registration': str,   # 马来西亚注册号
            'poison_schedule': str,         # 毒药分类
            'controlled_status': str        # 管制状态
        }
    }
```

### 2.3 AI智能查询功能

```python
class DrugAIAssistant:
    """药物AI助手"""

    def __init__(self):
        self.nlp_model = MedicalNLPModel()
        self.interaction_checker = InteractionChecker()
        self.dosing_calculator = DosingCalculator()

    def natural_language_query(self, query):
        """自然语言查询"""
        # 解析用户意图
        intent = self.nlp_model.parse_intent(query)

        if intent['type'] == 'drug_info':
            return self.get_drug_info(intent['drug_name'])
        elif intent['type'] == 'interaction':
            return self.check_interactions(intent['drugs'])
        elif intent['type'] == 'alternative':
            return self.find_alternatives(intent['drug_name'])
        elif intent['type'] == 'dosing':
            return self.calculate_dose(intent['params'])
        elif intent['type'] == 'indication':
            return self.find_by_indication(intent['condition'])

    def smart_search(self, query):
        """智能搜索"""
        results = {
            'exact_matches': [],
            'partial_matches': [],
            'similar_drugs': [],
            'related_conditions': []
        }

        # 多维度搜索
        results['exact_matches'] = self.search_exact(query)
        results['partial_matches'] = self.search_partial(query)
        results['similar_drugs'] = self.find_similar_drugs(query)
        results['related_conditions'] = self.find_related_conditions(query)

        return results

    def ai_drug_recommendation(self, diagnosis, patient_profile):
        """AI药物推荐"""
        recommendations = []

        # 根据诊断获取适用药物
        suitable_drugs = self.get_drugs_for_condition(diagnosis)

        for drug in suitable_drugs:
            # 检查患者禁忌
            contraindication_check = self.check_patient_contraindications(
                drug, patient_profile
            )

            # 检查药物相互作用
            interaction_check = self.check_current_medications(
                drug, patient_profile['current_medications']
            )

            # 检查中药相互作用
            herb_interaction = self.check_herb_interactions(
                drug, patient_profile['current_herbs']
            )

            if contraindication_check['safe'] and interaction_check['safe']:
                recommendations.append({
                    'drug': drug,
                    'confidence': self.calculate_confidence(drug, patient_profile),
                    'dosing': self.suggest_dosing(drug, patient_profile),
                    'warnings': interaction_check['warnings'] + herb_interaction['warnings'],
                    'alternatives': self.get_alternatives(drug)
                })

        return sorted(recommendations, key=lambda x: x['confidence'], reverse=True)
```

### 2.4 中西药相互作用数据库

```python
class HerbDrugInteractionDB:
    """中西药相互作用数据库"""

    interaction_levels = {
        'severe': '严重 - 避免同时使用',
        'major': '重要 - 需要监测',
        'moderate': '中度 - 谨慎使用',
        'minor': '轻微 - 注意观察'
    }

    def __init__(self):
        self.interactions = self.load_interactions()

    def check_interaction(self, drug, herb):
        """检查中西药相互作用"""
        key = f"{drug}_{herb}"

        if key in self.interactions:
            interaction = self.interactions[key]
            return {
                'has_interaction': True,
                'level': interaction['level'],
                'mechanism': interaction['mechanism'],
                'clinical_effect': interaction['clinical_effect'],
                'management': interaction['management'],
                'evidence_level': interaction['evidence'],
                'references': interaction['references']
            }

        # AI预测潜在相互作用
        predicted = self.predict_interaction(drug, herb)
        return {
            'has_interaction': predicted['probability'] > 0.5,
            'predicted': True,
            'probability': predicted['probability'],
            'potential_mechanism': predicted['mechanism'],
            'recommendation': '建议咨询药师或医师'
        }

    # 常见中西药相互作用示例
    common_interactions = [
        {
            'herb': '人参',
            'drug': 'Warfarin',
            'level': 'major',
            'mechanism': '人参可能降低Warfarin的抗凝效果',
            'management': '监测INR，可能需要调整Warfarin剂量'
        },
        {
            'herb': '当归',
            'drug': 'Warfarin',
            'level': 'major',
            'mechanism': '当归含有香豆素类化合物，增强抗凝作用',
            'management': '避免同时使用，或密切监测出血风险'
        },
        {
            'herb': '甘草',
            'drug': 'Digoxin',
            'level': 'major',
            'mechanism': '甘草可导致低钾血症，增加Digoxin毒性',
            'management': '监测血钾和Digoxin血药浓度'
        },
        {
            'herb': '麻黄',
            'drug': 'MAOIs',
            'level': 'severe',
            'mechanism': '麻黄碱与MAOIs合用可致高血压危象',
            'management': '禁止同时使用'
        },
        {
            'herb': '银杏',
            'drug': 'Aspirin',
            'level': 'moderate',
            'mechanism': '两者均有抗血小板作用，增加出血风险',
            'management': '监测出血症状'
        }
    ]
```

### 2.5 药物分类浏览

```yaml
药物分类系统:
  按ATC分类:
    A - 消化道和代谢:
      - A01 口腔科用药
      - A02 抗酸药
      - A03 胃肠解痉药
      - A04 止吐药
      - A10 糖尿病用药

    B - 血液和造血器官:
      - B01 抗血栓药
      - B02 止血药
      - B03 抗贫血药

    C - 心血管系统:
      - C01 心脏病用药
      - C02 抗高血压药
      - C03 利尿药
      - C07 β受体阻滞剂
      - C10 调脂药

    J - 抗感染药:
      - J01 抗菌药
      - J02 抗真菌药
      - J05 抗病毒药

    M - 肌肉骨骼系统:
      - M01 抗炎镇痛药
      - M02 外用药
      - M03 肌肉松弛药

    N - 神经系统:
      - N02 镇痛药
      - N03 抗癫痫药
      - N05 精神药物
      - N06 精神兴奋药

  按疾病分类:
    - 高血压用药
    - 糖尿病用药
    - 心脏病用药
    - 感染性疾病用药
    - 疼痛管理用药
    - 精神疾病用药
```

### 2.6 剂量计算器

```python
class DosingCalculator:
    """智能剂量计算器"""

    def calculate_dose(self, drug, patient):
        """计算个体化剂量"""
        base_dose = drug['standard_dose']

        adjustments = {
            'renal': self.renal_adjustment(drug, patient['renal_function']),
            'hepatic': self.hepatic_adjustment(drug, patient['hepatic_function']),
            'weight': self.weight_adjustment(drug, patient['weight']),
            'age': self.age_adjustment(drug, patient['age']),
            'genetic': self.pharmacogenomic_adjustment(drug, patient.get('genotype'))
        }

        final_dose = base_dose
        for factor, adjustment in adjustments.items():
            final_dose *= adjustment['multiplier']

        return {
            'recommended_dose': final_dose,
            'dose_range': drug['dose_range'],
            'frequency': drug['frequency'],
            'duration': drug['typical_duration'],
            'adjustments_made': adjustments,
            'monitoring': drug['monitoring_parameters']
        }

    def renal_adjustment(self, drug, renal_function):
        """肾功能剂量调整"""
        egfr = renal_function.get('eGFR', 90)

        if drug['renal_dosing']:
            for range_info in drug['renal_dosing']:
                if range_info['egfr_min'] <= egfr <= range_info['egfr_max']:
                    return {
                        'multiplier': range_info['adjustment'],
                        'reason': f"eGFR {egfr}: {range_info['instruction']}"
                    }

        return {'multiplier': 1.0, 'reason': 'No adjustment needed'}

    def pediatric_dosing(self, drug, child):
        """儿童剂量计算"""
        methods = {
            'weight_based': child['weight'] * drug['mg_per_kg'],
            'bsa_based': child['bsa'] * drug['mg_per_m2'],
            'age_based': drug['pediatric_doses'].get(child['age_group'])
        }

        # 选择最合适的方法
        preferred_method = drug.get('preferred_pediatric_method', 'weight_based')
        calculated_dose = methods[preferred_method]

        # 确保不超过成人剂量
        max_dose = drug['max_pediatric_dose'] or drug['standard_dose']
        final_dose = min(calculated_dose, max_dose)

        return {
            'dose': final_dose,
            'method': preferred_method,
            'max_dose': max_dose
        }
```

---

## 3. 现代Chiropractic手法数据库

### 3.1 系统概述

全面的脊骨神经科（Chiropractic）手法技术数据库，包含各种调整技术、适应症、3D演示和循证依据。

### 3.2 手法分类体系

```yaml
Chiropractic手法分类:

  1. 高速低幅推力技术 (HVLA):
    - Diversified Technique
    - Gonstead Technique
    - Thompson Drop Technique
    - Toggle Recoil

  2. 低力技术:
    - Activator Methods
    - Cox Flexion-Distraction
    - Sacro-Occipital Technique (SOT)
    - Craniosacral Therapy

  3. 软组织技术:
    - Active Release Technique (ART)
    - Graston Technique
    - Myofascial Release
    - Trigger Point Therapy

  4. 仪器辅助技术:
    - Activator Instrument
    - Impulse Adjusting
    - ArthroStim
    - ProAdjuster

  5. 特殊技术:
    - Upper Cervical Specific
    - Applied Kinesiology
    - Network Spinal Analysis
    - Torque Release Technique
```

### 3.3 手法数据结构

```python
class ChiropracticTechnique:
    """Chiropractic手法数据结构"""

    technique_schema = {
        'basic_info': {
            'name': str,                    # 技术名称
            'name_chinese': str,            # 中文名称
            'category': str,                # 分类
            'developer': str,               # 创始人
            'year_developed': int,          # 发展年份
            'description': str              # 描述
        },
        'clinical_info': {
            'indications': list,            # 适应症
            'contraindications': list,      # 禁忌症
            'precautions': list,            # 注意事项
            'target_structures': list,      # 目标结构
            'mechanism': str                # 作用机制
        },
        'technique_details': {
            'patient_position': str,        # 患者体位
            'practitioner_position': str,   # 医师位置
            'contact_points': list,         # 接触点
            'line_of_drive': str,           # 推力方向
            'force_parameters': dict,       # 力量参数
            'steps': list                   # 操作步骤
        },
        'media': {
            '3d_animation': str,            # 3D动画链接
            'video_demo': str,              # 视频演示
            'images': list,                 # 图片
            'anatomical_overlay': str       # 解剖叠加图
        },
        'evidence': {
            'research_summary': str,        # 研究摘要
            'effectiveness_rating': str,    # 有效性评级
            'safety_rating': str,           # 安全性评级
            'references': list              # 参考文献
        },
        'tcm_correlation': {
            'related_meridians': list,      # 相关经络
            'related_points': list,         # 相关穴位
            'tcm_indications': list         # 中医适应症
        }
    }
```

### 3.4 常见手法详细信息

```python
diversified_technique = {
    'name': 'Diversified Technique',
    'name_chinese': '多元化技术',
    'category': 'HVLA',
    'description': '最常用的脊椎矫正技术，使用高速低幅推力恢复关节功能',

    'indications': [
        '脊椎半脱位',
        '关节功能障碍',
        '急性腰痛',
        '颈椎病',
        '胸椎功能紊乱'
    ],

    'contraindications': [
        '骨质疏松症（严重）',
        '脊椎肿瘤',
        '脊椎感染',
        '急性骨折',
        '脊髓病变',
        '椎动脉疾病',
        '严重关节不稳'
    ],

    'cervical_adjustment': {
        'patient_position': '仰卧位，头部在调整台边缘',
        'contact': '拇指或食指接触横突或关节突',
        'stabilization': '另一手稳定头部',
        'thrust': '快速、精确、低幅度推力',
        'direction': '根据半脱位方向确定推力线',
        'precautions': [
            '术前进行椎动脉测试',
            '注意患者颈部旋转幅度',
            '避免过度伸展'
        ]
    },

    'thoracic_adjustment': {
        'patient_position': '俯卧位或仰卧交叉手臂',
        'contact': '豆状骨接触横突',
        'thrust': '利用身体重量的下压推力',
        'direction': '前下方向',
        'breathing': '患者呼气末进行调整'
    },

    'lumbar_adjustment': {
        'patient_position': '侧卧位',
        'contact': '豆状骨接触乳突或棘突',
        'stabilization': '稳定骨盆和肩部',
        'thrust': '旋转推力',
        'direction': '根据半脱位类型确定'
    },

    'evidence': {
        'effectiveness': '高',
        'safety': '高（当正确应用时）',
        'research': '大量RCT支持其对急性腰痛的有效性'
    }
}

gonstead_technique = {
    'name': 'Gonstead Technique',
    'name_chinese': '冈斯特德技术',
    'category': 'HVLA',
    'description': '精确的脊椎分析和特定调整系统',

    'analysis_methods': [
        {
            'name': 'Visualization',
            'chinese': '视诊',
            'description': '观察姿势、步态、皮肤变化'
        },
        {
            'name': 'Instrumentation',
            'chinese': '仪器检查',
            'description': '使用Nervoscope检测温度差异'
        },
        {
            'name': 'Static Palpation',
            'chinese': '静态触诊',
            'description': '检查水肿、压痛、肌肉紧张'
        },
        {
            'name': 'Motion Palpation',
            'chinese': '动态触诊',
            'description': '评估关节活动度'
        },
        {
            'name': 'X-ray Analysis',
            'chinese': 'X光分析',
            'description': '确定半脱位位置和方向'
        }
    ],

    'cervical_chair': {
        'description': '使用专用颈椎调整椅',
        'patient_position': '坐位，头部轻度前屈',
        'technique': '精确的拇指推力'
    },

    'knee_chest_table': {
        'description': '使用膝胸位调整台',
        'patient_position': '跪位，胸部靠在垫上',
        'advantages': '减少腰椎前凸，便于调整'
    }
}

activator_method = {
    'name': 'Activator Methods',
    'name_chinese': '激活器方法',
    'category': '仪器辅助低力技术',
    'description': '使用手持机械仪器进行精确、低力调整',

    'instrument': {
        'name': 'Activator Adjusting Instrument',
        'mechanism': '弹簧驱动的脉冲力',
        'force': '0.3J - 较低的力量',
        'speed': '高速（<3毫秒）',
        'advantages': [
            '力量可控',
            '适合敏感患者',
            '可用于所有年龄',
            '无关节腔化声音'
        ]
    },

    'protocol': {
        'leg_length_analysis': '仰卧位腿长分析',
        'isolation_tests': '隔离测试确定调整部位',
        'adjustment_sequence': '从骶骨到颈椎的系统调整',
        'post_check': '调整后重新检查腿长'
    },

    'indications': [
        '老年患者',
        '骨质疏松患者',
        '急性疼痛患者',
        '儿童',
        '对HVLA恐惧的患者',
        '术后患者'
    ],

    'evidence': {
        'research': '多项RCT显示与手法调整效果相当',
        'safety': '极高的安全性记录'
    }
}

cox_flexion_distraction = {
    'name': 'Cox Flexion-Distraction',
    'name_chinese': 'Cox屈曲牵引技术',
    'category': '低力技术',
    'description': '使用专用治疗台进行脊椎减压',

    'mechanism': {
        'primary': '增加椎间隙高度',
        'secondary': [
            '降低椎间盘内压',
            '增加椎管和椎间孔面积',
            '改善椎间盘营养',
            '减少神经根压迫'
        ]
    },

    'indications': [
        '腰椎间盘突出',
        '椎管狭窄',
        '退行性椎间盘疾病',
        '小关节综合征',
        '脊椎滑脱（I-II度）'
    ],

    'contraindications': [
        '马尾综合征',
        '严重骨质疏松',
        '腹主动脉瘤',
        '脊椎肿瘤',
        '感染'
    ],

    'protocol': {
        'position': '俯卧位在专用治疗台',
        'cycles': '每节段3-5个屈曲牵引周期',
        'hold_time': '每个周期保持3-5秒',
        'sessions': '通常需要12-15次治疗'
    },

    'evidence': {
        'effectiveness': '高',
        'research': 'Cox博士的研究显示85%的椎间盘突出患者改善'
    }
}
```

### 3.5 3D演示系统

```python
class ChiropracticVisualization:
    """Chiropractic手法3D可视化"""

    def __init__(self):
        self.model_engine = ThreeJSEngine()
        self.anatomy_models = AnatomyModelLibrary()

    def create_technique_demo(self, technique_id):
        """创建手法3D演示"""
        technique = self.get_technique(technique_id)

        demo = {
            'scene': self.setup_scene(),
            'models': {
                'patient': self.anatomy_models.get_spine_model(),
                'practitioner_hands': self.anatomy_models.get_hand_model(),
                'table': self.get_treatment_table(technique['table_type'])
            },
            'animations': self.create_animations(technique),
            'annotations': self.create_annotations(technique),
            'controls': {
                'play': True,
                'pause': True,
                'step_by_step': True,
                'rotate': True,
                'zoom': True,
                'explode_view': True
            }
        }

        return demo

    def create_animations(self, technique):
        """创建动画序列"""
        animations = []

        for i, step in enumerate(technique['steps']):
            animation = {
                'step_number': i + 1,
                'name': step['name'],
                'duration': step['duration'],
                'keyframes': self.generate_keyframes(step),
                'camera_position': step['camera_angle'],
                'highlights': step['structures_involved'],
                'force_vectors': step.get('force_visualization'),
                'narration': step['description']
            }
            animations.append(animation)

        return animations

    def anatomical_overlay(self, technique):
        """解剖结构叠加"""
        return {
            'bones': {
                'vertebrae': True,
                'specific_level': technique['target_level'],
                'highlight_color': '#FF6B6B'
            },
            'joints': {
                'facet_joints': True,
                'intervertebral_discs': True
            },
            'soft_tissue': {
                'muscles': technique.get('muscles_involved', []),
                'ligaments': technique.get('ligaments_involved', []),
                'nerves': technique.get('nerves_affected', [])
            },
            'contact_points': {
                'show': True,
                'practitioner_contact': technique['contact_points'],
                'stabilization_points': technique['stabilization']
            },
            'force_vectors': {
                'show': True,
                'direction': technique['line_of_drive'],
                'magnitude': technique['force_parameters']
            }
        }
```

### 3.6 Chiropractic与中医结合

```python
class ChiropracticTCMIntegration:
    """Chiropractic与中医整合"""

    def spine_meridian_correlation(self):
        """脊椎节段与经络对应"""
        correlations = {
            'C1_Atlas': {
                'meridians': ['督脉', '膀胱经'],
                'points': ['风府', '哑门', '天柱'],
                'tcm_functions': '通督脉，醒脑开窍',
                'related_symptoms': '头痛、眩晕、失眠'
            },
            'C2_Axis': {
                'meridians': ['督脉', '膀胱经'],
                'points': ['风池', '完骨'],
                'tcm_functions': '疏风清热，明目聪耳',
                'related_symptoms': '颈痛、耳鸣、视力问题'
            },
            'C3-C5': {
                'meridians': ['手太阴肺经', '手阳明大肠经'],
                'points': ['大椎', '肩井', '天髎'],
                'tcm_functions': '宣肺利咽，通经活络',
                'related_symptoms': '咽喉问题、肩颈痛、上肢麻木'
            },
            'C6-C7': {
                'meridians': ['手少阴心经', '手太阳小肠经'],
                'points': ['大椎', '陶道', '身柱'],
                'tcm_functions': '清心安神，舒筋活络',
                'related_symptoms': '心悸、上肢无力、手指麻木'
            },
            'T1-T4': {
                'meridians': ['心经', '心包经', '肺经'],
                'points': ['大杼', '风门', '肺俞', '心俞'],
                'tcm_functions': '宣肺理气，宁心安神',
                'related_symptoms': '胸闷、咳嗽、心悸、气短'
            },
            'T5-T8': {
                'meridians': ['肝经', '胆经', '脾经', '胃经'],
                'points': ['膈俞', '肝俞', '胆俞', '脾俞', '胃俞'],
                'tcm_functions': '疏肝利胆，健脾和胃',
                'related_symptoms': '消化问题、胁痛、胃痛'
            },
            'T9-T12': {
                'meridians': ['脾经', '肾经', '三焦经'],
                'points': ['脾俞', '胃俞', '三焦俞', '肾俞'],
                'tcm_functions': '温补脾肾，利水消肿',
                'related_symptoms': '腰痛、腹胀、泌尿问题'
            },
            'L1-L5': {
                'meridians': ['肾经', '膀胱经'],
                'points': ['肾俞', '气海俞', '大肠俞', '关元俞'],
                'tcm_functions': '补肾壮腰，通经活络',
                'related_symptoms': '腰痛、下肢痛、生殖泌尿问题'
            },
            'Sacrum': {
                'meridians': ['督脉', '任脉', '肾经'],
                'points': ['腰俞', '长强', '八髎'],
                'tcm_functions': '补肾固本，调理下焦',
                'related_symptoms': '腰骶痛、便秘、妇科问题'
            }
        }

        return correlations

    def integrated_treatment_protocol(self, condition, findings):
        """整合治疗方案"""
        protocol = {
            'chiropractic': {
                'adjustment': self.recommend_technique(findings['subluxations']),
                'soft_tissue': self.recommend_soft_tissue_work(findings['muscle_tension']),
                'rehabilitation': self.recommend_exercises(condition)
            },
            'tcm': {
                'acupuncture': self.recommend_acupoints(findings['spine_levels']),
                'tuina': self.recommend_tuina(findings['affected_meridians']),
                'herbal': self.recommend_herbs(condition)
            },
            'combined_rationale': self.explain_synergy(condition),
            'treatment_sequence': self.optimal_sequence(),
            'expected_outcomes': self.predict_outcomes(condition)
        }

        return protocol
```

---

## 4. 统一更新与提醒机制

### 4.1 更新管理系统

```python
class UnifiedUpdateManager:
    """统一更新管理器"""

    def __init__(self):
        self.update_sources = {
            'xray_models': {
                'source': 'medical_ai_registry',
                'check_frequency': 'weekly',
                'auto_update': False  # 需要验证
            },
            'drug_database': {
                'source': 'drugbank_api',
                'check_frequency': 'daily',
                'auto_update': True
            },
            'herb_drug_interactions': {
                'source': 'natural_medicines_db',
                'check_frequency': 'weekly',
                'auto_update': True
            },
            'chiropractic_techniques': {
                'source': 'chiropractic_research_db',
                'check_frequency': 'monthly',
                'auto_update': True
            },
            'malaysia_drug_registry': {
                'source': 'npra_malaysia',
                'check_frequency': 'weekly',
                'auto_update': True
            }
        }

    def check_all_updates(self):
        """检查所有更新"""
        updates_available = []

        for component, config in self.update_sources.items():
            update_info = self.check_component_update(component, config)
            if update_info['has_update']:
                updates_available.append(update_info)

        return updates_available

    def notify_updates(self, updates):
        """发送更新通知"""
        notifications = []

        for update in updates:
            notification = {
                'id': generate_uuid(),
                'type': 'system_update',
                'component': update['component'],
                'priority': update['priority'],
                'title': f"{update['component_name']}有新更新",
                'message': update['description'],
                'version': {
                    'current': update['current_version'],
                    'new': update['new_version']
                },
                'changes': update['changelog'],
                'action_required': not update['auto_update'],
                'timestamp': datetime.now()
            }
            notifications.append(notification)

            # 发送通知
            self.send_notification(notification)

        return notifications
```

### 4.2 更新类型和优先级

```yaml
更新优先级:
  critical:
    description: "紧急安全更新或重大错误修复"
    notification: "立即通知 + 强制更新提醒"
    examples:
      - AI模型安全漏洞
      - 药物相互作用重大错误
      - 严重禁忌症遗漏

  high:
    description: "重要功能更新或数据更新"
    notification: "当日通知 + 更新建议"
    examples:
      - 新药物上市
      - AI模型性能提升
      - 新手法技术添加

  medium:
    description: "常规更新和改进"
    notification: "周报通知"
    examples:
      - 数据库常规更新
      - 界面改进
      - 小功能增强

  low:
    description: "次要更新和优化"
    notification: "月报通知"
    examples:
      - 性能优化
      - 文档更新
      - 界面微调
```

### 4.3 更新通知界面

```python
class UpdateNotificationUI:
    """更新通知界面"""

    def render_notification_center(self, user):
        """渲染通知中心"""
        notifications = self.get_user_notifications(user)

        return {
            'unread_count': len([n for n in notifications if not n['read']]),
            'categories': {
                'system_updates': self.filter_by_type(notifications, 'system_update'),
                'drug_alerts': self.filter_by_type(notifications, 'drug_alert'),
                'safety_notices': self.filter_by_type(notifications, 'safety_notice'),
                'new_content': self.filter_by_type(notifications, 'new_content')
            },
            'priority_alerts': [n for n in notifications if n['priority'] in ['critical', 'high']],
            'actions': {
                'mark_all_read': True,
                'update_all': True,
                'settings': True
            }
        }

    def render_update_detail(self, update):
        """渲染更新详情"""
        return {
            'header': {
                'title': update['title'],
                'component': update['component_name'],
                'priority_badge': update['priority'],
                'date': update['timestamp']
            },
            'version_info': {
                'current': update['current_version'],
                'new': update['new_version'],
                'size': update['download_size']
            },
            'changelog': {
                'new_features': update['changes'].get('features', []),
                'improvements': update['changes'].get('improvements', []),
                'bug_fixes': update['changes'].get('fixes', []),
                'data_updates': update['changes'].get('data', [])
            },
            'impact': {
                'downtime': update['requires_restart'],
                'backup_required': update['backup_recommended'],
                'compatibility': update['compatibility_notes']
            },
            'actions': {
                'update_now': True,
                'schedule_update': True,
                'view_details': True,
                'skip_version': update['priority'] not in ['critical']
            }
        }
```

### 4.4 自动更新配置

```python
class AutoUpdateConfig:
    """自动更新配置"""

    default_settings = {
        'auto_update_enabled': True,
        'update_schedule': {
            'preferred_time': '03:00',  # 凌晨3点
            'preferred_day': 'Sunday',   # 周日
            'timezone': 'Asia/Kuala_Lumpur'
        },
        'component_settings': {
            'xray_models': {
                'auto_update': False,
                'notify': True,
                'require_approval': True
            },
            'drug_database': {
                'auto_update': True,
                'notify': True,
                'require_approval': False
            },
            'chiropractic_db': {
                'auto_update': True,
                'notify': True,
                'require_approval': False
            }
        },
        'notification_preferences': {
            'email': True,
            'in_app': True,
            'sms': False,
            'critical_only_sms': True
        },
        'backup_before_update': True,
        'rollback_enabled': True
    }

    def get_user_settings(self, user_id):
        """获取用户更新设置"""
        user_settings = self.db.get_user_update_settings(user_id)
        return {**self.default_settings, **user_settings}

    def schedule_update(self, component, version, schedule):
        """计划更新"""
        return {
            'job_id': generate_uuid(),
            'component': component,
            'version': version,
            'scheduled_time': schedule['time'],
            'pre_tasks': [
                'backup_current_version',
                'verify_download',
                'check_dependencies'
            ],
            'post_tasks': [
                'verify_installation',
                'run_tests',
                'notify_completion'
            ]
        }
```

---

## 5. 数据库设计

### 5.1 X光分析数据库

```sql
-- X光检查记录
CREATE TABLE xray_examinations (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    exam_date TIMESTAMP NOT NULL,
    exam_type VARCHAR(50) NOT NULL,
    body_part VARCHAR(50) NOT NULL,
    views JSONB,
    image_paths JSONB,
    dicom_metadata JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI分析结果
CREATE TABLE xray_ai_analysis (
    id UUID PRIMARY KEY,
    examination_id UUID REFERENCES xray_examinations(id),
    model_version VARCHAR(50) NOT NULL,
    analysis_timestamp TIMESTAMP NOT NULL,
    findings JSONB NOT NULL,
    abnormalities JSONB,
    measurements JSONB,
    confidence_scores JSONB,
    annotations JSONB,
    tcm_correlations JSONB,
    raw_output JSONB
);

-- X光报告
CREATE TABLE xray_reports (
    id UUID PRIMARY KEY,
    examination_id UUID REFERENCES xray_examinations(id),
    analysis_id UUID REFERENCES xray_ai_analysis(id),
    report_content JSONB NOT NULL,
    impression TEXT,
    recommendations JSONB,
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI模型版本管理
CREATE TABLE xray_ai_models (
    id UUID PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    body_part VARCHAR(50) NOT NULL,
    architecture VARCHAR(100),
    training_data_info JSONB,
    performance_metrics JSONB,
    release_date DATE,
    is_active BOOLEAN DEFAULT false,
    model_path VARCHAR(255),
    checksum VARCHAR(64)
);
```

### 5.2 药物字典数据库

```sql
-- 药物主表
CREATE TABLE drugs (
    id UUID PRIMARY KEY,
    generic_name VARCHAR(255) NOT NULL,
    generic_name_chinese VARCHAR(255),
    brand_names JSONB,
    drug_class VARCHAR(100),
    atc_code VARCHAR(20),
    cas_number VARCHAR(20),
    molecular_formula VARCHAR(100),
    molecular_weight DECIMAL(10,4),
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 药物临床信息
CREATE TABLE drug_clinical_info (
    id UUID PRIMARY KEY,
    drug_id UUID REFERENCES drugs(id),
    indications JSONB,
    contraindications JSONB,
    dosage_forms JSONB,
    routes_of_administration JSONB,
    standard_dosing JSONB,
    pediatric_dosing JSONB,
    renal_dosing JSONB,
    hepatic_dosing JSONB,
    pharmacokinetics JSONB,
    pharmacodynamics TEXT
);

-- 药物安全信息
CREATE TABLE drug_safety (
    id UUID PRIMARY KEY,
    drug_id UUID REFERENCES drugs(id),
    side_effects JSONB,
    warnings JSONB,
    black_box_warning TEXT,
    pregnancy_category VARCHAR(10),
    lactation_info TEXT,
    overdose_info TEXT,
    storage_conditions TEXT
);

-- 药物相互作用
CREATE TABLE drug_interactions (
    id UUID PRIMARY KEY,
    drug1_id UUID REFERENCES drugs(id),
    drug2_id UUID REFERENCES drugs(id),
    interaction_level VARCHAR(20) NOT NULL,
    mechanism TEXT,
    clinical_effect TEXT,
    management TEXT,
    evidence_level VARCHAR(20),
    references JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 中西药相互作用
CREATE TABLE herb_drug_interactions (
    id UUID PRIMARY KEY,
    herb_id UUID REFERENCES herbs(id),
    drug_id UUID REFERENCES drugs(id),
    interaction_level VARCHAR(20) NOT NULL,
    mechanism TEXT,
    clinical_effect TEXT,
    management TEXT,
    evidence_level VARCHAR(20),
    references JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 马来西亚药物注册信息
CREATE TABLE malaysia_drug_registry (
    id UUID PRIMARY KEY,
    drug_id UUID REFERENCES drugs(id),
    registration_number VARCHAR(50) UNIQUE,
    registration_date DATE,
    expiry_date DATE,
    poison_schedule VARCHAR(10),
    controlled_status VARCHAR(20),
    manufacturer VARCHAR(255),
    importer VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active'
);
```

### 5.3 Chiropractic数据库

```sql
-- Chiropractic手法主表
CREATE TABLE chiropractic_techniques (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_chinese VARCHAR(255),
    category VARCHAR(100),
    developer VARCHAR(255),
    year_developed INTEGER,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 手法临床信息
CREATE TABLE technique_clinical_info (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES chiropractic_techniques(id),
    indications JSONB,
    contraindications JSONB,
    precautions JSONB,
    target_structures JSONB,
    mechanism TEXT
);

-- 手法技术细节
CREATE TABLE technique_details (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES chiropractic_techniques(id),
    spine_region VARCHAR(50),
    patient_position TEXT,
    practitioner_position TEXT,
    contact_points JSONB,
    line_of_drive TEXT,
    force_parameters JSONB,
    steps JSONB,
    tips TEXT
);

-- 手法媒体资源
CREATE TABLE technique_media (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES chiropractic_techniques(id),
    media_type VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    file_path VARCHAR(255),
    thumbnail_path VARCHAR(255),
    duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 手法循证依据
CREATE TABLE technique_evidence (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES chiropractic_techniques(id),
    research_summary TEXT,
    effectiveness_rating VARCHAR(20),
    safety_rating VARCHAR(20),
    conditions_studied JSONB,
    references JSONB
);

-- Chiropractic与中医关联
CREATE TABLE technique_tcm_correlation (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES chiropractic_techniques(id),
    spine_level VARCHAR(20),
    related_meridians JSONB,
    related_points JSONB,
    tcm_indications JSONB,
    tcm_functions TEXT
);

-- 治疗记录
CREATE TABLE chiropractic_treatments (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    visit_id UUID REFERENCES visits(id),
    technique_id UUID REFERENCES chiropractic_techniques(id),
    spine_levels JSONB,
    findings_before JSONB,
    adjustments_performed JSONB,
    findings_after JSONB,
    patient_response TEXT,
    practitioner_id UUID REFERENCES users(id),
    treatment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.4 更新管理数据库

```sql
-- 系统组件版本
CREATE TABLE system_components (
    id UUID PRIMARY KEY,
    component_name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    current_version VARCHAR(50),
    last_updated TIMESTAMP,
    update_source VARCHAR(255),
    check_frequency VARCHAR(20),
    auto_update BOOLEAN DEFAULT false
);

-- 可用更新
CREATE TABLE available_updates (
    id UUID PRIMARY KEY,
    component_id UUID REFERENCES system_components(id),
    new_version VARCHAR(50) NOT NULL,
    release_date TIMESTAMP,
    priority VARCHAR(20),
    changelog JSONB,
    download_url VARCHAR(255),
    download_size BIGINT,
    checksum VARCHAR(64),
    is_installed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 更新历史
CREATE TABLE update_history (
    id UUID PRIMARY KEY,
    component_id UUID REFERENCES system_components(id),
    from_version VARCHAR(50),
    to_version VARCHAR(50),
    update_type VARCHAR(20),
    status VARCHAR(20),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    performed_by UUID REFERENCES users(id),
    notes TEXT
);

-- 用户更新设置
CREATE TABLE user_update_preferences (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    settings JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 更新通知
CREATE TABLE update_notifications (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    update_id UUID REFERENCES available_updates(id),
    notification_type VARCHAR(50),
    priority VARCHAR(20),
    title VARCHAR(255),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. API接口设计

### 6.1 X光分析API

```yaml
X光分析API:

  上传分析:
    POST /api/xray/analyze:
      description: "上传X光片并进行AI分析"
      request:
        multipart/form-data:
          image: file (required)
          patient_id: uuid (required)
          body_part: string (required)
          exam_type: string (required)
          views: array
      response:
        examination_id: uuid
        analysis_id: uuid
        findings: array
        abnormalities: array
        measurements: object
        confidence: number
        annotations: array

  获取报告:
    GET /api/xray/reports/{examination_id}:
      description: "获取X光分析报告"
      response:
        report: object

  批量分析:
    POST /api/xray/batch-analyze:
      description: "批量上传分析"
      request:
        images: array of files
        patient_id: uuid
        exam_type: string

  对比分析:
    POST /api/xray/compare:
      description: "对比多次检查结果"
      request:
        examination_ids: array of uuid
      response:
        comparison: object
        changes: array
        trends: object
```

### 6.2 药物字典API

```yaml
药物字典API:

  搜索药物:
    GET /api/drugs/search:
      parameters:
        q: string (query)
        class: string
        indication: string
        page: integer
        limit: integer
      response:
        drugs: array
        total: integer

  获取药物详情:
    GET /api/drugs/{drug_id}:
      response:
        drug: object
        clinical_info: object
        safety_info: object
        interactions: array

  检查相互作用:
    POST /api/drugs/interactions/check:
      request:
        drugs: array of drug_ids
        herbs: array of herb_ids
      response:
        interactions: array
        severity: string
        recommendations: array

  剂量计算:
    POST /api/drugs/dosing/calculate:
      request:
        drug_id: uuid
        patient: object (weight, age, renal_function, etc.)
      response:
        recommended_dose: number
        adjustments: array
        monitoring: array

  AI药物推荐:
    POST /api/drugs/recommend:
      request:
        diagnosis: string
        patient_profile: object
        current_medications: array
        current_herbs: array
      response:
        recommendations: array
```

### 6.3 Chiropractic API

```yaml
Chiropractic API:

  获取手法列表:
    GET /api/chiropractic/techniques:
      parameters:
        category: string
        indication: string
        spine_region: string
      response:
        techniques: array

  获取手法详情:
    GET /api/chiropractic/techniques/{id}:
      response:
        technique: object
        clinical_info: object
        details: object
        media: array
        evidence: object
        tcm_correlation: object

  获取3D演示:
    GET /api/chiropractic/techniques/{id}/3d-demo:
      response:
        scene_config: object
        animations: array
        annotations: array

  记录治疗:
    POST /api/chiropractic/treatments:
      request:
        patient_id: uuid
        visit_id: uuid
        technique_id: uuid
        spine_levels: array
        findings: object
        adjustments: object
      response:
        treatment_id: uuid

  获取整合方案:
    POST /api/chiropractic/integrated-protocol:
      request:
        condition: string
        findings: object
      response:
        chiropractic: object
        tcm: object
        combined_rationale: string
```

### 6.4 更新管理API

```yaml
更新管理API:

  检查更新:
    GET /api/updates/check:
      response:
        updates_available: array
        last_checked: timestamp

  获取更新详情:
    GET /api/updates/{update_id}:
      response:
        update: object
        changelog: object

  安装更新:
    POST /api/updates/{update_id}/install:
      response:
        job_id: uuid
        status: string

  获取更新状态:
    GET /api/updates/jobs/{job_id}/status:
      response:
        status: string
        progress: number

  获取用户通知:
    GET /api/updates/notifications:
      response:
        notifications: array
        unread_count: integer

  更新设置:
    PUT /api/updates/settings:
      request:
        settings: object
      response:
        success: boolean
```

---

## 7. 界面设计

### 7.1 X光分析界面

```
┌─────────────────────────────────────────────────────────────────┐
│  X光AI分析系统                                    [通知] [设置]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────┐  ┌────────────────────────┐    │
│  │                             │  │  分析结果              │    │
│  │                             │  ├────────────────────────┤    │
│  │      [X光图像显示区]        │  │  ⚠ 发现 3 项异常       │    │
│  │                             │  │                        │    │
│  │    [标注和测量叠加]         │  │  1. L4-L5椎间隙狭窄    │    │
│  │                             │  │     置信度: 94%        │    │
│  │                             │  │                        │    │
│  │  [对比度] [亮度] [缩放]     │  │  2. L5椎体骨赘形成    │    │
│  └─────────────────────────────┘  │     置信度: 89%        │    │
│                                   │                        │    │
│  [上一张] [下一张] [对比模式]     │  3. 轻度腰椎前凸减少  │    │
│                                   │     置信度: 85%        │    │
│  ┌─────────────────────────────┐  └────────────────────────┘    │
│  │  测量数据                   │                                │
│  │  ─────────────────────────  │  ┌────────────────────────┐    │
│  │  腰椎前凸角: 35°            │  │  中医关联              │    │
│  │  L4-L5间隙: 4.2mm          │  ├────────────────────────┤    │
│  │  L5-S1间隙: 5.8mm          │  │  相关经络: 肾经、膀胱经│    │
│  │  椎体排列: 轻度后移         │  │  建议穴位:             │    │
│  └─────────────────────────────┘  │  • 肾俞 • 大肠俞       │    │
│                                   │  • 委中 • 承山         │    │
│  [生成报告] [导出DICOM] [分享]    └────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 药物字典界面

```
┌─────────────────────────────────────────────────────────────────┐
│  现代药物AI字典                                  [通知] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🔍 搜索药物 (输入药名、适应症或ATC码)               │    │
│  │  [Metformin                                        ] 🎤  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [按分类浏览] [相互作用检查] [剂量计算] [AI推荐]                │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Metformin (二甲双胍)                                   │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │                                                         │    │
│  │  基本信息 | 临床应用 | 剂量 | 相互作用 | 安全性          │    │
│  │  ═════════════════════════════════════════════════════  │    │
│  │                                                         │    │
│  │  药物分类: 双胍类降糖药                                 │    │
│  │  ATC码: A10BA02                                         │    │
│  │  商品名: Glucophage, Fortamet, Glumetza                 │    │
│  │                                                         │    │
│  │  适应症:                                                │    │
│  │  • 2型糖尿病                                            │    │
│  │  • 多囊卵巢综合征                                       │    │
│  │  • 糖尿病预防                                           │    │
│  │                                                         │    │
│  │  ⚠ 中药相互作用:                                       │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ 黄芪 - 中度相互作用                             │    │    │
│  │  │ 可能增强降糖作用，监测血糖                      │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │                                                         │    │
│  │  马来西亚注册: MAL19XXXXXX | 毒药分类: Group B          │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [添加到处方] [打印信息] [患者教育单张]                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Chiropractic手法界面

```
┌─────────────────────────────────────────────────────────────────┐
│  Chiropractic手法数据库                          [通知] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [HVLA技术] [低力技术] [软组织] [仪器辅助] [按适应症] [按部位]  │
│                                                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │  Cox Flexion-Distraction │  │                              │  │
│  │  Cox屈曲牵引技术         │  │    [3D动画演示区]            │  │
│  ├─────────────────────────┤  │                              │  │
│  │                         │  │  ▶ [播放] [暂停] [步骤]      │  │
│  │  分类: 低力技术          │  │                              │  │
│  │  目标: 腰椎减压          │  │  [旋转] [缩放] [解剖叠加]    │  │
│  │                         │  │                              │  │
│  │  适应症:                 │  └──────────────────────────────┘  │
│  │  ✓ 腰椎间盘突出         │                                    │
│  │  ✓ 椎管狭窄             │  ┌──────────────────────────────┐  │
│  │  ✓ 退行性椎间盘病       │  │  操作步骤                    │  │
│  │  ✓ 小关节综合征         │  ├──────────────────────────────┤  │
│  │                         │  │  1. 患者俯卧位               │  │
│  │  禁忌症:                 │  │  2. 确定目标节段             │  │
│  │  ✗ 马尾综合征           │  │  3. 接触棘突                 │  │
│  │  ✗ 严重骨质疏松         │  │  4. 缓慢屈曲牵引             │  │
│  │  ✗ 脊椎肿瘤             │  │  5. 保持3-5秒                │  │
│  │                         │  │  6. 重复3-5个周期            │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  中医关联                                               │    │
│  │  ─────────────────────────────────────────────────────  │    │
│  │  相关经络: 督脉、膀胱经、肾经                           │    │
│  │  配合穴位: 肾俞、大肠俞、委中、承山、昆仑               │    │
│  │  配合推拿: 滚法腰背部、㨰法肾俞、点按委中               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [查看研究证据] [记录治疗] [打印指导]                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.4 更新通知中心

```
┌─────────────────────────────────────────────────────────────────┐
│  更新与通知中心                                  [全部标记已读]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  待处理更新: 3    新通知: 5    上次检查: 今天 08:00             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🔴 紧急更新                                            │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │                                                         │    │
│  │  药物相互作用数据库更新                                 │    │
│  │  版本: 2024.01.15 → 2024.01.20                          │    │
│  │  优先级: 高                                             │    │
│  │                                                         │    │
│  │  更新内容:                                              │    │
│  │  • 新增 45 条中西药相互作用                             │    │
│  │  • 修正 3 条严重相互作用分级                            │    │
│  │  • 更新马来西亚新注册药物                               │    │
│  │                                                         │    │
│  │  [立即更新] [计划更新] [查看详情]                       │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🟡 常规更新                                            │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │                                                         │    │
│  │  Chiropractic手法数据库                                 │    │
│  │  版本: 2.3.0 → 2.4.0                                    │    │
│  │  • 新增 5 种手法技术                                    │    │
│  │  • 更新 3D动画                                          │    │
│  │                                                         │    │
│  │  X光AI模型更新                                          │    │
│  │  版本: 1.5.0 → 1.6.0                                    │    │
│  │  • 脊椎分析准确率提升 3%                                │    │
│  │  • 新增骨密度评估功能                                   │    │
│  │                                                         │    │
│  │  [全部更新] [选择更新]                                  │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  更新设置                                               │    │
│  │  ─────────────────────────────────────────────────────  │    │
│  │  [✓] 启用自动更新                                       │    │
│  │  [✓] 更新前备份                                         │    │
│  │  [✓] 邮件通知                                           │    │
│  │  [ ] 仅紧急更新发送短信                                 │    │
│  │  首选更新时间: [03:00] 首选日期: [周日]                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 安全与合规

### 8.1 医学AI免责声明

```yaml
AI辅助诊断免责:
  - X光AI分析仅供参考，不能替代放射科医师诊断
  - 药物推荐需经执业医师确认
  - Chiropractic手法需由持证从业者执行
  - 所有AI建议应结合临床判断

数据安全:
  - 所有医学影像加密存储
  - 符合PDPA 2010数据保护要求
  - 审计日志记录所有访问
  - 定期安全评估
```

### 8.2 更新安全机制

```yaml
更新验证:
  - 数字签名验证
  - 校验和验证
  - 沙盒测试
  - 回滚机制

质量控制:
  - AI模型更新需通过验证测试
  - 药物数据更新需多源验证
  - 重大更新需管理员批准
```

---

## 9. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2024 | 初始版本 - AI X光分析、药物字典、Chiropractic手法数据库 |

---

**文档结束**
