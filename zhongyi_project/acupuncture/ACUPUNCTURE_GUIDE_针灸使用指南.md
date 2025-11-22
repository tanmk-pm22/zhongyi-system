# 针灸模块使用指南 | Acupuncture Module User Guide

## 概述 | Overview

针灸模块是一个现代化的中医针灸治疗管理系统，集成了AI智能推荐、3D穴位参考库和多种现代针灸技术支持。

The Acupuncture Module is a modern TCM acupuncture treatment management system with AI-powered recommendations, 3D acupoint reference library, and support for modern acupuncture techniques.

---

## 主要功能 | Key Features

### 1. 完整的治疗记录 | Complete Treatment Records
- 患者信息和治疗日期 | Patient information and session dates
- 主诉和中医诊断 | Chief complaints and TCM diagnosis
- 使用的穴位详细记录 | Detailed acupoint usage records
- 治疗技术和手法说明 | Treatment techniques and methods
- 患者反应追踪 | Patient response tracking
- 后续治疗计划 | Follow-up treatment planning

### 2. 现代针灸技术支持 | Modern Acupuncture Techniques
系统支持以下现代针灸方法：
- 传统针灸 | Traditional Acupuncture
- 电针 | Electroacupuncture
- 耳针 | Auricular Acupuncture
- 头针 | Scalp Acupuncture
- 艾灸 | Moxibustion
- 拔罐 | Cupping Therapy
- **激光针灸 | Laser Acupuncture** (新增)
- **磁疗针灸 | Magnetic Acupuncture** (新增)
- **温针灸 | Warming Needle** (新增)
- **火针 | Fire Needling** (新增)
- **刺络放血 | Bloodletting Therapy** (新增)

### 3. AI智能推荐系统 | AI Recommendation System

#### 工作原理 | How it Works
AI系统基于以下信息提供穴位推荐：
1. **主诉分析** | Complaint Analysis
   - 自动识别症状关键词
   - 匹配相应的治疗穴位
   
2. **中医辨证分析** | TCM Pattern Analysis
   - 识别辨证类型
   - 推荐对症穴位组合

#### 支持的症状 | Supported Symptoms
- 头痛、偏头痛 | Headaches, Migraines
- 颈肩疼痛 | Neck and shoulder pain
- 失眠 | Insomnia
- 消化问题 | Digestive issues
- 呼吸系统问题 | Respiratory problems
- 腰痛、膝痛 | Lower back pain, knee pain
- 情绪问题 | Emotional issues
- 妇科问题 | Gynecological issues

#### 支持的辨证类型 | Supported TCM Patterns
- 气滞血瘀 | Qi Stagnation and Blood Stasis
- 肝阳上亢 | Liver Yang Rising
- 肝郁气滞 | Liver Qi Stagnation
- 脾胃虚弱 | Spleen-Stomach Deficiency
- 肾阳虚/肾阴虚 | Kidney Yang/Yin Deficiency
- 心脾两虚 | Heart-Spleen Deficiency
- 痰湿 | Phlegm-Dampness

### 4. 穴位参考库 | Acupoint Reference Library

#### 包含信息 | Information Included
- 穴位编码和名称 | Acupoint codes and names (中文/拼音/English)
- 所属经络 | Meridian classification
- 精确定位 | Precise location
- 2D和3D图片支持 | 2D and 3D image support
- 视频演示链接 | Video demonstration links
- 主治功效 | Indications and functions
- 针刺方法 | Needling techniques
- 注意事项 | Precautions
- 使用统计和有效率 | Usage statistics and effectiveness ratings

---

## 如何使用 | How to Use

### 步骤1：访问针灸模块 | Step 1: Access the Module

#### 方式 A：从导航菜单 | Method A: From Navigation Menu
1. 登录系统
2. 点击顶部导航栏的 "针灸 | Acupuncture"

#### 方式 B：从首页快速访问 | Method B: From Home Page
1. 在首页找到橙色的"针灸治疗 | Acupuncture"卡片
2. 点击进入

### 步骤2：创建新的治疗记录 | Step 2: Create New Session

1. 点击 "新建 | New" 按钮
2. 填写基本信息：
   - 选择患者
   - 选择治疗日期
   - 选择治疗类型

3. 填写诊断信息：
   - 输入主诉（症状）
   - 输入中医诊断

### 步骤3：使用AI推荐（可选）| Step 3: Use AI Recommendations (Optional)

**目前AI推荐功能通过后台管理系统使用**

要获得AI推荐：
1. 在Python shell中使用AI助手：
   ```python
   from acupuncture.ai_helper import AcupointAIHelper
   
   # 获取推荐
   points, confidence, reasoning = AcupointAIHelper.recommend_acupoints(
       chief_complaint="头痛",
       tcm_diagnosis="肝阳上亢"
   )
   
   print(f"推荐穴位: {points}")
   print(f"置信度: {confidence}%")
   print(f"推理依据: {reasoning}")
   ```

