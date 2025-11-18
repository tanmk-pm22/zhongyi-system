# 中药真伪辨别、供应商市场、OCR识别与病人查询系统技术规格

## 文档信息
- **版本**: 1.0
- **创建日期**: 2024年
- **适用范围**: 马来西亚中医诊所系统
- **合规标准**: Malaysia T&CM Act 2016, PDPA 2010

---

## 目录
1. [中药草药AI真伪辨别系统](#1-中药草药ai真伪辨别系统)
2. [中药批发市场供应商数据库](#2-中药批发市场供应商数据库)
3. [中医AI仪器厂商数据库](#3-中医ai仪器厂商数据库)
4. [中成药批发商供应系统](#4-中成药批发商供应系统)
5. [OCR文字识别与翻译系统](#5-ocr文字识别与翻译系统)
6. [QR码与身份证病人查询系统](#6-qr码与身份证病人查询系统)
7. [数据库设计](#7-数据库设计)
8. [API接口设计](#8-api接口设计)
9. [界面设计](#9-界面设计)

---

## 1. 中药草药AI真伪辨别系统

### 1.1 系统概述

基于深度学习的中药材真伪鉴别系统，通过拍照即可识别中药材的真伪、品质和等级。

### 1.2 核心功能

#### 1.2.1 支持的鉴别类型

```yaml
鉴别范围:
  常用中药材:
    - 根及根茎类 (人参、黄芪、当归、甘草等)
    - 果实种子类 (枸杞、五味子、决明子等)
    - 花类 (金银花、菊花、红花等)
    - 全草类 (薄荷、藿香、益母草等)
    - 叶类 (桑叶、枇杷叶、艾叶等)
    - 皮类 (肉桂、厚朴、黄柏等)
    - 动物类 (鹿茸、阿胶、蜈蚣等)
    - 矿物类 (朱砂、石膏、滑石等)

  鉴别内容:
    - 真伪鉴别 (正品/伪品/混淆品)
    - 品质等级 (特级/一级/二级/三级)
    - 产地鉴别
    - 加工方式鉴别
    - 储存状况评估
    - 掺假检测
```

#### 1.2.2 AI鉴别引擎

```python
class HerbAuthenticationEngine:
    """中药材AI鉴别引擎"""

    def __init__(self):
        self.models = {
            'identification': HerbIdentificationModel(),
            'authentication': HerbAuthenticationModel(),
            'quality': HerbQualityModel(),
            'origin': HerbOriginModel()
        }
        self.herb_database = HerbReferenceDatabase()

    def authenticate(self, image, herb_name=None):
        """鉴别中药材"""
        results = {
            'identification': {},
            'authentication': {},
            'quality': {},
            'characteristics': {},
            'recommendations': []
        }

        # 1. 品种识别
        if herb_name:
            results['identification'] = {
                'claimed': herb_name,
                'detected': self.identify_herb(image),
                'match': False
            }
        else:
            results['identification'] = self.identify_herb(image)

        herb_id = results['identification'].get('herb_id')

        # 2. 真伪鉴别
        results['authentication'] = self.authenticate_herb(image, herb_id)

        # 3. 品质评估
        results['quality'] = self.assess_quality(image, herb_id)

        # 4. 特征分析
        results['characteristics'] = self.analyze_characteristics(image, herb_id)

        # 5. 建议
        results['recommendations'] = self.generate_recommendations(results)

        return results

    def identify_herb(self, image):
        """识别中药材品种"""
        # 图像预处理
        processed = self.preprocess(image)

        # AI识别
        predictions = self.models['identification'].predict(processed)

        # 返回Top-5结果
        return {
            'primary': {
                'herb_id': predictions[0]['id'],
                'name': predictions[0]['name'],
                'pinyin': predictions[0]['pinyin'],
                'confidence': predictions[0]['confidence']
            },
            'alternatives': predictions[1:5]
        }

    def authenticate_herb(self, image, herb_id):
        """真伪鉴别"""
        # 获取参考标准
        reference = self.herb_database.get_reference(herb_id)

        # AI鉴别
        auth_result = self.models['authentication'].predict(image, reference)

        return {
            'is_authentic': auth_result['authentic'],
            'confidence': auth_result['confidence'],
            'verdict': auth_result['verdict'],  # 正品/伪品/疑似伪品
            'evidence': {
                'matching_features': auth_result['matches'],
                'discrepancies': auth_result['discrepancies'],
                'key_identifiers': auth_result['identifiers']
            },
            'common_adulterants': self.get_common_adulterants(herb_id),
            'differentiation_points': self.get_differentiation_points(herb_id)
        }

    def assess_quality(self, image, herb_id):
        """品质评估"""
        quality_result = self.models['quality'].predict(image, herb_id)

        return {
            'grade': quality_result['grade'],  # 特级/一级/二级/三级
            'score': quality_result['score'],  # 0-100
            'factors': {
                'appearance': quality_result['appearance_score'],
                'color': quality_result['color_score'],
                'texture': quality_result['texture_score'],
                'integrity': quality_result['integrity_score'],
                'cleanliness': quality_result['cleanliness_score']
            },
            'defects': quality_result['defects'],
            'storage_condition': quality_result['storage'],
            'estimated_age': quality_result['age_estimate']
        }

    def analyze_characteristics(self, image, herb_id):
        """特征分析"""
        return {
            'morphology': self.analyze_morphology(image),
            'color': self.analyze_color(image),
            'texture': self.analyze_texture(image),
            'surface': self.analyze_surface(image),
            'cross_section': self.analyze_cross_section(image) if self.has_cross_section(image) else None
        }
```

#### 1.2.3 常见中药真伪鉴别要点

```python
class HerbAuthenticationKnowledge:
    """中药鉴别知识库"""

    authentication_points = {
        '人参': {
            'authentic_features': [
                '主根呈圆柱形或纺锤形',
                '表面灰黄色，有纵皱纹和横向皮孔',
                '芦头（根茎）明显，有芦碗',
                '质硬，断面淡黄白色，有菊花纹',
                '气特异，味微苦、甘'
            ],
            'common_adulterants': [
                {
                    'name': '商陆根',
                    'differences': '无芦头，断面同心环明显，味苦辣'
                },
                {
                    'name': '野豇豆根',
                    'differences': '表面有横长皮孔，断面纤维性'
                },
                {
                    'name': '华山参',
                    'differences': '根头部膨大，质轻泡'
                }
            ],
            'quality_indicators': {
                '特级': '芦长、体长、皮老、纹深，无破疤',
                '一级': '芦体较长，皮较老',
                '二级': '芦体一般，皮纹一般',
                '三级': '芦短体小，皮嫩纹浅'
            }
        },

        '冬虫夏草': {
            'authentic_features': [
                '虫体似蚕，长3-5cm',
                '表面深黄色至黄棕色，有环纹20-30条',
                '头部红棕色，足8对，中部4对明显',
                '子座细长，上部稍膨大',
                '质脆易折断，断面略平坦，淡黄白色'
            ],
            'common_adulterants': [
                {
                    'name': '亚香棒虫草',
                    'differences': '子座单生或分枝，虫体发黑'
                },
                {
                    'name': '凉山虫草',
                    'differences': '虫体较长，子座较长'
                },
                {
                    'name': '人工伪造品',
                    'differences': '用面粉、淀粉等模压，无环纹'
                }
            ]
        },

        '三七': {
            'authentic_features': [
                '主根呈类圆锥形或圆柱形',
                '表面灰褐色或灰黄色',
                '顶端有茎痕，周围有瘤状突起',
                '质坚实，断面灰绿色、黄绿色或灰白色',
                '气微，味苦回甜'
            ],
            'common_adulterants': [
                {
                    'name': '莪术',
                    'differences': '气香特异，味微苦辛'
                },
                {
                    'name': '姜黄',
                    'differences': '断面橙黄色，气香特异'
                }
            ]
        },

        '藏红花': {
            'authentic_features': [
                '柱头三分枝，长约3cm',
                '暗红色，上部宽而略扁平',
                '顶端边缘呈不整齐的齿状',
                '质松软，有光泽',
                '气特异，味微苦',
                '入水膨胀，水染金黄色'
            ],
            'common_adulterants': [
                {
                    'name': '红花',
                    'differences': '为管状花，不是柱头'
                },
                {
                    'name': '玉米须染色',
                    'differences': '无分枝，水浸颜色不正'
                },
                {
                    'name': '纸纤维染色',
                    'differences': '质地不对，无特异气味'
                }
            ],
            'authenticity_tests': [
                '水试：真品水染金黄色，花不褪色',
                '压片：真品油润有光泽',
                '显微：柱头顶端边缘有乳头状突起'
            ]
        }
    }
```

#### 1.2.4 拍照指导系统

```python
class HerbPhotoGuidance:
    """中药拍照指导"""

    def get_photo_requirements(self, herb_category):
        """获取拍照要求"""
        requirements = {
            'general': {
                'lighting': '自然光或均匀人工光',
                'background': '白色或浅色背景',
                'focus': '清晰对焦',
                'scale': '放置标尺参照',
                'angles': ['正面', '背面', '侧面', '断面']
            },
            'root_herbs': {
                'views': ['整体外观', '表面纹理', '断面', '顶端/芦头'],
                'details': ['皮部', '木部', '髓部'],
                'special': '如有支根需拍摄'
            },
            'flower_herbs': {
                'views': ['整体', '花瓣', '花蕊', '花萼'],
                'color': '注意颜色准确',
                'special': '避免压扁变形'
            },
            'seed_herbs': {
                'views': ['整体', '表面纹理', '种脐', '切面'],
                'quantity': '多颗一起拍摄对比'
            },
            'animal_herbs': {
                'views': ['整体', '特征部位', '断面/切面'],
                'special': '注意纹理和光泽'
            }
        }

        return requirements.get(herb_category, requirements['general'])

    def realtime_guidance(self, camera_feed, herb_type):
        """实时拍摄指导"""
        feedback = {
            'lighting': self.check_lighting(camera_feed),
            'focus': self.check_focus(camera_feed),
            'framing': self.check_framing(camera_feed),
            'scale_reference': self.check_scale(camera_feed),
            'suggestions': []
        }

        if not feedback['lighting']['adequate']:
            feedback['suggestions'].append('请增加光线或移到光线充足处')

        if not feedback['focus']['sharp']:
            feedback['suggestions'].append('请调整焦距使药材清晰')

        if not feedback['scale_reference']['present']:
            feedback['suggestions'].append('请放置标尺作为大小参照')

        return feedback
```

### 1.3 鉴别报告生成

```python
class AuthenticationReportGenerator:
    """鉴别报告生成器"""

    def generate_report(self, auth_results, herb_info):
        """生成鉴别报告"""
        report = {
            'header': {
                'report_id': generate_uuid(),
                'date': datetime.now(),
                'herb_name': herb_info['name'],
                'sample_id': herb_info.get('sample_id')
            },
            'identification': {
                'result': auth_results['identification'],
                'confidence': auth_results['identification']['confidence']
            },
            'authentication': {
                'verdict': auth_results['authentication']['verdict'],
                'confidence': auth_results['authentication']['confidence'],
                'evidence': auth_results['authentication']['evidence']
            },
            'quality': {
                'grade': auth_results['quality']['grade'],
                'score': auth_results['quality']['score'],
                'details': auth_results['quality']['factors']
            },
            'characteristics': auth_results['characteristics'],
            'images': herb_info['images'],
            'recommendations': auth_results['recommendations'],
            'disclaimer': self.get_disclaimer()
        }

        return report

    def get_disclaimer(self):
        """免责声明"""
        return """
        本报告基于图像AI分析，仅供参考。
        最终鉴别结果应结合实物检验和专业鉴定。
        如有疑问，请咨询专业中药鉴定师。
        """
```

---

## 2. 中药批发市场供应商数据库

### 2.1 系统概述

全面的中药材批发市场和供应商信息平台，包含价格行情、供应商评级和采购管理。

### 2.2 供应商数据结构

```python
class HerbSupplierDatabase:
    """中药供应商数据库"""

    supplier_schema = {
        'basic_info': {
            'id': str,
            'company_name': str,           # 公司名称
            'company_name_en': str,        # 英文名称
            'business_type': str,          # 批发商/种植基地/加工厂
            'registration_no': str,        # 注册号
            'established_year': int,       # 成立年份
            'description': str
        },
        'contact': {
            'address': str,
            'city': str,
            'state': str,
            'country': str,
            'postal_code': str,
            'phone': str,
            'fax': str,
            'email': str,
            'website': str,
            'wechat': str,
            'whatsapp': str
        },
        'business': {
            'main_products': list,         # 主营产品
            'product_categories': list,    # 产品分类
            'annual_revenue': str,         # 年营业额
            'export_markets': list,        # 出口市场
            'certifications': list,        # 认证
            'production_capacity': str     # 产能
        },
        'quality': {
            'rating': float,               # 评分 (1-5)
            'reviews_count': int,          # 评价数
            'response_rate': float,        # 回复率
            'delivery_rate': float,        # 准时交货率
            'quality_pass_rate': float,    # 质量合格率
            'verified': bool               # 是否认证
        },
        'compliance': {
            'gmp_certified': bool,         # GMP认证
            'gap_certified': bool,         # GAP认证
            'iso_certified': bool,         # ISO认证
            'halal_certified': bool,       # 清真认证
            'organic_certified': bool,     # 有机认证
            'licenses': list               # 经营许可证
        }
    }

    # 主要中药材市场
    major_markets = {
        '中国': [
            {
                'name': '亳州中药材市场',
                'location': '安徽亳州',
                'specialty': '全国最大中药材集散中心',
                'annual_volume': '约1000亿元'
            },
            {
                'name': '安国中药材市场',
                'location': '河北安国',
                'specialty': '千年药都',
                'annual_volume': '约300亿元'
            },
            {
                'name': '玉林中药材市场',
                'location': '广西玉林',
                'specialty': '南方药都',
                'annual_volume': '约200亿元'
            },
            {
                'name': '成都荷花池',
                'location': '四川成都',
                'specialty': '西南药材集散中心'
            }
        ],
        '马来西亚': [
            {
                'name': '吉隆坡中药批发市场',
                'location': 'Kuala Lumpur',
                'areas': ['Petaling Street', 'Pudu']
            },
            {
                'name': '槟城中药市场',
                'location': 'Penang',
                'specialty': '历史悠久的中药集散地'
            }
        ]
    }
```

### 2.3 价格行情系统

```python
class HerbPriceSystem:
    """中药材价格行情系统"""

    def __init__(self):
        self.price_sources = [
            'major_markets',      # 主要市场报价
            'supplier_quotes',    # 供应商报价
            'industry_reports'    # 行业报告
        ]

    price_schema = {
        'herb_id': str,
        'herb_name': str,
        'specification': str,      # 规格
        'origin': str,             # 产地
        'grade': str,              # 等级
        'unit': str,               # 单位 (kg, 500g, etc.)
        'price': {
            'current': float,      # 当前价
            'low': float,          # 最低价
            'high': float,         # 最高价
            'average': float       # 平均价
        },
        'trend': {
            'daily_change': float,      # 日涨跌
            'weekly_change': float,     # 周涨跌
            'monthly_change': float,    # 月涨跌
            'yearly_change': float      # 年涨跌
        },
        'market': str,             # 市场
        'updated_at': datetime
    }

    def get_price(self, herb_id, specification=None, origin=None):
        """获取价格"""
        query = {'herb_id': herb_id}
        if specification:
            query['specification'] = specification
        if origin:
            query['origin'] = origin

        prices = self.db.find_prices(query)

        return {
            'herb_id': herb_id,
            'prices': prices,
            'analysis': self.analyze_price_trend(prices),
            'recommendations': self.price_recommendations(prices)
        }

    def analyze_price_trend(self, prices):
        """分析价格趋势"""
        return {
            'trend': self.calculate_trend(prices),
            'volatility': self.calculate_volatility(prices),
            'seasonal_pattern': self.detect_seasonality(prices),
            'forecast': self.forecast_price(prices)
        }

    def compare_suppliers(self, herb_id, quantity):
        """比较供应商价格"""
        suppliers = self.get_suppliers_for_herb(herb_id)

        comparisons = []
        for supplier in suppliers:
            quote = self.get_supplier_quote(supplier['id'], herb_id, quantity)
            comparisons.append({
                'supplier': supplier,
                'quote': quote,
                'total_cost': self.calculate_total_cost(quote, quantity),
                'delivery_time': quote['delivery_time'],
                'rating': supplier['quality']['rating']
            })

        # 按综合评分排序
        return sorted(comparisons, key=lambda x: self.calculate_score(x), reverse=True)

    # 价格示例数据
    sample_prices = {
        '人参': {
            '生晒参': {
                '特级': {'price': 2500, 'unit': 'kg', 'origin': '吉林'},
                '一级': {'price': 1800, 'unit': 'kg', 'origin': '吉林'},
                '二级': {'price': 1200, 'unit': 'kg', 'origin': '吉林'}
            },
            '红参': {
                '特级': {'price': 3000, 'unit': 'kg', 'origin': '吉林'},
                '一级': {'price': 2200, 'unit': 'kg', 'origin': '吉林'}
            }
        },
        '黄芪': {
            '甘肃统片': {'price': 45, 'unit': 'kg'},
            '内蒙统片': {'price': 38, 'unit': 'kg'},
            '特级片': {'price': 65, 'unit': 'kg'}
        },
        '当归': {
            '岷县头': {'price': 85, 'unit': 'kg'},
            '岷县全归': {'price': 55, 'unit': 'kg'},
            '云南全归': {'price': 40, 'unit': 'kg'}
        }
    }
```

### 2.4 采购管理

```python
class ProcurementSystem:
    """采购管理系统"""

    def create_purchase_order(self, order_info):
        """创建采购订单"""
        order = {
            'order_id': generate_order_id(),
            'supplier_id': order_info['supplier_id'],
            'items': order_info['items'],
            'total_amount': self.calculate_total(order_info['items']),
            'delivery_address': order_info['delivery_address'],
            'expected_delivery': order_info['expected_delivery'],
            'payment_terms': order_info['payment_terms'],
            'status': 'pending',
            'created_at': datetime.now()
        }

        return order

    def track_order(self, order_id):
        """追踪订单"""
        order = self.get_order(order_id)

        return {
            'order': order,
            'status_history': self.get_status_history(order_id),
            'shipping_info': self.get_shipping_info(order_id),
            'estimated_arrival': self.estimate_arrival(order_id)
        }

    def evaluate_supplier(self, supplier_id, order_id, evaluation):
        """评价供应商"""
        return {
            'evaluation_id': generate_uuid(),
            'supplier_id': supplier_id,
            'order_id': order_id,
            'ratings': {
                'product_quality': evaluation['quality'],
                'delivery_time': evaluation['delivery'],
                'packaging': evaluation['packaging'],
                'communication': evaluation['communication'],
                'overall': evaluation['overall']
            },
            'comments': evaluation['comments'],
            'created_at': datetime.now()
        }
```

---

## 3. 中医AI仪器厂商数据库

### 3.1 系统概述

中医医疗AI仪器和设备的厂商信息、产品介绍和应用指南。

### 3.2 仪器分类

```yaml
中医AI仪器分类:

  诊断设备:
    舌诊仪:
      - 标准化舌象采集
      - AI舌诊分析
      - 量化数据输出

    面诊仪:
      - 面部图像采集
      - 五色分析
      - 面部分区分析

    脉诊仪:
      - 脉象采集
      - 脉图分析
      - 脉象识别

    经络检测仪:
      - 穴位电阻测量
      - 经络能量分析
      - 体质评估

    体质辨识仪:
      - 九种体质辨识
      - 健康评估
      - 调养建议

  治疗设备:
    智能针灸仪:
      - 电针治疗
      - 参数智能调节
      - 穴位定位辅助

    艾灸仪:
      - 智能温控
      - 无烟艾灸
      - 多穴位同时治疗

    拔罐仪:
      - 电动负压
      - 压力精确控制
      - 多罐同时操作

    推拿机器人:
      - 手法模拟
      - 力度控制
      - 个性化方案

    中药熏蒸仪:
      - 温度控制
      - 药物雾化
      - 全身/局部熏蒸
```

### 3.3 厂商数据结构

```python
class MedicalDeviceManufacturerDB:
    """医疗器械厂商数据库"""

    manufacturer_schema = {
        'basic_info': {
            'id': str,
            'name': str,
            'name_en': str,
            'country': str,
            'established': int,
            'description': str,
            'specialization': list
        },
        'contact': {
            'headquarters': str,
            'phone': str,
            'email': str,
            'website': str,
            'sales_contacts': list
        },
        'certifications': {
            'iso_13485': bool,
            'ce_mark': bool,
            'fda_cleared': bool,
            'cfda_approved': bool,
            'mda_registered': bool,  # Malaysia
            'other': list
        },
        'products': list,  # 产品列表
        'service': {
            'warranty': str,
            'training': bool,
            'installation': bool,
            'maintenance': bool,
            'technical_support': str
        }
    }

    # 示例厂商数据
    sample_manufacturers = [
        {
            'name': '道生医疗',
            'name_en': 'Daosheng Medical',
            'country': '中国',
            'specialization': ['舌诊仪', '面诊仪', '脉诊仪'],
            'products': [
                {
                    'name': 'DS-01舌面诊仪',
                    'type': '舌诊仪',
                    'features': [
                        '标准化D65光源',
                        'AI舌象分析',
                        '量化数据输出',
                        '历史对比功能'
                    ],
                    'price_range': 'RM 15,000 - 25,000',
                    'certifications': ['CFDA', 'CE']
                }
            ]
        },
        {
            'name': '上工医信',
            'name_en': 'Shanggong Medical',
            'country': '中国',
            'specialization': ['四诊合参系统', '中医AI诊断'],
            'products': [
                {
                    'name': '中医四诊合参系统',
                    'type': '综合诊断系统',
                    'features': [
                        '望闻问切四诊合参',
                        'AI辨证论治',
                        '处方推荐',
                        '健康管理'
                    ]
                }
            ]
        },
        {
            'name': '天中依脉',
            'name_en': 'Tianzhong Yimai',
            'country': '中国',
            'specialization': ['脉诊仪'],
            'products': [
                {
                    'name': 'YM-III脉象仪',
                    'type': '脉诊仪',
                    'features': [
                        '三通道脉象采集',
                        '28种脉象识别',
                        '脉图分析',
                        '数据存储管理'
                    ]
                }
            ]
        }
    ]
```

### 3.4 产品详细信息

```python
class MedicalDeviceProduct:
    """医疗设备产品"""

    product_schema = {
        'basic_info': {
            'id': str,
            'name': str,
            'model': str,
            'manufacturer_id': str,
            'category': str,
            'subcategory': str,
            'description': str
        },
        'specifications': {
            'dimensions': str,
            'weight': str,
            'power': str,
            'display': str,
            'connectivity': list,
            'os': str,
            'storage': str
        },
        'features': {
            'main_functions': list,
            'ai_capabilities': list,
            'software_features': list,
            'integration': list
        },
        'clinical': {
            'applications': list,
            'accuracy': str,
            'clinical_validation': str,
            'user_requirements': str
        },
        'regulatory': {
            'certifications': list,
            'registration_numbers': dict,
            'classification': str
        },
        'commercial': {
            'price_range': str,
            'warranty': str,
            'consumables': list,
            'training_included': bool
        },
        'media': {
            'images': list,
            'videos': list,
            'brochure': str,
            'manual': str
        }
    }
```

### 3.5 设备比较系统

```python
class DeviceComparisonSystem:
    """设备比较系统"""

    def compare_devices(self, device_ids):
        """比较多个设备"""
        devices = [self.get_device(id) for id in device_ids]

        comparison = {
            'devices': devices,
            'comparison_table': self.create_comparison_table(devices),
            'pros_cons': self.analyze_pros_cons(devices),
            'recommendation': self.generate_recommendation(devices)
        }

        return comparison

    def create_comparison_table(self, devices):
        """创建比较表"""
        aspects = [
            'price', 'features', 'accuracy',
            'certifications', 'support', 'user_reviews'
        ]

        table = {}
        for aspect in aspects:
            table[aspect] = {
                device['name']: self.get_aspect_value(device, aspect)
                for device in devices
            }

        return table

    def find_suitable_device(self, requirements):
        """根据需求查找设备"""
        all_devices = self.get_all_devices()

        # 筛选符合要求的设备
        suitable = []
        for device in all_devices:
            if self.meets_requirements(device, requirements):
                score = self.calculate_match_score(device, requirements)
                suitable.append({
                    'device': device,
                    'match_score': score
                })

        # 按匹配度排序
        return sorted(suitable, key=lambda x: x['match_score'], reverse=True)
```

---

## 4. 中成药批发商供应系统

### 4.1 系统概述

中成药批发商信息和供应管理系统，包含产品目录、价格和订购功能。

### 4.2 中成药数据结构

```python
class PatentMedicineDatabase:
    """中成药数据库"""

    medicine_schema = {
        'basic_info': {
            'id': str,
            'name': str,                    # 药品名称
            'pinyin': str,                  # 拼音
            'english_name': str,            # 英文名
            'manufacturer': str,            # 生产厂家
            'approval_number': str,         # 批准文号
            'otc_rx': str                   # OTC/Rx
        },
        'composition': {
            'ingredients': list,            # 成分
            'specification': str,           # 规格
            'dosage_form': str              # 剂型
        },
        'clinical': {
            'functions': str,               # 功能主治
            'indications': list,            # 适应症
            'dosage': str,                  # 用法用量
            'contraindications': list,      # 禁忌
            'precautions': list,            # 注意事项
            'interactions': list,           # 相互作用
            'adverse_reactions': list       # 不良反应
        },
        'storage': {
            'conditions': str,              # 储存条件
            'shelf_life': str,              # 保质期
            'packaging': str                # 包装
        },
        'regulatory': {
            'malaysia_registration': str,   # 马来西亚注册号
            'china_approval': str,          # 中国批准文号
            'gmp_certified': bool
        }
    }

    # 中成药分类
    categories = {
        '解表剂': ['感冒灵', '银翘片', '藿香正气'],
        '清热剂': ['牛黄解毒片', '板蓝根颗粒', '双黄连'],
        '泻下剂': ['麻仁丸', '通便灵'],
        '祛湿剂': ['二妙丸', '四妙丸', '茵陈五苓丸'],
        '温里剂': ['附子理中丸', '良附丸'],
        '理气剂': ['越鞠丸', '木香顺气丸'],
        '理血剂': ['血府逐瘀胶囊', '复方丹参片'],
        '补益剂': ['六味地黄丸', '补中益气丸', '归脾丸'],
        '安神剂': ['天王补心丹', '柏子养心丸'],
        '开窍剂': ['安宫牛黄丸', '苏合香丸'],
        '固涩剂': ['金锁固精丸', '缩泉丸'],
        '消导剂': ['保和丸', '健胃消食片'],
        '祛痰剂': ['二陈丸', '半夏天麻丸'],
        '治风剂': ['天麻丸', '大活络丸'],
        '外用剂': ['云南白药', '跌打万花油']
    }
```

### 4.3 批发商数据

```python
class PatentMedicineSupplier:
    """中成药批发商"""

    supplier_schema = {
        'basic_info': {
            'id': str,
            'company_name': str,
            'business_license': str,
            'gsp_certified': bool,          # GSP认证
            'established': int
        },
        'contact': {
            'address': str,
            'phone': str,
            'email': str,
            'sales_rep': list
        },
        'products': {
            'brands': list,                 # 代理品牌
            'categories': list,             # 经营类别
            'total_products': int
        },
        'service': {
            'min_order': str,               # 最小订货量
            'delivery_time': str,           # 发货时间
            'payment_terms': list,          # 付款方式
            'return_policy': str            # 退货政策
        },
        'quality': {
            'rating': float,
            'reviews': int,
            'verified': bool
        }
    }

    # 马来西亚主要中成药批发商
    malaysia_suppliers = [
        {
            'name': 'Eu Yan Sang',
            'type': '连锁中药店/批发',
            'brands': ['余仁生'],
            'locations': ['全马各州'],
            'specialty': '传统中成药、保健品'
        },
        {
            'name': 'Hai-O Enterprise',
            'type': '批发/零售',
            'brands': ['海鸥'],
            'specialty': '中成药、保健品'
        },
        {
            'name': 'Salim Trading',
            'type': '批发',
            'location': 'Kuala Lumpur',
            'specialty': '中国进口中成药'
        }
    ]
```

### 4.4 价格和订购

```python
class PatentMedicineOrdering:
    """中成药订购系统"""

    def get_price_list(self, supplier_id, category=None):
        """获取价格表"""
        prices = self.db.get_supplier_prices(supplier_id)

        if category:
            prices = [p for p in prices if p['category'] == category]

        return {
            'supplier_id': supplier_id,
            'prices': prices,
            'updated_at': self.get_last_update(supplier_id),
            'terms': self.get_supplier_terms(supplier_id)
        }

    def create_order(self, order_info):
        """创建订单"""
        order = {
            'order_id': generate_order_id(),
            'supplier_id': order_info['supplier_id'],
            'items': order_info['items'],
            'subtotal': self.calculate_subtotal(order_info['items']),
            'discount': self.apply_discount(order_info),
            'total': self.calculate_total(order_info),
            'delivery': order_info['delivery'],
            'payment': order_info['payment'],
            'status': 'pending',
            'created_at': datetime.now()
        }

        return order

    def check_inventory(self, supplier_id, product_id):
        """检查库存"""
        return self.db.get_inventory(supplier_id, product_id)
```

---

## 5. OCR文字识别与翻译系统

### 5.1 系统概述

智能OCR系统，支持手写和印刷文字识别，并提供多语言自动翻译功能。

### 5.2 OCR引擎

```python
class MedicalOCREngine:
    """医疗OCR引擎"""

    def __init__(self):
        self.engines = {
            'printed': PrintedTextOCR(),
            'handwritten': HandwrittenOCR(),
            'mixed': MixedTextOCR()
        }
        self.medical_nlp = MedicalNLPProcessor()

    def recognize(self, image, text_type='auto'):
        """识别文字"""
        # 自动检测文字类型
        if text_type == 'auto':
            text_type = self.detect_text_type(image)

        # 选择OCR引擎
        engine = self.engines.get(text_type, self.engines['mixed'])

        # 识别文字
        raw_text = engine.recognize(image)

        # 后处理
        processed = self.post_process(raw_text)

        # 医学术语处理
        enhanced = self.medical_nlp.enhance(processed)

        return {
            'raw_text': raw_text,
            'processed_text': processed,
            'enhanced_text': enhanced,
            'confidence': engine.get_confidence(),
            'detected_language': self.detect_language(processed),
            'medical_terms': self.extract_medical_terms(enhanced)
        }

    def recognize_prescription(self, image):
        """识别处方"""
        # OCR识别
        ocr_result = self.recognize(image)

        # 处方结构化
        structured = self.structure_prescription(ocr_result['enhanced_text'])

        return {
            'raw_ocr': ocr_result,
            'structured': {
                'patient_info': structured.get('patient'),
                'diagnosis': structured.get('diagnosis'),
                'medications': structured.get('medications'),
                'instructions': structured.get('instructions'),
                'doctor_info': structured.get('doctor')
            }
        }

    def recognize_lab_report(self, image):
        """识别化验报告"""
        ocr_result = self.recognize(image)

        # 表格识别
        tables = self.recognize_tables(image)

        # 结构化结果
        structured = self.structure_lab_report(ocr_result, tables)

        return {
            'raw_ocr': ocr_result,
            'tables': tables,
            'structured_results': structured
        }

class HandwrittenOCR:
    """手写文字OCR"""

    def __init__(self):
        self.model = load_handwriting_model()
        self.char_recognizer = ChineseCharRecognizer()

    def recognize(self, image):
        """识别手写文字"""
        # 预处理
        processed = self.preprocess(image)

        # 行检测
        lines = self.detect_lines(processed)

        # 字符分割
        chars = self.segment_characters(lines)

        # 字符识别
        recognized = []
        for char in chars:
            result = self.char_recognizer.recognize(char)
            recognized.append(result)

        return self.combine_results(recognized)

    def preprocess(self, image):
        """预处理"""
        # 二值化
        binary = self.binarize(image)
        # 去噪
        denoised = self.denoise(binary)
        # 倾斜校正
        corrected = self.deskew(denoised)
        return corrected

    # 支持的手写类型
    supported_scripts = [
        '简体中文',
        '繁体中文',
        '英文',
        '马来文',
        '数字',
        '医学符号'
    ]
```

### 5.3 多语言翻译系统

```python
class MedicalTranslationEngine:
    """医学翻译引擎"""

    def __init__(self):
        self.translation_model = MedicalNMTModel()
        self.medical_dictionary = MedicalDictionary()

    # 支持的语言
    supported_languages = {
        'zh-CN': '简体中文',
        'zh-TW': '繁体中文',
        'en': 'English',
        'ms': 'Bahasa Malaysia',
        'ta': 'Tamil',
        'hi': 'Hindi'
    }

    def translate(self, text, source_lang, target_lang):
        """翻译文本"""
        # 检测医学术语
        terms = self.extract_medical_terms(text, source_lang)

        # 翻译医学术语
        translated_terms = self.translate_terms(terms, source_lang, target_lang)

        # 翻译全文
        translated = self.translation_model.translate(
            text, source_lang, target_lang
        )

        # 后处理：确保医学术语准确
        final = self.post_process_translation(translated, translated_terms)

        return {
            'original': text,
            'translated': final,
            'source_language': source_lang,
            'target_language': target_lang,
            'medical_terms': translated_terms,
            'confidence': self.calculate_confidence(translated)
        }

    def translate_terms(self, terms, source_lang, target_lang):
        """翻译医学术语"""
        translations = []

        for term in terms:
            # 查询医学词典
            dict_result = self.medical_dictionary.lookup(
                term, source_lang, target_lang
            )

            if dict_result:
                translations.append({
                    'original': term,
                    'translation': dict_result['translation'],
                    'source': 'dictionary',
                    'confidence': 1.0
                })
            else:
                # 使用NMT翻译
                nmt_result = self.translation_model.translate_term(
                    term, source_lang, target_lang
                )
                translations.append({
                    'original': term,
                    'translation': nmt_result,
                    'source': 'nmt',
                    'confidence': 0.8
                })

        return translations

    def auto_translate(self, text, target_lang):
        """自动检测语言并翻译"""
        # 检测源语言
        source_lang = self.detect_language(text)

        # 翻译
        return self.translate(text, source_lang, target_lang)

    def batch_translate(self, texts, target_lang):
        """批量翻译"""
        results = []
        for text in texts:
            result = self.auto_translate(text, target_lang)
            results.append(result)
        return results

class MedicalDictionary:
    """医学词典"""

    def __init__(self):
        self.dictionaries = {
            'tcm': TCMDictionary(),           # 中医词典
            'western': WesternMedDict(),      # 西医词典
            'herb': HerbDictionary(),         # 中药词典
            'acupoint': AcupointDictionary()  # 穴位词典
        }

    def lookup(self, term, source_lang, target_lang):
        """查询术语"""
        for dict_name, dictionary in self.dictionaries.items():
            result = dictionary.lookup(term, source_lang, target_lang)
            if result:
                return {
                    'translation': result['translation'],
                    'pinyin': result.get('pinyin'),
                    'definition': result.get('definition'),
                    'category': dict_name
                }
        return None
```

### 5.4 OCR与翻译集成

```python
class OCRTranslationIntegration:
    """OCR与翻译集成"""

    def __init__(self):
        self.ocr = MedicalOCREngine()
        self.translator = MedicalTranslationEngine()

    def recognize_and_translate(self, image, target_lang):
        """识别并翻译"""
        # OCR识别
        ocr_result = self.ocr.recognize(image)

        # 检测语言
        source_lang = ocr_result['detected_language']

        # 如果需要翻译
        if source_lang != target_lang:
            translation = self.translator.translate(
                ocr_result['enhanced_text'],
                source_lang,
                target_lang
            )
        else:
            translation = None

        return {
            'ocr_result': ocr_result,
            'translation': translation,
            'source_language': source_lang,
            'target_language': target_lang
        }

    def process_document(self, images, target_lang):
        """处理多页文档"""
        results = []

        for i, image in enumerate(images):
            result = self.recognize_and_translate(image, target_lang)
            result['page'] = i + 1
            results.append(result)

        return {
            'pages': results,
            'combined_text': self.combine_pages(results),
            'combined_translation': self.combine_translations(results)
        }
```

---

## 6. QR码与身份证病人查询系统

### 6.1 系统概述

快速病人识别系统，支持QR码扫描和身份证查询，快速访问病历。

### 6.2 QR码系统

```python
class PatientQRSystem:
    """病人QR码系统"""

    def generate_patient_qr(self, patient_id):
        """生成病人QR码"""
        # 创建QR数据
        qr_data = {
            'type': 'patient',
            'patient_id': patient_id,
            'clinic_id': self.clinic_id,
            'generated_at': datetime.now().isoformat(),
            'checksum': self.generate_checksum(patient_id)
        }

        # 加密数据
        encrypted = self.encrypt_qr_data(qr_data)

        # 生成QR码
        qr_image = self.create_qr_image(encrypted)

        return {
            'qr_image': qr_image,
            'qr_data': qr_data,
            'expires_at': None  # 永久有效或设置过期时间
        }

    def scan_patient_qr(self, qr_image):
        """扫描病人QR码"""
        # 解码QR码
        decoded = self.decode_qr(qr_image)

        if not decoded:
            return {'success': False, 'error': 'QR码无法识别'}

        # 解密数据
        qr_data = self.decrypt_qr_data(decoded)

        # 验证数据
        if not self.verify_qr_data(qr_data):
            return {'success': False, 'error': 'QR码验证失败'}

        # 获取病人信息
        patient = self.get_patient(qr_data['patient_id'])

        if not patient:
            return {'success': False, 'error': '病人不存在'}

        return {
            'success': True,
            'patient': patient,
            'quick_actions': self.get_quick_actions(patient)
        }

    def get_quick_actions(self, patient):
        """获取快捷操作"""
        return [
            {
                'action': 'view_record',
                'label': '查看病历',
                'url': f'/patients/{patient["id"]}/records'
            },
            {
                'action': 'new_visit',
                'label': '新建就诊',
                'url': f'/patients/{patient["id"]}/visits/new'
            },
            {
                'action': 'view_history',
                'label': '历史记录',
                'url': f'/patients/{patient["id"]}/history'
            },
            {
                'action': 'prescriptions',
                'label': '处方记录',
                'url': f'/patients/{patient["id"]}/prescriptions'
            }
        ]

class QRCodeGenerator:
    """QR码生成器"""

    def create_qr_image(self, data, size='medium'):
        """创建QR码图像"""
        sizes = {
            'small': 200,
            'medium': 300,
            'large': 400
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # 添加诊所Logo
        img = self.add_logo(img)

        return img

    def add_logo(self, qr_image):
        """添加诊所Logo到QR码中心"""
        # 实现Logo叠加
        pass
```

### 6.3 身份证查询系统

```python
class ICSearchSystem:
    """身份证查询系统"""

    def search_by_ic(self, ic_number):
        """通过身份证查询病人"""
        # 支持完整身份证或最后6位数字查询
        if len(ic_number) == 6:
            return self.search_by_ic_last6(ic_number)

        # 验证完整身份证格式
        if not self.validate_ic_format(ic_number):
            return {'success': False, 'error': '身份证格式无效'}

        # 查询病人
        patient = self.db.find_patient_by_ic(ic_number)

    def search_by_ic_last6(self, last6_digits):
        """通过身份证最后6位查询"""
        # 验证格式（6位数字）
        if not re.match(r'^\d{6}$', last6_digits):
            return {'success': False, 'error': '请输入6位数字'}

        # 查询匹配的病人
        patients = self.db.find_patients_by_ic_suffix(last6_digits)

        if len(patients) == 0:
            return {
                'success': True,
                'found': False,
                'message': '未找到匹配的病人'
            }
        elif len(patients) == 1:
            # 只有一个匹配，直接返回
            return {
                'success': True,
                'found': True,
                'patient': patients[0],
                'last_visit': self.get_last_visit(patients[0]['id']),
                'quick_actions': self.get_quick_actions(patients[0])
            }
        else:
            # 多个匹配，返回列表让用户选择
            return {
                'success': True,
                'found': True,
                'multiple': True,
                'patients': [
                    {
                        'id': p['id'],
                        'name': p['name'],
                        'ic_masked': self.mask_ic(p['ic_number']),
                        'phone': self.mask_phone(p.get('phone', '')),
                        'last_visit': self.get_last_visit(p['id'])
                    }
                    for p in patients
                ],
                'message': f'找到 {len(patients)} 个匹配的病人，请选择'
            }

    def mask_phone(self, phone):
        """遮罩电话号码"""
        if len(phone) < 4:
            return phone
        return phone[:-4] + '****'

        if patient:
            return {
                'success': True,
                'found': True,
                'patient': patient,
                'last_visit': self.get_last_visit(patient['id']),
                'quick_actions': self.get_quick_actions(patient)
            }
        else:
            return {
                'success': True,
                'found': False,
                'message': '未找到病人记录',
                'action': {
                    'type': 'create_new',
                    'label': '创建新病人',
                    'prefill': self.extract_ic_info(ic_number)
                }
            }

    def validate_ic_format(self, ic_number):
        """验证身份证格式"""
        # 马来西亚身份证格式: YYMMDD-SS-GGGG
        # YY: 年份, MM: 月份, DD: 日期
        # SS: 州代码, GGGG: 序号

        pattern = r'^\d{6}-\d{2}-\d{4}$'
        return re.match(pattern, ic_number) is not None

    def extract_ic_info(self, ic_number):
        """从身份证提取信息"""
        # 去除连字符
        clean_ic = ic_number.replace('-', '')

        # 提取出生日期
        year = clean_ic[0:2]
        month = clean_ic[2:4]
        day = clean_ic[4:6]

        # 确定世纪
        current_year = datetime.now().year % 100
        if int(year) > current_year:
            full_year = 1900 + int(year)
        else:
            full_year = 2000 + int(year)

        birth_date = f"{full_year}-{month}-{day}"

        # 提取州代码
        state_code = clean_ic[6:8]
        state = self.get_state_name(state_code)

        # 提取性别 (最后一位: 奇数=男, 偶数=女)
        gender = 'male' if int(clean_ic[-1]) % 2 == 1 else 'female'

        return {
            'ic_number': ic_number,
            'birth_date': birth_date,
            'state': state,
            'gender': gender
        }

    def get_state_name(self, code):
        """获取州名称"""
        states = {
            '01': 'Johor',
            '02': 'Kedah',
            '03': 'Kelantan',
            '04': 'Melaka',
            '05': 'Negeri Sembilan',
            '06': 'Pahang',
            '07': 'Pulau Pinang',
            '08': 'Perak',
            '09': 'Perlis',
            '10': 'Selangor',
            '11': 'Terengganu',
            '12': 'Sabah',
            '13': 'Sarawak',
            '14': 'Wilayah Persekutuan KL',
            '15': 'Wilayah Persekutuan Labuan',
            '16': 'Wilayah Persekutuan Putrajaya'
        }
        return states.get(code, 'Unknown')

    def scan_ic_card(self, image):
        """扫描身份证卡片"""
        # OCR识别身份证
        ocr_result = self.ocr.recognize_ic_card(image)

        if ocr_result['success']:
            # 提取身份证号
            ic_number = ocr_result['ic_number']

            # 查询病人
            return self.search_by_ic(ic_number)
        else:
            return {'success': False, 'error': '无法识别身份证'}
```

### 6.4 快速访问界面

```python
class QuickAccessSystem:
    """快速访问系统"""

    def __init__(self):
        self.qr_system = PatientQRSystem()
        self.ic_system = ICSearchSystem()

    def quick_search(self, query):
        """快速搜索"""
        # 判断查询类型
        query_type = self.detect_query_type(query)

        if query_type == 'qr':
            return self.qr_system.scan_patient_qr(query)
        elif query_type == 'ic':
            return self.ic_system.search_by_ic(query)
        elif query_type == 'phone':
            return self.search_by_phone(query)
        elif query_type == 'name':
            return self.search_by_name(query)
        else:
            return self.general_search(query)

    def detect_query_type(self, query):
        """检测查询类型"""
        # QR码数据
        if self.is_qr_data(query):
            return 'qr'

        # 身份证号
        if re.match(r'^\d{6}-\d{2}-\d{4}$', query):
            return 'ic'

        # 电话号码
        if re.match(r'^[\d\-\+]{10,}$', query):
            return 'phone'

        # 姓名
        return 'name'

    def get_patient_dashboard(self, patient_id):
        """获取病人仪表板"""
        patient = self.get_patient(patient_id)

        return {
            'patient': patient,
            'recent_visits': self.get_recent_visits(patient_id, limit=5),
            'current_medications': self.get_current_medications(patient_id),
            'allergies': patient.get('allergies', []),
            'upcoming_appointments': self.get_upcoming_appointments(patient_id),
            'alerts': self.get_patient_alerts(patient_id),
            'quick_actions': [
                {'action': 'new_visit', 'label': '新建就诊'},
                {'action': 'view_records', 'label': '查看病历'},
                {'action': 'prescribe', 'label': '开具处方'},
                {'action': 'print_qr', 'label': '打印QR码'}
            ]
        }
```

### 6.5 病人卡片打印

```python
class PatientCardPrinter:
    """病人卡片打印"""

    def generate_patient_card(self, patient_id):
        """生成病人卡片"""
        patient = self.get_patient(patient_id)
        qr_code = self.qr_system.generate_patient_qr(patient_id)

        card = {
            'front': {
                'clinic_name': self.clinic_info['name'],
                'clinic_logo': self.clinic_info['logo'],
                'patient_name': patient['name'],
                'patient_id': patient['id'],
                'ic_number': self.mask_ic(patient['ic_number']),
                'qr_code': qr_code['qr_image']
            },
            'back': {
                'clinic_address': self.clinic_info['address'],
                'clinic_phone': self.clinic_info['phone'],
                'emergency_contact': patient.get('emergency_contact'),
                'allergies': patient.get('allergies', []),
                'blood_type': patient.get('blood_type'),
                'notes': '请妥善保管此卡'
            }
        }

        return card

    def mask_ic(self, ic_number):
        """遮罩身份证号"""
        # 显示前6位和后4位
        return ic_number[:6] + '-XX-' + ic_number[-4:]

    def print_card(self, patient_id, printer='default'):
        """打印卡片"""
        card = self.generate_patient_card(patient_id)

        # 生成打印格式
        print_data = self.format_for_printing(card)

        # 发送到打印机
        return self.send_to_printer(print_data, printer)
```

---

## 7. 数据库设计

### 7.1 中药鉴别数据库

```sql
-- 中药材参考数据
CREATE TABLE herb_references (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    pinyin VARCHAR(100),
    latin_name VARCHAR(200),
    family VARCHAR(100),
    category VARCHAR(50),
    authentic_features JSONB,
    quality_standards JSONB,
    common_adulterants JSONB,
    differentiation_points JSONB,
    images JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 鉴别记录
CREATE TABLE herb_authentication_records (
    id UUID PRIMARY KEY,
    herb_id UUID REFERENCES herb_references(id),
    sample_id VARCHAR(50),
    image_paths JSONB,
    authentication_result JSONB,
    quality_result JSONB,
    characteristics JSONB,
    confidence DECIMAL(5,4),
    authenticated_by UUID REFERENCES users(id),
    authenticated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 供应商
CREATE TABLE herb_suppliers (
    id UUID PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    business_type VARCHAR(50),
    registration_no VARCHAR(100),
    contact_info JSONB,
    certifications JSONB,
    rating DECIMAL(3,2),
    reviews_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 价格行情
CREATE TABLE herb_prices (
    id UUID PRIMARY KEY,
    herb_id UUID REFERENCES herb_references(id),
    supplier_id UUID REFERENCES herb_suppliers(id),
    specification VARCHAR(100),
    origin VARCHAR(100),
    grade VARCHAR(50),
    price DECIMAL(10,2),
    unit VARCHAR(20),
    market VARCHAR(100),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.2 医疗设备数据库

```sql
-- 设备厂商
CREATE TABLE device_manufacturers (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    country VARCHAR(100),
    contact_info JSONB,
    certifications JSONB,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 设备产品
CREATE TABLE device_products (
    id UUID PRIMARY KEY,
    manufacturer_id UUID REFERENCES device_manufacturers(id),
    name VARCHAR(255) NOT NULL,
    model VARCHAR(100),
    category VARCHAR(100),
    specifications JSONB,
    features JSONB,
    clinical_info JSONB,
    regulatory JSONB,
    price_range VARCHAR(100),
    media JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.3 中成药数据库

```sql
-- 中成药
CREATE TABLE patent_medicines (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pinyin VARCHAR(100),
    manufacturer VARCHAR(255),
    approval_number VARCHAR(100),
    composition JSONB,
    functions TEXT,
    indications JSONB,
    dosage TEXT,
    contraindications JSONB,
    precautions JSONB,
    storage TEXT,
    regulatory JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 中成药供应商
CREATE TABLE patent_medicine_suppliers (
    id UUID PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_info JSONB,
    brands JSONB,
    categories JSONB,
    service_info JSONB,
    rating DECIMAL(3,2),
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.4 病人QR码数据库

```sql
-- 病人QR码
CREATE TABLE patient_qr_codes (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    qr_data TEXT NOT NULL,
    qr_image_path VARCHAR(255),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- QR扫描记录
CREATE TABLE qr_scan_logs (
    id UUID PRIMARY KEY,
    qr_id UUID REFERENCES patient_qr_codes(id),
    scanned_by UUID REFERENCES users(id),
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_info JSONB,
    location VARCHAR(255)
);
```

---

## 8. API接口设计

### 8.1 中药鉴别API

```yaml
中药鉴别API:

  鉴别分析:
    POST /api/herbs/authenticate:
      description: "中药材AI鉴别"
      request:
        multipart/form-data:
          images: files (required)
          herb_name: string (optional)
          sample_id: string (optional)
      response:
        identification: object
        authentication: object
        quality: object
        characteristics: object
        confidence: number

  获取鉴别要点:
    GET /api/herbs/{herb_id}/authentication-points:
      response:
        authentic_features: array
        common_adulterants: array
        quality_standards: object
```

### 8.2 供应商API

```yaml
供应商API:

  搜索供应商:
    GET /api/suppliers/search:
      parameters:
        type: string (herb/patent_medicine)
        product: string
        location: string
        certified: boolean
      response:
        suppliers: array
        total: integer

  获取价格:
    GET /api/herbs/{herb_id}/prices:
      parameters:
        specification: string
        origin: string
      response:
        prices: array
        trend: object
```

### 8.3 OCR翻译API

```yaml
OCR翻译API:

  识别文字:
    POST /api/ocr/recognize:
      request:
        image: file
        type: string (auto/printed/handwritten)
      response:
        text: string
        confidence: number
        language: string

  翻译:
    POST /api/translate:
      request:
        text: string
        source_lang: string (auto)
        target_lang: string
      response:
        translated: string
        medical_terms: array

  识别并翻译:
    POST /api/ocr/recognize-translate:
      request:
        image: file
        target_lang: string
      response:
        ocr_result: object
        translation: object
```

### 8.4 病人查询API

```yaml
病人查询API:

  扫描QR码:
    POST /api/patients/scan-qr:
      request:
        qr_data: string
      response:
        success: boolean
        patient: object
        quick_actions: array

  身份证查询:
    GET /api/patients/search-ic:
      parameters:
        ic_number: string
      response:
        found: boolean
        patient: object

  生成QR码:
    POST /api/patients/{patient_id}/generate-qr:
      response:
        qr_image: string (base64)
        qr_data: object
```

---

## 9. 界面设计

### 9.1 中药鉴别界面

```
┌─────────────────────────────────────────────────────────────────┐
│  中药材AI鉴别系统                                [历史] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────┐  ┌──────────────────────────┐  │
│  │                             │  │  鉴别结果                │  │
│  │    [中药材照片显示]         │  ├──────────────────────────┤  │
│  │                             │  │                          │  │
│  │    [AI标注和特征标记]       │  │  识别: 人参 (95%)        │  │
│  │                             │  │                          │  │
│  └─────────────────────────────┘  │  真伪: ✓ 正品            │  │
│                                   │  置信度: 92%              │  │
│  [拍照] [相册] [多角度]           │                          │  │
│                                   │  品质等级: 一级           │  │
│  ┌─────────────────────────────┐  │  评分: 85/100            │  │
│  │  拍摄提示                   │  │                          │  │
│  │  • 请拍摄整体外观           │  │  特征分析:               │  │
│  │  • 包含表面纹理细节         │  │  • 芦头明显 ✓            │  │
│  │  • 如有断面请拍摄           │  │  • 纹理清晰 ✓            │  │
│  │  • 放置标尺参照             │  │  • 颜色正常 ✓            │  │
│  └─────────────────────────────┘  │  • 质地适中 ✓            │  │
│                                   │                          │  │
│                                   │  常见伪品对比:           │  │
│                                   │  [商陆根] [野豇豆根]     │  │
│                                   └──────────────────────────┘  │
│                                                                 │
│  [生成报告] [查看供应商] [价格行情] [保存记录]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 供应商市场界面

```
┌─────────────────────────────────────────────────────────────────┐
│  中药材供应商市场                                [收藏] [订单]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔍 [搜索药材或供应商                                      ]    │
│                                                                 │
│  [全部] [根茎类] [花类] [果实类] [动物类] [矿物类]               │
│                                                                 │
│  人参 - 价格行情                                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  规格          产地      等级    价格(RM/kg)   涨跌     │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  生晒参        吉林      特级    550          +2.5%    │    │
│  │  生晒参        吉林      一级    420          +1.8%    │    │
│  │  红参          吉林      特级    680          +3.2%    │    │
│  │  高丽参        韩国      天级    1200         -0.5%    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  推荐供应商                                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  供应商        评分    主营产品        最小订量    操作  │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  长白山参业    4.8⭐   人参系列        5kg        [询价] │    │
│  │  亳州德仁堂    4.6⭐   各类中药材      10kg       [询价] │    │
│  │  安国中药城    4.5⭐   批发零售        1kg        [询价] │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  [查看更多供应商] [价格走势图] [批量询价]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 病人快速查询界面

```
┌─────────────────────────────────────────────────────────────────┐
│  快速查询病人                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │           📷 扫描QR码                                   │    │
│  │                                                         │    │
│  │      [相机取景框 - 对准病人QR码]                        │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ─────────────── 或 ───────────────                             │
│                                                                 │
│  身份证号码查询:                                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  [880515-14-5678                                    ] 🔍 │    │
│  └─────────────────────────────────────────────────────────┘    │
│  💡 可输入完整身份证或最后6位数字 (如: 145678)                  │
│                                                                 │
│  快速搜索 (姓名/电话):                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  [                                                  ] 🔍 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  最近访问的病人:                                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  张三      880515-14-****    最后就诊: 2024-01-10       │    │
│  │  李四      750823-07-****    最后就诊: 2024-01-09       │    │
│  │  王五      901205-01-****    最后就诊: 2024-01-08       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

查询结果界面:

┌─────────────────────────────────────────────────────────────────┐
│  病人信息                                        [打印QR] [编辑] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  姓名: 张三                                       │
│  │          │  身份证: 880515-14-5678                           │
│  │  [照片]  │  性别: 男    年龄: 36岁                           │
│  │          │  电话: 012-3456789                                │
│  └──────────┘  地址: Kuala Lumpur                               │
│                                                                 │
│  快捷操作:                                                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │ 新建就诊 │ │ 查看病历 │ │ 开处方  │ │ 预约    │               │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘               │
│                                                                 │
│  最近就诊记录:                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  2024-01-10  主诉: 头痛、失眠    诊断: 肝阳上亢         │    │
│  │  2023-12-28  主诉: 咳嗽、痰多    诊断: 痰湿阻肺         │    │
│  │  2023-12-15  主诉: 腰痛          诊断: 肾虚腰痛         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  过敏史: 青霉素                                                 │
│  当前用药: 天麻丸、六味地黄丸                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.4 OCR翻译界面

```
┌─────────────────────────────────────────────────────────────────┐
│  OCR识别与翻译                                   [历史] [设置]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [拍照识别] [相册导入] [文档扫描]                                │
│                                                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │                         │  │  识别结果                    │  │
│  │   [原始图片/文档]       │  ├──────────────────────────────┤  │
│  │                         │  │                              │  │
│  │   [文字区域标注]        │  │  患者姓名：张三              │  │
│  │                         │  │  诊断：肝阳上亢              │  │
│  └─────────────────────────┘  │  处方：                      │  │
│                               │    天麻钩藤饮加减            │  │
│  检测语言: 中文               │    天麻 10g                  │  │
│  置信度: 95%                  │    钩藤 15g                  │  │
│                               │    石决明 20g                │  │
│  翻译目标: [English      ▼]  │    ...                       │  │
│                               │                              │  │
│  ┌─────────────────────────┐  └──────────────────────────────┘  │
│  │  翻译结果               │                                    │
│  ├─────────────────────────┤  医学术语:                         │
│  │                         │  ┌──────────────────────────────┐  │
│  │  Patient: Zhang San     │  │ 肝阳上亢                     │  │
│  │  Diagnosis: Liver Yang  │  │ = Liver Yang Rising          │  │
│  │  Rising                 │  │                              │  │
│  │  Prescription:          │  │ 天麻                         │  │
│  │    Tianma Gouteng       │  │ = Gastrodia (Tianma)         │  │
│  │    Decoction Modified   │  └──────────────────────────────┘  │
│  │    ...                  │                                    │
│  └─────────────────────────┘                                    │
│                                                                 │
│  [复制文字] [复制翻译] [导出] [添加到病历]                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. 安全与合规

### 10.1 数据安全

```yaml
安全措施:
  QR码安全:
    - 数据加密
    - 校验和验证
    - 可设置过期时间
    - 扫描日志记录

  身份证处理:
    - 遮罩显示
    - 加密存储
    - 访问控制
    - 审计日志

  供应商数据:
    - 认证验证
    - 评价真实性
    - 价格数据来源标注
```

### 10.2 合规要求

```yaml
PDPA合规:
  - 病人数据最小化
  - 知情同意
  - 数据访问控制
  - 删除权支持

供应商合规:
  - 营业执照验证
  - GMP/GSP认证
  - 产品注册验证
```

---

## 11. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2024 | 初始版本 - 中药鉴别、供应商、OCR、QR查询系统 |

---

**文档结束**
