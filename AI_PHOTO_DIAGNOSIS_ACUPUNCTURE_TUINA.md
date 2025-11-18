# 现场拍照AI诊断、针灸穴位与推拿手法系统技术规格

## 文档信息
- **版本**: 1.0
- **创建日期**: 2024年
- **适用范围**: 马来西亚中医诊所系统
- **合规标准**: Malaysia T&CM Act 2016, PDPA 2010

---

## 目录
1. [现场拍照AI诊断系统](#1-现场拍照ai诊断系统)
2. [AI针灸穴位智能系统](#2-ai针灸穴位智能系统)
3. [推拿手法数据库系统](#3-推拿手法数据库系统)
4. [统一更新机制](#4-统一更新机制)
5. [数据库设计](#5-数据库设计)
6. [API接口设计](#6-api接口设计)
7. [界面设计](#7-界面设计)

---

## 1. 现场拍照AI诊断系统

### 1.1 系统概述

实时拍照AI诊断系统，支持随时拍摄患者症状照片，通过AI进行智能分析和辅助诊断。

### 1.2 核心功能

#### 1.2.1 多平台拍照支持

```yaml
支持设备:
  移动端:
    - iOS (iPhone/iPad)
    - Android (手机/平板)
    - 支持前后摄像头

  桌面端:
    - USB摄像头
    - 内置摄像头
    - 专业医学摄像设备

  专业设备:
    - 皮肤镜
    - 舌诊仪
    - 口腔内窥镜
    - 耳镜

图像要求:
  分辨率: 最低 1920x1080
  格式: JPEG, PNG, HEIC
  大小: 最大 20MB
  色彩: sRGB色彩空间
```

#### 1.2.2 拍照引导系统

```python
class PhotoGuidanceSystem:
    """拍照引导系统"""

    def __init__(self):
        self.guides = self.load_photo_guides()

    def get_guidance(self, symptom_type):
        """获取拍照指导"""
        guides = {
            'tongue': {
                'name': '舌象拍摄',
                'instructions': [
                    '自然光线下拍摄',
                    '舌头自然伸出，不要过度用力',
                    '保持舌面平整',
                    '避免进食或刷舌后立即拍摄',
                    '包含整个舌体'
                ],
                'overlay': 'tongue_outline.png',
                'example': 'tongue_example.jpg',
                'common_errors': [
                    '光线不足',
                    '舌头伸出过度',
                    '只拍摄舌尖'
                ]
            },
            'face': {
                'name': '面部望诊',
                'instructions': [
                    '正面自然光',
                    '不要化妆',
                    '放松面部表情',
                    '包含整个面部'
                ],
                'overlay': 'face_outline.png',
                'zones': ['额头', '眼周', '鼻部', '颧部', '口唇', '下颌']
            },
            'skin': {
                'name': '皮肤症状',
                'instructions': [
                    '近距离拍摄病灶',
                    '包含周围正常皮肤对比',
                    '使用标尺参照',
                    '多角度拍摄'
                ],
                'scale_reference': True,
                'multiple_angles': True
            },
            'nail': {
                'name': '指甲望诊',
                'instructions': [
                    '清洁指甲',
                    '去除指甲油',
                    '自然光线',
                    '拍摄所有手指'
                ],
                'overlay': 'nail_outline.png'
            },
            'eye': {
                'name': '目诊',
                'instructions': [
                    '睁大眼睛',
                    '向上看露出下眼睑',
                    '避免闪光灯直射',
                    '拍摄双眼'
                ]
            },
            'wound': {
                'name': '伤口/肿胀',
                'instructions': [
                    '清洁伤口周围',
                    '包含标尺',
                    '拍摄不同角度',
                    '记录时间进展'
                ],
                'scale_reference': True,
                'time_series': True
            }
        }

        return guides.get(symptom_type, self.default_guide())

    def realtime_feedback(self, camera_feed, symptom_type):
        """实时拍摄反馈"""
        guide = self.get_guidance(symptom_type)

        feedback = {
            'framing': self.check_framing(camera_feed, guide),
            'lighting': self.check_lighting(camera_feed),
            'focus': self.check_focus(camera_feed),
            'stability': self.check_stability(camera_feed),
            'overlay_alignment': self.check_overlay(camera_feed, guide)
        }

        return {
            'ready_to_capture': all(f['ok'] for f in feedback.values()),
            'feedback': feedback,
            'suggestions': self.generate_suggestions(feedback)
        }
```

#### 1.2.3 AI图像分析引擎

```python
class MedicalImageAnalysisEngine:
    """医学图像AI分析引擎"""

    def __init__(self):
        self.models = {
            'tongue': TongueDiagnosisModel(),
            'face': FaceDiagnosisModel(),
            'skin': SkinAnalysisModel(),
            'nail': NailDiagnosisModel(),
            'eye': EyeDiagnosisModel(),
            'general': GeneralSymptomModel()
        }

    def analyze(self, image, analysis_type, patient_context=None):
        """分析症状图像"""
        # 图像预处理
        processed = self.preprocess(image, analysis_type)

        # 选择模型
        model = self.models.get(analysis_type, self.models['general'])

        # AI分析
        results = model.predict(processed)

        # 结合患者背景
        if patient_context:
            results = self.contextualize(results, patient_context)

        return {
            'findings': results['findings'],
            'tcm_diagnosis': results['tcm_diagnosis'],
            'western_correlation': results['western_correlation'],
            'confidence': results['confidence'],
            'annotations': results['annotations'],
            'recommendations': results['recommendations']
        }

class TongueDiagnosisModel:
    """舌诊AI模型"""

    def predict(self, image):
        """舌象分析"""
        results = {
            'findings': [],
            'tcm_diagnosis': {},
            'western_correlation': [],
            'confidence': 0.0,
            'annotations': [],
            'recommendations': []
        }

        # 1. 舌体分析
        tongue_body = self.analyze_tongue_body(image)
        results['findings'].append({
            'category': '舌体',
            'color': tongue_body['color'],  # 淡红、淡白、红、绛、紫
            'shape': tongue_body['shape'],  # 胖大、瘦薄、齿痕、裂纹
            'texture': tongue_body['texture'],
            'tcm_meaning': self.interpret_body(tongue_body)
        })

        # 2. 舌苔分析
        tongue_coating = self.analyze_coating(image)
        results['findings'].append({
            'category': '舌苔',
            'color': tongue_coating['color'],  # 白、黄、灰、黑
            'thickness': tongue_coating['thickness'],  # 薄、厚
            'moisture': tongue_coating['moisture'],  # 润、燥、滑、腻
            'distribution': tongue_coating['distribution'],
            'tcm_meaning': self.interpret_coating(tongue_coating)
        })

        # 3. 舌下络脉
        sublingual = self.analyze_sublingual(image)
        results['findings'].append({
            'category': '舌下络脉',
            'color': sublingual['color'],
            'distension': sublingual['distension'],
            'tcm_meaning': self.interpret_sublingual(sublingual)
        })

        # 4. 综合辨证
        results['tcm_diagnosis'] = self.synthesize_diagnosis(
            tongue_body, tongue_coating, sublingual
        )

        # 5. 西医关联
        results['western_correlation'] = self.western_correlations(results['findings'])

        return results

    def synthesize_diagnosis(self, body, coating, sublingual):
        """综合舌象辨证"""
        diagnosis = {
            'primary_pattern': '',
            'secondary_patterns': [],
            'pathogenic_factors': [],
            'organ_involvement': [],
            'treatment_principle': ''
        }

        # 舌象辨证规则
        if body['color'] == '淡白' and coating['color'] == '白':
            diagnosis['primary_pattern'] = '阳虚'
            diagnosis['pathogenic_factors'].append('寒')
            diagnosis['organ_involvement'].extend(['脾', '肾'])

        elif body['color'] == '红' and coating['color'] == '黄':
            diagnosis['primary_pattern'] = '实热'
            diagnosis['pathogenic_factors'].append('热')

        elif body['color'] == '紫' or sublingual['distension'] == '怒张':
            diagnosis['primary_pattern'] = '血瘀'
            diagnosis['pathogenic_factors'].append('瘀')

        # ... 更多辨证规则

        return diagnosis

class SkinAnalysisModel:
    """皮肤症状AI模型"""

    def predict(self, image):
        """皮肤症状分析"""
        results = {
            'findings': [],
            'tcm_diagnosis': {},
            'western_correlation': [],
            'confidence': 0.0,
            'annotations': [],
            'recommendations': []
        }

        # 1. 病灶检测
        lesions = self.detect_lesions(image)
        for lesion in lesions:
            results['findings'].append({
                'type': lesion['type'],  # 斑、丘疹、水疱、脓疱、结节等
                'location': lesion['location'],
                'size': lesion['size'],
                'color': lesion['color'],
                'shape': lesion['shape'],
                'border': lesion['border'],
                'distribution': lesion['distribution']
            })

        # 2. 可能诊断
        possible_conditions = self.classify_conditions(lesions)
        results['western_correlation'] = possible_conditions

        # 3. 中医辨证
        results['tcm_diagnosis'] = self.tcm_skin_diagnosis(lesions)

        # 4. 标注
        results['annotations'] = self.generate_annotations(image, lesions)

        return results

    def detectable_conditions(self):
        """可检测的皮肤病变"""
        return {
            '常见皮肤病': [
                '湿疹', '荨麻疹', '银屑病', '痤疮',
                '带状疱疹', '真菌感染', '接触性皮炎'
            ],
            '色素病变': [
                '色素痣', '白癜风', '黄褐斑', '雀斑'
            ],
            '肿瘤筛查': [
                '基底细胞癌', '鳞状细胞癌', '黑色素瘤'
            ],
            '中医皮肤病': [
                '风热证', '血热证', '湿热证', '血虚风燥'
            ]
        }
```

#### 1.2.4 面部望诊分析

```python
class FaceDiagnosisModel:
    """面部望诊AI模型"""

    def predict(self, image):
        """面部望诊分析"""
        results = {
            'findings': [],
            'tcm_diagnosis': {},
            'western_correlation': [],
            'confidence': 0.0
        }

        # 面部分区分析
        face_zones = {
            'forehead': '心肺',
            'nose': '脾胃',
            'left_cheek': '肝',
            'right_cheek': '肺',
            'chin': '肾',
            'around_mouth': '脾胃',
            'around_eyes': '肝肾'
        }

        for zone, organ in face_zones.items():
            zone_analysis = self.analyze_zone(image, zone)
            results['findings'].append({
                'zone': zone,
                'related_organ': organ,
                'color': zone_analysis['color'],
                'texture': zone_analysis['texture'],
                'abnormalities': zone_analysis['abnormalities'],
                'tcm_interpretation': self.interpret_zone(zone_analysis, organ)
            })

        # 整体面色
        overall_complexion = self.analyze_complexion(image)
        results['findings'].append({
            'category': '整体面色',
            'color': overall_complexion['dominant_color'],
            'luster': overall_complexion['luster'],
            'tcm_meaning': self.interpret_complexion(overall_complexion)
        })

        # 五色主病
        color_diagnosis = {
            '青': '肝病、寒证、痛证、瘀血',
            '赤': '热证、心火',
            '黄': '脾虚、湿证',
            '白': '虚证、寒证、失血',
            '黑': '肾虚、寒证、瘀血、水饮'
        }

        return results
```

### 1.3 实时拍照界面

```python
class RealtimeCaptureUI:
    """实时拍照界面"""

    def render_capture_screen(self, symptom_type):
        """渲染拍照界面"""
        guide = self.get_guidance(symptom_type)

        return {
            'camera_view': {
                'overlay': guide['overlay'],
                'grid_lines': True,
                'level_indicator': True
            },
            'realtime_feedback': {
                'lighting_indicator': True,
                'focus_indicator': True,
                'framing_guide': True
            },
            'controls': {
                'capture_button': True,
                'flash_toggle': True,
                'camera_switch': True,
                'zoom_control': True,
                'gallery_access': True
            },
            'guidance_panel': {
                'instructions': guide['instructions'],
                'example_image': guide.get('example'),
                'tips': guide.get('tips', [])
            },
            'quick_actions': {
                'retake': True,
                'adjust': True,
                'analyze': True
            }
        }

    def post_capture_review(self, image):
        """拍摄后预览"""
        quality_check = self.check_image_quality(image)

        return {
            'image_preview': image,
            'quality_assessment': quality_check,
            'actions': {
                'accept': quality_check['acceptable'],
                'retake': True,
                'adjust': True,
                'crop': True,
                'annotate': True
            },
            'warnings': quality_check.get('warnings', [])
        }
```

### 1.4 症状时间线追踪

```python
class SymptomTimelineTracker:
    """症状时间线追踪"""

    def create_timeline(self, patient_id, symptom_type):
        """创建症状时间线"""
        photos = self.get_patient_photos(patient_id, symptom_type)

        timeline = []
        for photo in photos:
            timeline.append({
                'date': photo['captured_at'],
                'image': photo['image_path'],
                'analysis': photo['ai_analysis'],
                'notes': photo['practitioner_notes'],
                'treatment': photo.get('treatment_given')
            })

        return {
            'timeline': timeline,
            'progression': self.analyze_progression(timeline),
            'comparison_view': self.generate_comparison(timeline)
        }

    def analyze_progression(self, timeline):
        """分析病情进展"""
        if len(timeline) < 2:
            return None

        progression = {
            'trend': '',  # improving, stable, worsening
            'changes': [],
            'key_observations': []
        }

        # 对比首次和最近一次
        first = timeline[0]['analysis']
        latest = timeline[-1]['analysis']

        # 分析变化
        changes = self.compare_analyses(first, latest)
        progression['changes'] = changes
        progression['trend'] = self.determine_trend(changes)

        return progression

    def generate_comparison(self, timeline):
        """生成对比视图"""
        if len(timeline) < 2:
            return None

        return {
            'side_by_side': {
                'first': timeline[0],
                'latest': timeline[-1]
            },
            'slider_comparison': True,
            'overlay_comparison': True,
            'animated_progression': len(timeline) > 2
        }
```

### 1.5 离线支持

```python
class OfflinePhotoCapture:
    """离线拍照支持"""

    def __init__(self):
        self.local_storage = LocalImageStorage()
        self.sync_manager = SyncManager()

    def capture_offline(self, image, metadata):
        """离线拍摄"""
        # 本地保存
        local_id = self.local_storage.save({
            'image': image,
            'metadata': metadata,
            'captured_at': datetime.now(),
            'synced': False
        })

        # 基本本地分析（轻量级模型）
        local_analysis = self.local_basic_analysis(image)

        return {
            'local_id': local_id,
            'basic_analysis': local_analysis,
            'pending_sync': True,
            'message': '图片已保存，连接网络后将进行完整AI分析'
        }

    def sync_pending(self):
        """同步待上传图片"""
        pending = self.local_storage.get_pending()

        for item in pending:
            try:
                # 上传到服务器
                result = self.upload_and_analyze(item)

                # 更新本地记录
                self.local_storage.mark_synced(item['local_id'], result)

            except NetworkError:
                continue

        return self.local_storage.get_sync_status()
```

---

## 2. AI针灸穴位智能系统

### 2.1 系统概述

智能针灸穴位推荐和定位系统，结合AI图像识别和3D可视化技术。

### 2.2 穴位数据库

```python
class AcupointDatabase:
    """穴位数据库"""

    acupoint_schema = {
        'basic_info': {
            'code': str,                    # 国际代码 (如 LI4)
            'chinese_name': str,            # 中文名 (合谷)
            'pinyin': str,                  # 拼音 (Hegu)
            'english_name': str,            # 英文名
            'meridian': str,                # 所属经络
            'point_number': int,            # 经穴序号
            'point_type': list              # 穴位类型 (原穴、络穴、郄穴等)
        },
        'location': {
            'anatomical_location': str,     # 解剖位置
            'location_method': str,         # 定位方法
            'cun_measurement': str,         # 骨度分寸
            'simple_location': str,         # 简便取穴
            'depth': str,                   # 针刺深度
            'angle': str,                   # 针刺角度
            'coordinates_3d': dict          # 3D坐标
        },
        'clinical': {
            'indications': list,            # 主治
            'functions': list,              # 功效
            'combinations': list,           # 配伍穴位
            'contraindications': list,      # 禁忌
            'cautions': list                # 注意事项
        },
        'technique': {
            'needling_sensation': str,      # 针感
            'manipulation': list,           # 手法
            'moxibustion': dict,            # 艾灸
            'cupping': dict,                # 拔罐
            'acupressure': dict             # 指压
        },
        'media': {
            'images': list,                 # 图片
            '3d_model': str,                # 3D模型
            'video': str,                   # 视频
            'ar_marker': str                # AR标记
        },
        'research': {
            'modern_research': list,        # 现代研究
            'mechanisms': list,             # 作用机制
            'evidence_level': str           # 证据等级
        }
    }
```

### 2.3 AI穴位推荐引擎

```python
class AcupointRecommendationEngine:
    """AI穴位推荐引擎"""

    def __init__(self):
        self.knowledge_base = AcupointKnowledgeBase()
        self.ml_model = AcupointMLModel()

    def recommend_points(self, diagnosis, symptoms, patient_profile):
        """智能推荐穴位"""
        recommendations = {
            'primary_points': [],      # 主穴
            'secondary_points': [],    # 配穴
            'local_points': [],        # 局部取穴
            'distal_points': [],       # 远端取穴
            'combination_rationale': ''
        }

        # 1. 基于辨证选穴
        pattern_points = self.select_by_pattern(diagnosis['pattern'])

        # 2. 基于症状选穴
        symptom_points = self.select_by_symptoms(symptoms)

        # 3. 基于经络选穴
        meridian_points = self.select_by_meridian(diagnosis['affected_meridians'])

        # 4. 特定穴应用
        special_points = self.select_special_points(diagnosis)

        # 5. AI优化组合
        optimized = self.ml_model.optimize_combination(
            pattern_points,
            symptom_points,
            meridian_points,
            special_points,
            patient_profile
        )

        recommendations['primary_points'] = optimized['primary']
        recommendations['secondary_points'] = optimized['secondary']
        recommendations['combination_rationale'] = self.generate_rationale(optimized)

        return recommendations

    def select_special_points(self, diagnosis):
        """选择特定穴"""
        special_points = []

        # 五输穴应用
        if '实证' in diagnosis['pattern']:
            special_points.append({
                'type': '井穴',
                'indication': '清热开窍',
                'points': self.get_jing_points(diagnosis['affected_meridians'])
            })

        # 八会穴应用
        hui_points = {
            '脏': '章门',
            '腑': '中脘',
            '气': '膻中',
            '血': '膈俞',
            '筋': '阳陵泉',
            '脉': '太渊',
            '骨': '大杼',
            '髓': '绝骨'
        }

        for tissue, point in hui_points.items():
            if tissue in diagnosis.get('affected_tissues', []):
                special_points.append({
                    'type': '八会穴',
                    'point': point,
                    'indication': f'{tissue}病'
                })

        # 原穴、络穴应用
        if '表里同病' in diagnosis.get('patterns', []):
            special_points.extend(self.get_yuan_luo_pairs(diagnosis))

        return special_points

    def generate_rationale(self, recommendation):
        """生成配穴理由"""
        rationale = []

        for point in recommendation['primary']:
            rationale.append(f"{point['name']}: {point['selection_reason']}")

        rationale.append(f"\n配伍原则: {recommendation['combination_principle']}")

        return '\n'.join(rationale)
```

### 2.4 AR穴位定位

```python
class ARPointLocator:
    """AR穴位定位系统"""

    def __init__(self):
        self.body_detector = BodyPartDetector()
        self.point_mapper = AcupointMapper()

    def locate_point_ar(self, camera_feed, point_code):
        """AR实时穴位定位"""
        # 检测身体部位
        body_parts = self.body_detector.detect(camera_feed)

        # 获取穴位信息
        point_info = self.get_point_info(point_code)

        # 计算穴位位置
        point_location = self.point_mapper.calculate_position(
            body_parts,
            point_info['location']
        )

        return {
            'point_code': point_code,
            'point_name': point_info['chinese_name'],
            'screen_position': point_location['screen_coords'],
            'confidence': point_location['confidence'],
            'overlay': {
                'marker': self.create_point_marker(point_info),
                'label': point_info['chinese_name'],
                'depth_indicator': point_info['depth'],
                'angle_indicator': point_info['angle']
            },
            'guidance': {
                'verbal': f"定位{point_info['chinese_name']}：{point_info['simple_location']}",
                'measurement': point_info['cun_measurement']
            }
        }

    def multi_point_ar(self, camera_feed, point_codes):
        """多穴位AR显示"""
        results = []

        for code in point_codes:
            result = self.locate_point_ar(camera_feed, code)
            results.append(result)

        # 显示穴位连线（如经络走向）
        if len(results) > 1:
            connections = self.calculate_connections(results)

        return {
            'points': results,
            'connections': connections,
            'meridian_path': self.show_meridian_path(point_codes)
        }

    def cun_measurement_guide(self, camera_feed, body_part):
        """骨度分寸测量指导"""
        # 检测体表标志
        landmarks = self.detect_landmarks(camera_feed, body_part)

        # 计算分寸
        measurements = self.calculate_cun(landmarks, body_part)

        return {
            'landmarks': landmarks,
            'measurements': measurements,
            'overlay': self.create_measurement_overlay(measurements)
        }
```

### 2.5 3D穴位可视化

```python
class Acupoint3DVisualization:
    """3D穴位可视化"""

    def __init__(self):
        self.model_engine = ThreeJSEngine()
        self.anatomy_models = AnatomyModelLibrary()

    def render_point_3d(self, point_code):
        """3D渲染穴位"""
        point_info = self.get_point_info(point_code)

        scene = {
            'model': self.get_body_region_model(point_info['region']),
            'point_marker': {
                'position': point_info['coordinates_3d'],
                'color': self.get_meridian_color(point_info['meridian']),
                'size': 'medium',
                'pulse_animation': True
            },
            'anatomical_layers': {
                'skin': True,
                'muscle': True,
                'nerve': True,
                'vessel': True,
                'bone': True
            },
            'needle_simulation': {
                'depth': point_info['depth'],
                'angle': point_info['angle'],
                'path': self.calculate_needle_path(point_info)
            },
            'related_structures': self.get_related_anatomy(point_info),
            'controls': {
                'rotate': True,
                'zoom': True,
                'layer_toggle': True,
                'cross_section': True
            }
        }

        return scene

    def meridian_visualization(self, meridian_name):
        """经络可视化"""
        meridian = self.get_meridian_data(meridian_name)

        return {
            'path': meridian['pathway'],
            'points': meridian['points'],
            'branches': meridian['branches'],
            'connections': meridian['connections'],
            'animation': {
                'qi_flow': True,
                'direction': meridian['flow_direction'],
                'speed': 'medium'
            }
        }
```

### 2.6 常用穴位配伍

```python
class AcupointCombinations:
    """穴位配伍数据库"""

    classic_combinations = {
        '四关穴': {
            'points': ['合谷', '太冲'],
            'functions': ['疏肝理气', '行气活血', '镇痛'],
            'indications': ['头痛', '眩晕', '高血压', '月经不调', '情志病']
        },
        '四总穴': {
            'points': ['足三里', '委中', '列缺', '合谷'],
            'functions': ['肚腹三里留', '腰背委中求', '头项寻列缺', '面口合谷收'],
            'indications': ['相应部位疾病']
        },
        '回阳九针': {
            'points': ['哑门', '劳宫', '三阴交', '涌泉', '太溪', '中脘', '环跳', '足三里', '合谷'],
            'functions': ['回阳救逆'],
            'indications': ['亡阳证', '厥证']
        },
        '十三鬼穴': {
            'points': ['人中', '少商', '隐白', '大陵', '申脉', '风府', '颊车', '承浆', '劳宫', '上星', '会阴', '曲池', '海泉'],
            'functions': ['醒脑开窍', '宁心安神'],
            'indications': ['癫狂', '精神疾病']
        }
    }

    condition_combinations = {
        '头痛': {
            '风寒头痛': ['风池', '风门', '合谷', '列缺'],
            '风热头痛': ['风池', '曲池', '合谷', '太阳'],
            '肝阳头痛': ['风池', '太冲', '太溪', '侠溪'],
            '血虚头痛': ['百会', '足三里', '三阴交', '血海'],
            '瘀血头痛': ['阿是穴', '合谷', '太冲', '膈俞']
        },
        '失眠': {
            '心脾两虚': ['神门', '三阴交', '心俞', '脾俞'],
            '心肾不交': ['神门', '太溪', '心俞', '肾俞'],
            '肝火扰心': ['神门', '太冲', '行间', '风池'],
            '痰热扰心': ['神门', '丰隆', '内关', '曲池']
        },
        '腰痛': {
            '寒湿腰痛': ['肾俞', '腰阳关', '委中', '昆仑'],
            '瘀血腰痛': ['肾俞', '膈俞', '委中', '次髎'],
            '肾虚腰痛': ['肾俞', '命门', '太溪', '志室']
        }
    }
```

---

## 3. 推拿手法数据库系统

### 3.1 系统概述

全面的推拿手法数据库，包含各种手法技术、适应症、3D演示和操作指导。

### 3.2 手法分类体系

```yaml
推拿手法分类:

  1. 摆动类手法:
    - 一指禅推法
    - 滚法
    - 揉法
    - 缠法

  2. 摩擦类手法:
    - 推法
    - 摩法
    - 擦法
    - 搓法
    - 抹法

  3. 挤压类手法:
    - 按法
    - 点法
    - 拿法
    - 捏法
    - 掐法
    - 捻法
    - 踩跷法

  4. 叩击类手法:
    - 拍法
    - 击法
    - 弹法

  5. 振动类手法:
    - 振法
    - 抖法

  6. 运动关节类手法:
    - 摇法
    - 扳法
    - 拔伸法
    - 背法
```

### 3.3 手法数据结构

```python
class TuinaManipulation:
    """推拿手法数据结构"""

    manipulation_schema = {
        'basic_info': {
            'name': str,                    # 手法名称
            'category': str,                # 分类
            'aliases': list,                # 别名
            'description': str              # 描述
        },
        'technique': {
            'hand_position': str,           # 手部姿势
            'contact_area': str,            # 接触部位
            'force_direction': str,         # 用力方向
            'movement_pattern': str,        # 运动形式
            'rhythm': str,                  # 节律
            'frequency': str,               # 频率
            'duration': str,                # 持续时间
            'force_intensity': str          # 力度
        },
        'application': {
            'body_regions': list,           # 适用部位
            'indications': list,            # 适应症
            'contraindications': list,      # 禁忌症
            'precautions': list,            # 注意事项
            'effects': list                 # 作用效果
        },
        'combination': {
            'combined_techniques': list,    # 配合手法
            'acupoints': list,              # 配合穴位
            'sequences': list               # 操作顺序
        },
        'media': {
            'images': list,                 # 图片
            '3d_animation': str,            # 3D动画
            'video_demo': str,              # 视频演示
            'hand_diagram': str             # 手势图
        },
        'training': {
            'difficulty_level': str,        # 难度等级
            'practice_tips': list,          # 练习要点
            'common_errors': list,          # 常见错误
            'progression': list             # 进阶练习
        }
    }
```

### 3.4 常用手法详细信息

```python
tuina_techniques = {
    '一指禅推法': {
        'category': '摆动类',
        'description': '用拇指指端、罗纹面或偏峰着力于一定部位或穴位，沉肩、垂肘、悬腕，以肘关节为支点，前臂作主动摆动，带动腕部摆动和拇指关节做屈伸活动',
        'technique': {
            'hand_position': '拇指伸直，其余四指自然弯曲',
            'contact_area': '拇指指端、罗纹面或偏峰',
            'force_direction': '垂直向下，略带推动',
            'movement_pattern': '摆动',
            'rhythm': '均匀',
            'frequency': '120-160次/分',
            'duration': '每穴位3-5分钟',
            'force_intensity': '中等，以渗透为度'
        },
        'effects': [
            '舒筋活络',
            '调和营卫',
            '祛瘀消积',
            '健脾和胃'
        ],
        'indications': [
            '头痛',
            '失眠',
            '胃脘痛',
            '腹痛',
            '肩周炎',
            '颈椎病'
        ],
        'body_regions': ['头面部', '颈项部', '腰背部', '四肢'],
        'key_points': [
            '肩部放松，不可耸肩',
            '肘部自然下垂',
            '腕部灵活，不可僵硬',
            '用力均匀，深透有力',
            '频率要稳定'
        ]
    },

    '滚法': {
        'category': '摆动类',
        'description': '用手背近小指侧部分或小指、无名指、中指的掌指关节突起部分着力，附着于一定部位上，通过腕关节连续的屈伸外旋活动，使产生的力持续作用于治疗部位',
        'technique': {
            'hand_position': '手指自然弯曲，小指侧着力',
            'contact_area': '第5掌指关节背侧',
            'force_direction': '垂直加滚动',
            'movement_pattern': '腕关节屈伸+前臂旋转',
            'rhythm': '均匀连续',
            'frequency': '120-160次/分',
            'duration': '每部位5-10分钟',
            'force_intensity': '中等偏重'
        },
        'effects': [
            '舒筋活血',
            '滑利关节',
            '缓解肌肉痉挛',
            '消除疲劳'
        ],
        'indications': [
            '颈椎病',
            '肩周炎',
            '腰肌劳损',
            '坐骨神经痛',
            '风湿痹痛'
        ],
        'body_regions': ['颈肩部', '腰背部', '臀部', '四肢'],
        'key_points': [
            '腕部放松，滚动自如',
            '吸定不移，紧贴皮肤',
            '压力均匀',
            '幅度要够（120度）',
            '手背滚动，不是手掌'
        ]
    },

    '按法': {
        'category': '挤压类',
        'description': '用指、掌或肘等部位着力于一定的部位或穴位上，逐渐用力下按',
        'variants': {
            '指按法': {
                'contact': '拇指或中指指端',
                'use': '穴位点按',
                'force': '轻到中等'
            },
            '掌按法': {
                'contact': '掌根或全掌',
                'use': '大面积部位',
                'force': '中等到重'
            },
            '肘按法': {
                'contact': '肘尖或鹰嘴',
                'use': '腰臀等肌肉丰厚处',
                'force': '重'
            }
        },
        'effects': [
            '开通闭塞',
            '活血止痛',
            '放松肌肉',
            '矫正畸形'
        ],
        'key_points': [
            '着力部位要紧贴体表',
            '用力方向要垂直向下',
            '用力要由轻到重，稳而持续',
            '不可用暴力或突然用力'
        ]
    },

    '拿法': {
        'category': '挤压类',
        'description': '用拇指与其他手指相对用力，在一定部位和穴位上进行节律性的提捏',
        'technique': {
            'hand_position': '拇指与其余四指对合',
            'contact_area': '指腹',
            'movement_pattern': '提捏',
            'rhythm': '缓和有力',
            'frequency': '缓慢，每分钟30-50次'
        },
        'variants': {
            '三指拿': '拇指与食、中指',
            '五指拿': '拇指与其余四指'
        },
        'effects': [
            '疏通经络',
            '开窍醒脑',
            '缓解痉挛',
            '消除疲劳'
        ],
        'indications': [
            '颈项强痛',
            '肩臂酸痛',
            '头痛',
            '感冒'
        ],
        'classic_applications': {
            '拿风池': '治疗头痛、感冒',
            '拿肩井': '治疗肩颈疼痛',
            '拿合谷': '治疗头面五官疾患'
        }
    },

    '摇法': {
        'category': '运动关节类',
        'description': '用一手握住关节近端，另一手握住关节远端，作缓和的环转运动',
        'joints': {
            '颈椎摇法': {
                'position': '患者坐位',
                'method': '一手扶头顶，一手托下颌，缓慢摇转',
                'range': '适度，不超过正常活动范围',
                'caution': '动作轻柔，不可用力过猛'
            },
            '肩关节摇法': {
                'position': '患者坐位或卧位',
                'method': '一手扶肩，一手握腕，环转运动',
                'range': '逐渐增大',
                'indications': ['肩周炎', '肩关节活动受限']
            },
            '腰椎摇法': {
                'position': '患者侧卧位',
                'method': '一手按腰，一手握踝，旋转髋关节带动腰椎',
                'range': '适度',
                'caution': '腰椎间盘突出者慎用'
            },
            '髋关节摇法': {
                'position': '患者仰卧位',
                'method': '屈髋屈膝，握膝做环转运动',
                'range': '由小到大',
                'indications': ['髋关节疾患', '腰腿痛']
            }
        },
        'effects': [
            '滑利关节',
            '松解粘连',
            '增加活动范围'
        ],
        'key_points': [
            '动作缓和',
            '力量适中',
            '活动范围由小到大',
            '不可使用暴力'
        ]
    },

    '扳法': {
        'category': '运动关节类',
        'description': '用巧力作较大幅度的快速旋转或屈伸动作，常伴有关节弹响',
        'types': {
            '颈椎扳法': {
                '斜扳法': {
                    'position': '患者坐位，颈部前屈并旋转',
                    'method': '一手扶头侧，一手扶下颌，寸劲扳动',
                    'indications': ['颈椎小关节紊乱', '落枕'],
                    'contraindications': ['颈椎不稳', '椎动脉型颈椎病', '严重骨质疏松']
                },
                '旋转扳法': {
                    'position': '患者坐位，颈部中立位',
                    'method': '旋转头部至最大角度，寸劲加力',
                    'caution': '动作要稳准，力量要适度'
                }
            },
            '胸椎扳法': {
                '扩胸扳法': {
                    'position': '患者坐位，双手交叉抱于颈后',
                    'method': '医者从背后抱住患者双肘，向后扳动',
                    'indications': ['胸椎小关节紊乱', '背痛']
                }
            },
            '腰椎扳法': {
                '斜扳法': {
                    'position': '患者侧卧位，上腿屈曲，下腿伸直',
                    'method': '一手按肩向后，一手按臀向前，相对用力',
                    'indications': ['腰椎后关节紊乱', '急性腰扭伤']
                },
                '旋转扳法': {
                    'position': '患者坐位',
                    'method': '旋转腰部至最大角度，寸劲加力'
                }
            }
        },
        'key_points': [
            '扳动前要充分放松肌肉',
            '活动到位后寸劲发力',
            '力量要稳、准、巧',
            '不可使用暴力',
            '注意禁忌症'
        ]
    }
}
```

### 3.5 3D手法演示

```python
class TuinaVisualization:
    """推拿手法3D可视化"""

    def create_technique_demo(self, technique_name):
        """创建手法3D演示"""
        technique = self.get_technique(technique_name)

        demo = {
            'scene': {
                'patient_model': self.get_patient_model(technique['body_regions']),
                'practitioner_hands': self.get_hand_models(),
                'treatment_table': self.get_table_model()
            },
            'animations': self.create_animations(technique),
            'viewpoints': {
                'overview': '整体视角',
                'hand_closeup': '手部特写',
                'contact_point': '接触点视角',
                'patient_view': '患者视角'
            },
            'annotations': {
                'contact_area': technique['contact_area'],
                'force_direction': technique['force_direction'],
                'movement_arrows': True,
                'key_points': technique['key_points']
            },
            'controls': {
                'play_pause': True,
                'speed_control': True,
                'step_by_step': True,
                'loop': True,
                'rotate_view': True,
                'zoom': True
            },
            'audio': {
                'narration': self.generate_narration(technique),
                'rhythm_guide': technique.get('rhythm_audio')
            }
        }

        return demo

    def create_animations(self, technique):
        """创建动画序列"""
        animations = []

        # 准备动作
        animations.append({
            'name': '准备姿势',
            'duration': 2000,
            'description': technique['hand_position']
        })

        # 接触
        animations.append({
            'name': '接触部位',
            'duration': 1500,
            'description': f"接触点：{technique['contact_area']}"
        })

        # 主要动作循环
        animations.append({
            'name': '主要手法',
            'duration': 5000,
            'loop': True,
            'speed': technique['frequency'],
            'description': technique['movement_pattern']
        })

        return animations

    def hand_position_guide(self, technique_name):
        """手部姿势指导"""
        technique = self.get_technique(technique_name)

        return {
            '3d_hand_model': self.render_hand_position(technique),
            'finger_positions': technique['hand_position'],
            'wrist_angle': technique.get('wrist_angle'),
            'force_distribution': self.visualize_force(technique),
            'common_errors': technique['training']['common_errors'],
            'correction_tips': technique['training']['practice_tips']
        }
```

### 3.6 推拿治疗方案

```python
class TuinaTreatmentProtocol:
    """推拿治疗方案"""

    def generate_protocol(self, diagnosis, affected_areas):
        """生成推拿治疗方案"""
        protocol = {
            'preparation': [],
            'main_treatment': [],
            'finishing': [],
            'total_duration': 0,
            'frequency': '',
            'course': ''
        }

        # 1. 准备手法
        protocol['preparation'] = self.get_preparation_techniques(affected_areas)

        # 2. 主要治疗
        main_techniques = self.select_techniques(diagnosis, affected_areas)
        protocol['main_treatment'] = main_techniques

        # 3. 结束手法
        protocol['finishing'] = self.get_finishing_techniques(affected_areas)

        # 4. 配合穴位
        protocol['acupoints'] = self.recommend_acupoints(diagnosis)

        # 5. 治疗参数
        protocol['total_duration'] = self.calculate_duration(protocol)
        protocol['frequency'] = self.recommend_frequency(diagnosis)
        protocol['course'] = self.recommend_course(diagnosis)

        return protocol

    condition_protocols = {
        '颈椎病': {
            'preparation': [
                {'technique': '滚法', 'region': '颈肩部', 'duration': '3分钟'},
                {'technique': '按揉法', 'region': '颈项肌', 'duration': '2分钟'}
            ],
            'main_treatment': [
                {'technique': '一指禅推法', 'points': ['风池', '天柱', '颈夹脊'], 'duration': '5分钟'},
                {'technique': '拿法', 'region': '颈项部', 'duration': '3分钟'},
                {'technique': '弹拨法', 'region': '斜方肌、胸锁乳突肌', 'duration': '2分钟'},
                {'technique': '颈椎摇法', 'duration': '2分钟'},
                {'technique': '颈椎扳法', 'note': '根据情况选用'}
            ],
            'finishing': [
                {'technique': '拍法', 'region': '颈肩部', 'duration': '1分钟'}
            ],
            'acupoints': ['风池', '天柱', '肩井', '大椎', '后溪'],
            'frequency': '每日或隔日1次',
            'course': '10次为一疗程'
        },

        '腰椎间盘突出': {
            'preparation': [
                {'technique': '滚法', 'region': '腰背部', 'duration': '5分钟'},
                {'technique': '按揉法', 'region': '腰部肌肉', 'duration': '3分钟'}
            ],
            'main_treatment': [
                {'technique': '点按法', 'points': ['肾俞', '大肠俞', '环跳', '委中'], 'duration': '5分钟'},
                {'technique': '弹拨法', 'region': '竖脊肌、梨状肌', 'duration': '3分钟'},
                {'technique': '斜扳法', 'region': '腰椎', 'note': '急性期慎用'},
                {'technique': '牵引拔伸法', 'duration': '3分钟'}
            ],
            'finishing': [
                {'technique': '推法', 'region': '督脉', 'duration': '2分钟'},
                {'technique': '擦法', 'region': '腰骶部', 'duration': '1分钟'}
            ],
            'acupoints': ['肾俞', '大肠俞', '环跳', '委中', '承山', '昆仑'],
            'frequency': '每日或隔日1次',
            'course': '15次为一疗程'
        },

        '肩周炎': {
            'preparation': [
                {'technique': '滚法', 'region': '肩部周围', 'duration': '3分钟'},
                {'technique': '按揉法', 'region': '肩部肌肉', 'duration': '2分钟'}
            ],
            'main_treatment': [
                {'technique': '点按法', 'points': ['肩髃', '肩髎', '肩贞', '臂臑'], 'duration': '5分钟'},
                {'technique': '弹拨法', 'region': '冈上肌、冈下肌、肱二头肌', 'duration': '3分钟'},
                {'technique': '拿法', 'region': '肩臂部', 'duration': '2分钟'},
                {'technique': '摇法', 'joint': '肩关节', 'duration': '3分钟'},
                {'technique': '抬举法', 'duration': '2分钟'}
            ],
            'finishing': [
                {'technique': '搓法', 'region': '上肢', 'duration': '1分钟'},
                {'technique': '抖法', 'region': '上肢', 'duration': '1分钟'}
            ],
            'acupoints': ['肩髃', '肩髎', '肩贞', '曲池', '合谷', '阿是穴'],
            'frequency': '每日1次',
            'course': '10次为一疗程'
        }
    }
```

### 3.7 推拿与针灸结合

```python
class TuinaAcupunctureIntegration:
    """推拿针灸结合方案"""

    def integrated_treatment(self, condition, diagnosis):
        """生成综合治疗方案"""
        return {
            'sequence': self.determine_sequence(condition),
            'tuina_protocol': self.get_tuina_protocol(condition),
            'acupuncture_protocol': self.get_acupuncture_protocol(condition),
            'rationale': self.explain_integration(condition),
            'synergy_effects': self.describe_synergy(condition)
        }

    def determine_sequence(self, condition):
        """确定治疗顺序"""
        # 一般原则：先推拿后针灸，或针灸留针时推拿
        sequences = {
            '肌肉痉挛': '先推拿放松肌肉，后针灸调理',
            '关节疾病': '先针灸镇痛，后推拿松解',
            '经络阻滞': '针灸推拿同时进行',
            '气血不足': '先针灸补益，后推拿调理'
        }

        return sequences.get(condition['type'], '根据具体情况灵活运用')
```

---

## 4. 统一更新机制

### 4.1 更新组件

```yaml
可更新组件:
  AI模型:
    - 舌诊AI模型
    - 面诊AI模型
    - 皮肤分析模型
    - 图像识别模型

  数据库:
    - 穴位数据库
    - 推拿手法数据库
    - 症状图谱数据库
    - 经络数据库

  媒体资源:
    - 3D模型
    - 演示视频
    - AR标记
    - 图片资源

  知识库:
    - 辨证规则
    - 配穴方案
    - 治疗方案
    - 最新研究
```

### 4.2 更新管理器

```python
class UnifiedUpdateManager:
    """统一更新管理器"""

    def __init__(self):
        self.components = {
            'tongue_ai': {'check': 'weekly', 'auto': False},
            'face_ai': {'check': 'weekly', 'auto': False},
            'skin_ai': {'check': 'weekly', 'auto': False},
            'acupoint_db': {'check': 'monthly', 'auto': True},
            'tuina_db': {'check': 'monthly', 'auto': True},
            'symptom_atlas': {'check': 'weekly', 'auto': True},
            '3d_models': {'check': 'monthly', 'auto': True},
            'research_db': {'check': 'weekly', 'auto': True}
        }

    def check_updates(self):
        """检查所有更新"""
        updates = []

        for component, config in self.components.items():
            update = self.check_component(component)
            if update['available']:
                updates.append({
                    'component': component,
                    'current_version': update['current'],
                    'new_version': update['new'],
                    'changes': update['changelog'],
                    'priority': update['priority'],
                    'auto_update': config['auto']
                })

        return updates

    def notify_user(self, updates):
        """通知用户更新"""
        notifications = []

        for update in updates:
            notification = {
                'title': f"{update['component']} 有新更新",
                'message': f"版本 {update['new_version']} 可用",
                'priority': update['priority'],
                'changes': update['changes'][:3],  # 显示前3条更新内容
                'actions': ['立即更新', '稍后提醒', '查看详情']
            }

            notifications.append(notification)

        return notifications
```

---

## 5. 数据库设计

### 5.1 拍照诊断数据库

```sql
-- 症状照片
CREATE TABLE symptom_photos (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    visit_id UUID REFERENCES visits(id),
    photo_type VARCHAR(50) NOT NULL,  -- tongue, face, skin, etc.
    image_path VARCHAR(255) NOT NULL,
    thumbnail_path VARCHAR(255),
    original_filename VARCHAR(255),
    file_size BIGINT,
    resolution VARCHAR(20),
    captured_at TIMESTAMP NOT NULL,
    device_info JSONB,
    location_info JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI分析结果
CREATE TABLE photo_ai_analysis (
    id UUID PRIMARY KEY,
    photo_id UUID REFERENCES symptom_photos(id),
    model_version VARCHAR(50) NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    findings JSONB NOT NULL,
    tcm_diagnosis JSONB,
    western_correlation JSONB,
    confidence_scores JSONB,
    annotations JSONB,
    recommendations JSONB,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 症状时间线
CREATE TABLE symptom_timeline (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    symptom_type VARCHAR(50) NOT NULL,
    photo_ids JSONB,  -- Array of photo IDs
    progression_analysis JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 拍照指南
CREATE TABLE photo_guides (
    id UUID PRIMARY KEY,
    photo_type VARCHAR(50) UNIQUE NOT NULL,
    instructions JSONB,
    overlay_image VARCHAR(255),
    example_images JSONB,
    common_errors JSONB,
    tips JSONB,
    is_active BOOLEAN DEFAULT true
);
```

### 5.2 针灸穴位数据库

```sql
-- 穴位主表
CREATE TABLE acupoints (
    id UUID PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,  -- e.g., LI4
    chinese_name VARCHAR(50) NOT NULL,
    pinyin VARCHAR(50),
    english_name VARCHAR(100),
    meridian_id UUID REFERENCES meridians(id),
    point_number INTEGER,
    point_types JSONB,  -- 原穴、络穴等
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 穴位位置
CREATE TABLE acupoint_locations (
    id UUID PRIMARY KEY,
    acupoint_id UUID REFERENCES acupoints(id),
    anatomical_location TEXT,
    location_method TEXT,
    cun_measurement TEXT,
    simple_location TEXT,
    needle_depth VARCHAR(50),
    needle_angle VARCHAR(50),
    coordinates_3d JSONB,
    body_region VARCHAR(50)
);

-- 穴位临床应用
CREATE TABLE acupoint_clinical (
    id UUID PRIMARY KEY,
    acupoint_id UUID REFERENCES acupoints(id),
    indications JSONB,
    functions JSONB,
    contraindications JSONB,
    cautions JSONB,
    needling_sensation TEXT,
    manipulations JSONB,
    moxibustion_info JSONB,
    combinations JSONB
);

-- 穴位媒体
CREATE TABLE acupoint_media (
    id UUID PRIMARY KEY,
    acupoint_id UUID REFERENCES acupoints(id),
    media_type VARCHAR(50),
    file_path VARCHAR(255),
    thumbnail_path VARCHAR(255),
    description TEXT,
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 经络
CREATE TABLE meridians (
    id UUID PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    chinese_name VARCHAR(50) NOT NULL,
    english_name VARCHAR(100),
    pathway TEXT,
    point_count INTEGER,
    element VARCHAR(20),
    yin_yang VARCHAR(10),
    paired_meridian_id UUID,
    flow_direction VARCHAR(20),
    peak_time VARCHAR(20)
);

-- 穴位配伍
CREATE TABLE acupoint_combinations (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    acupoint_ids JSONB,
    indications JSONB,
    functions JSONB,
    source TEXT,
    is_classic BOOLEAN DEFAULT false
);
```

### 5.3 推拿手法数据库

```sql
-- 推拿手法主表
CREATE TABLE tuina_techniques (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    aliases JSONB,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 手法技术细节
CREATE TABLE technique_details (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES tuina_techniques(id),
    hand_position TEXT,
    contact_area TEXT,
    force_direction TEXT,
    movement_pattern TEXT,
    rhythm TEXT,
    frequency TEXT,
    duration TEXT,
    force_intensity TEXT
);

-- 手法应用
CREATE TABLE technique_applications (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES tuina_techniques(id),
    body_regions JSONB,
    indications JSONB,
    contraindications JSONB,
    precautions JSONB,
    effects JSONB
);

-- 手法媒体
CREATE TABLE technique_media (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES tuina_techniques(id),
    media_type VARCHAR(50),
    title VARCHAR(255),
    file_path VARCHAR(255),
    thumbnail_path VARCHAR(255),
    duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 手法训练
CREATE TABLE technique_training (
    id UUID PRIMARY KEY,
    technique_id UUID REFERENCES tuina_techniques(id),
    difficulty_level VARCHAR(20),
    practice_tips JSONB,
    common_errors JSONB,
    progression JSONB
);

-- 推拿治疗方案
CREATE TABLE tuina_protocols (
    id UUID PRIMARY KEY,
    condition VARCHAR(100) NOT NULL,
    preparation JSONB,
    main_treatment JSONB,
    finishing JSONB,
    acupoints JSONB,
    frequency TEXT,
    course TEXT,
    notes TEXT
);

-- 推拿治疗记录
CREATE TABLE tuina_treatments (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    visit_id UUID REFERENCES visits(id),
    protocol_id UUID REFERENCES tuina_protocols(id),
    techniques_used JSONB,
    body_regions JSONB,
    duration INTEGER,
    patient_response TEXT,
    practitioner_notes TEXT,
    practitioner_id UUID REFERENCES users(id),
    treatment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. API接口设计

### 6.1 拍照诊断API

```yaml
拍照诊断API:

  上传分析:
    POST /api/photo/analyze:
      description: "上传症状照片并AI分析"
      request:
        multipart/form-data:
          image: file (required)
          patient_id: uuid (required)
          photo_type: string (required)  # tongue, face, skin
          visit_id: uuid
      response:
        photo_id: uuid
        analysis: object
        findings: array
        tcm_diagnosis: object
        confidence: number
        annotations: array

  获取拍照指南:
    GET /api/photo/guide/{photo_type}:
      description: "获取拍照指导"
      response:
        instructions: array
        overlay: string
        examples: array
        tips: array

  获取时间线:
    GET /api/photo/timeline/{patient_id}:
      parameters:
        symptom_type: string
      response:
        timeline: array
        progression: object

  对比照片:
    POST /api/photo/compare:
      request:
        photo_ids: array
      response:
        comparison: object
        changes: array
```

### 6.2 针灸穴位API

```yaml
针灸穴位API:

  搜索穴位:
    GET /api/acupoints/search:
      parameters:
        q: string
        meridian: string
        indication: string
        region: string
      response:
        acupoints: array
        total: integer

  获取穴位详情:
    GET /api/acupoints/{code}:
      response:
        acupoint: object
        location: object
        clinical: object
        media: array

  AI推荐穴位:
    POST /api/acupoints/recommend:
      request:
        diagnosis: object
        symptoms: array
        patient_profile: object
      response:
        primary_points: array
        secondary_points: array
        rationale: string

  获取3D模型:
    GET /api/acupoints/{code}/3d:
      response:
        scene_config: object
        animations: array

  AR定位:
    POST /api/acupoints/ar-locate:
      request:
        point_codes: array
        body_image: file
      response:
        locations: array
        overlay: object
```

### 6.3 推拿手法API

```yaml
推拿手法API:

  获取手法列表:
    GET /api/tuina/techniques:
      parameters:
        category: string
        body_region: string
        indication: string
      response:
        techniques: array

  获取手法详情:
    GET /api/tuina/techniques/{id}:
      response:
        technique: object
        details: object
        applications: object
        media: array
        training: object

  获取3D演示:
    GET /api/tuina/techniques/{id}/demo:
      response:
        scene: object
        animations: array
        narration: string

  获取治疗方案:
    GET /api/tuina/protocols/{condition}:
      response:
        protocol: object

  记录治疗:
    POST /api/tuina/treatments:
      request:
        patient_id: uuid
        visit_id: uuid
        techniques: array
        duration: integer
        notes: string
      response:
        treatment_id: uuid
```

---

## 7. 界面设计

### 7.1 拍照诊断界面

```
┌─────────────────────────────────────────────────────────────────┐
│  症状拍照AI诊断                                  [历史] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [舌象] [面部] [皮肤] [指甲] [目诊] [其他]                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │              📷 相机取景框                               │    │
│  │                                                         │    │
│  │         ┌─────────────────┐                             │    │
│  │         │   [舌象轮廓]    │                             │    │
│  │         │                 │                             │    │
│  │         │   引导叠加层    │                             │    │
│  │         │                 │                             │    │
│  │         └─────────────────┘                             │    │
│  │                                                         │    │
│  │  💡 光线: 良好  🎯 对焦: OK  📐 构图: OK                  │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  拍摄提示:                                                      │
│  • 自然光线下拍摄                                               │
│  • 舌头自然伸出，不要过度用力                                   │
│  • 包含整个舌体                                                 │
│                                                                 │
│  [切换摄像头]  [ 📸 拍摄 ]  [闪光灯]  [相册]                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

拍摄后分析界面:

┌─────────────────────────────────────────────────────────────────┐
│  舌象AI分析结果                                  [重拍] [保存]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌────────────────────────────────────┐   │
│  │                  │  │  分析结果                          │   │
│  │   [舌象照片]     │  ├────────────────────────────────────┤   │
│  │                  │  │                                    │   │
│  │   [AI标注叠加]   │  │  舌体:                              │   │
│  │                  │  │  • 颜色: 淡红                       │   │
│  │                  │  │  • 形态: 胖大，边有齿痕             │   │
│  └──────────────────┘  │                                    │   │
│                        │  舌苔:                              │   │
│  置信度: 92%           │  • 颜色: 白                         │   │
│                        │  • 厚薄: 薄                         │   │
│                        │  • 润燥: 润                         │   │
│                        │                                    │   │
│                        │  辨证:                              │   │
│                        │  脾气虚证                           │   │
│                        │                                    │   │
│                        │  病机:                              │   │
│                        │  脾失健运，水湿内停                 │   │
│                        │                                    │   │
│                        └────────────────────────────────────┘   │
│                                                                 │
│  [添加到病历] [查看时间线] [分享] [打印]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 针灸穴位界面

```
┌─────────────────────────────────────────────────────────────────┐
│  AI针灸穴位系统                                  [收藏] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🔍 搜索穴位 (名称、代码、主治)                         │    │
│  │  [合谷                                              ] 🎤  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [按经络] [按部位] [按主治] [AI推荐] [常用配伍]                  │
│                                                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │  合谷 (LI4)             │  │                              │  │
│  │  手阳明大肠经           │  │    [3D穴位定位图]            │  │
│  ├─────────────────────────┤  │                              │  │
│  │                         │  │    [AR定位] [测量指导]       │  │
│  │  定位:                  │  │                              │  │
│  │  手背，第1、2掌骨间，   │  └──────────────────────────────┘  │
│  │  第2掌骨桡侧中点处      │                                    │
│  │                         │  ┌──────────────────────────────┐  │
│  │  简便取穴:              │  │  功效主治                    │  │
│  │  拇食指并拢，肌肉最高处 │  ├──────────────────────────────┤  │
│  │                         │  │                              │  │
│  │  针刺:                  │  │  功效:                       │  │
│  │  直刺0.5-1寸            │  │  • 镇静止痛                  │  │
│  │                         │  │  • 通经活络                  │  │
│  │  穴位类型:              │  │  • 清热解表                  │  │
│  │  • 原穴                 │  │                              │  │
│  │  • 四总穴之一           │  │  主治:                       │  │
│  │                         │  │  • 头痛、牙痛、咽喉肿痛      │  │
│  │  ⚠ 孕妇禁针            │  │  • 发热、无汗、多汗          │  │
│  │                         │  │  • 经闭、滞产                │  │
│  └─────────────────────────┘  │  • 面瘫、口眼歪斜            │  │
│                               │                              │  │
│                               │  常用配伍:                   │  │
│                               │  • 配太冲 - 四关穴           │  │
│                               │  • 配复溜 - 止汗/发汗        │  │
│                               └──────────────────────────────┘  │
│                                                                 │
│  [添加到处方] [查看视频] [AR定位] [打印]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 推拿手法界面

```
┌─────────────────────────────────────────────────────────────────┐
│  推拿手法数据库                                  [收藏] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [摆动类] [摩擦类] [挤压类] [叩击类] [振动类] [运动关节类]       │
│                                                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │  滚法                   │  │                              │  │
│  │  摆动类手法             │  │    [3D动画演示区]            │  │
│  ├─────────────────────────┤  │                              │  │
│  │                         │  │  ▶ [播放] [暂停] [步骤]      │  │
│  │  分类: 摆动类           │  │                              │  │
│  │  难度: ⭐⭐⭐           │  │  [正面] [侧面] [手部特写]    │  │
│  │                         │  │                              │  │
│  │  手法要领:              │  └──────────────────────────────┘  │
│  │  • 手指自然弯曲         │                                    │
│  │  • 小指侧着力           │  ┌──────────────────────────────┐  │
│  │  • 腕关节屈伸+旋转      │  │  操作要点                    │  │
│  │  • 频率120-160次/分     │  ├──────────────────────────────┤  │
│  │                         │  │                              │  │
│  │  适用部位:              │  │  ✓ 腕部放松，滚动自如        │  │
│  │  • 颈肩部               │  │  ✓ 吸定不移，紧贴皮肤        │  │
│  │  • 腰背部               │  │  ✓ 压力均匀                  │  │
│  │  • 臀部                 │  │  ✓ 幅度要够（120度）         │  │
│  │  • 四肢                 │  │                              │  │
│  │                         │  │  ✗ 常见错误:                 │  │
│  │  功效:                  │  │  • 腕部僵硬                  │  │
│  │  • 舒筋活血             │  │  • 用手掌滚动                │  │
│  │  • 滑利关节             │  │  • 幅度过小                  │  │
│  │  • 缓解肌肉痉挛         │  │                              │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
│                                                                 │
│  [记录治疗] [查看方案] [练习模式] [打印指导]                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 安全与合规

### 8.1 图像数据安全

```yaml
图像安全措施:
  存储:
    - AES-256加密存储
    - 去标识化处理
    - 访问控制
    - 审计日志

  传输:
    - TLS 1.3加密
    - 证书验证

  隐私:
    - 患者同意授权
    - 数据最小化
    - 保留期限管理
    - 删除权支持
```

### 8.2 AI诊断免责声明

```yaml
免责声明:
  - AI分析仅供参考，不能替代专业诊断
  - 最终诊断需由执业中医师确认
  - 如有紧急情况，请立即就医
  - 系统不提供处方建议
```

---

## 9. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2024 | 初始版本 - 拍照AI诊断、针灸穴位、推拿手法系统 |

---

**文档结束**