### 步骤4：记录治疗详情 | Step 4: Record Treatment Details

1. **使用穴位** | Acupoints Used
   - 输入使用的穴位，用逗号分隔
   - 例如：合谷(LI4), 太冲(LR3), 足三里(ST36)

2. **留针时间** | Retention Time
   - 选择：15分钟、20分钟、30分钟、40分钟

3. **手法说明** | Technique Notes
   - 记录针刺手法、深度、刺激强度等

4. **配合疗法** | Additional Treatments
   - 勾选：艾灸、拔罐、推拿

### 步骤5：记录治疗反应 | Step 5: Record Response

1. 选择患者反应等级：
   - 效果显著 | Excellent
   - 效果良好 | Good  
   - 效果一般 | Fair
   - 效果不佳 | Poor
   - 无明显变化 | No Change

2. 填写治疗备注

### 步骤6：计划后续治疗 | Step 6: Plan Follow-up

1. 设置下次复诊日期
2. 填写治疗计划
3. 输入治疗费用（马币）

### 步骤7：保存 | Step 7: Save

点击 "保存 | Save" 按钮完成记录

---

## 穴位参考库管理 | Acupoint Library Management

### 添加穴位参考 | Adding Acupoint References

通过Django管理后台添加：

1. 访问 `/admin/acupuncture/acupointreference/`
2. 点击 "Add Acupoint Reference"
3. 填写信息：
   - **基本信息**: 编码、中文名、拼音、英文名、经络
   - **定位**: 中英文定位描述
   - **图片**: 上传2D和3D图片
   - **视频**: 添加演示视频URL
   - **临床信息**: 主治、功效、针刺方法、注意事项

### 推荐的穴位图片来源 | Recommended Image Sources

1. **3D穴位图**:
   - Visible Body
   - Complete Anatomy
   - 3D Acupuncture (App)
   
2. **2D穴位图**:
   - WHO Standard Acupuncture Point Locations
   - 中国针灸穴位挂图
   - Open-source medical illustrations

### 视频演示资源 | Video Demonstration Resources

- YouTube: Search "acupuncture point location"
- 中医在线教学平台
- 专业针灸培训视频

---

## 数据统计和分析 | Statistics and Analysis

系统自动追踪：

### 穴位使用统计 | Acupoint Usage Statistics
- 每个穴位的使用次数
- 基于患者反馈的有效率
- 最常用穴位排名

### 治疗效果分析 | Treatment Effectiveness Analysis
- 不同治疗类型的效果对比
- AI推荐采用率
- 患者反应趋势

---

## 最佳实践 | Best Practices

### 1. 详细记录 | Detailed Records
- 尽可能详细记录症状
- 使用标准穴位编码（如LI4, ST36）
- 记录具体的针刺手法

### 2. 使用AI辅助 | Using AI Assistance
- AI推荐仅供参考
- 始终基于临床经验做最终决定
- 记录是否采用了AI建议以改进系统

### 3. 图片和视频 | Images and Videos
- 上传清晰的穴位图片
- 使用3D图片帮助学习
- 链接高质量的演示视频

### 4. 持续学习 | Continuous Learning
- 定期查看统计数据
- 分析哪些穴位最有效
- 根据数据调整治疗方案

---

## 技术支持 | Technical Support

### 常见问题 | FAQ

**Q: AI推荐的置信度是什么意思？**
A: 置信度表示AI对其推荐的信心程度（0-100%）。高置信度意味着症状和穴位的匹配度高。

**Q: 如何添加3D穴位图？**
A: 在管理后台的穴位参考中，上传image_3d字段。支持JPG, PNG格式。

**Q: 系统支持哪些图片格式？**
A: 支持 JPG, PNG, GIF。推荐使用PNG以获得最佳质量。

**Q: 可以批量导入穴位数据吗？**
A: 可以。使用Django的fixtures功能或编写数据导入脚本。

### 联系支持 | Contact Support

如有问题，请联系系统管理员或查看项目文档。

---

## 未来功能计划 | Future Features

- [ ] 交互式3D人体模型穴位选择
- [ ] 实时AI推荐界面集成
- [ ] 穴位定位AR辅助
- [ ] 治疗效果机器学习分析
- [ ] 穴位组合智能优化
- [ ] 多语言穴位名称支持
- [ ] 移动端APP集成

---

**版本 | Version**: 2.0  
**更新日期 | Last Updated**: 2025-01-22  
**作者 | Author**: Zhongyi TCM System Team
