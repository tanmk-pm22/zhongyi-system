# 中成药处方功能使用指南 | Patent Medicine Prescription Guide

## 功能概述 | Overview

系统现已支持在处方中添加现代中成药，包括丸剂、片剂、胶囊、颗粒等多种剂型。

The system now supports adding modern Chinese patent medicines to prescriptions, including pills, tablets, capsules, granules, and other dosage forms.

---

## 主要功能 | Main Features

### 1. 中成药库 | Patent Medicine Library

**访问路径：** 导航菜单 → 药品库 | Medicine Library → 中成药 | Patent Medicines

**功能：**
- 浏览所有中成药
- 按剂型筛选（丸剂、片剂、胶囊等）
- 按处方类型筛选（OTC/处方药）
- 搜索药品名称和生产厂家
- 查看药品详细信息（成分、功能主治、用法用量、价格等）

**Features:**
- Browse all patent medicines
- Filter by dosage form (pills, tablets, capsules, etc.)
- Filter by prescription type (OTC/Rx)
- Search by name and manufacturer
- View detailed information (ingredients, functions, usage, pricing)

---

### 2. 创建处方时添加中成药 | Adding Patent Medicines to New Prescriptions

**步骤：**

1. 选择患者后点击"开具处方 | Create Prescription"
2. 在"中成药 | Patent Medicines"卡片中：
   - 点击"添加中成药 | Add Medicine"
   - 从下拉列表选择中成药
   - 输入数量（盒数）
   - 系统自动计算总价
   - 可修改用法用量（默认使用药品说明书用量）
3. 可同时添加多个中成药
4. 可与草药处方配合使用

**Steps:**

1. After selecting a patient, click "Create Prescription"
2. In the "Patent Medicines" card:
   - Click "Add Medicine"
   - Select patent medicine from dropdown
   - Enter quantity (boxes)
   - System auto-calculates total price
   - Modify usage instructions if needed (defaults to package instructions)
3. Multiple patent medicines can be added
4. Can be used together with herbal formulas

---

### 3. 编辑现有处方 | Editing Existing Prescriptions

**步骤：**

1. 打开处方详情页面
2. 点击"编辑 | Edit"按钮
3. 在"中成药 | Patent Medicines"部分：
   - 现有中成药会预填充
   - 可添加新的中成药
   - 可删除不需要的中成药
   - 可修改数量和用法
4. 点击"保存更改 | Save Changes"

**Steps:**

1. Open prescription detail page
2. Click "Edit" button
3. In the "Patent Medicines" section:
   - Existing medicines are pre-filled
   - Add new medicines
   - Remove unwanted medicines
   - Modify quantity and usage
4. Click "Save Changes"

---

### 4. 查看处方中的中成药 | Viewing Patent Medicines in Prescriptions

**处方详情页面显示：**
- 中成药名称（中英文）
- 剂型（丸剂、片剂等）
- 数量（盒数）
- 用法用量
- 金额小计

**Prescription detail page shows:**
- Medicine name (Chinese/English)
- Dosage form (pills, tablets, etc.)
- Quantity (boxes)
- Usage instructions
- Subtotal amount

---

## 数据库中的中成药 | Available Patent Medicines

系统已预装10种常用中成药：

The system includes 10 common patent medicines:

1. **PM001** - 六味地黄丸 | Liu Wei Di Huang Wan (Pills)
2. **PM002** - 补中益气丸 | Bu Zhong Yi Qi Wan (Pills)
3. **PM003** - 感冒清热颗粒 | Gan Mao Qing Re Ke Li (Granules)
4. **PM004** - 板蓝根颗粒 | Ban Lan Gen Ke Li (Granules)
5. **PM005** - 逍遥丸 | Xiao Yao Wan (Pills)
6. **PM006** - 藿香正气口服液 | Huo Xiang Zheng Qi (Oral Liquid)
7. **PM007** - 云南白药胶囊 | Yun Nan Bai Yao (Capsules)
8. **PM008** - 归脾丸 | Gui Pi Wan (Pills)
9. **PM009** - 金匮肾气丸 | Jin Gui Shen Qi Wan (Pills)
10. **PM010** - 龙胆泻肝丸 | Long Dan Xie Gan Wan (Pills)

---

## AI助手功能 | AI Assistant

AI助手现在能够根据证型推荐合适的中成药：

The AI assistant can now recommend appropriate patent medicines based on syndrome patterns:

- **气虚 | Qi Deficiency** → 补中益气丸、归脾丸
- **血虚 | Blood Deficiency** → 归脾丸
- **阴虚 | Yin Deficiency** → 六味地黄丸
- **阳虚 | Yang Deficiency** → 金匮肾气丸
- **气滞 | Qi Stagnation** → 逍遥丸
- **血瘀 | Blood Stasis** → 云南白药胶囊
- **湿热 | Damp-Heat** → 龙胆泻肝丸
- **风寒 | Wind-Cold** → 感冒清热颗粒

AI推荐会考虑患者年龄，为儿童和老年患者提供特殊用量提示。

AI recommendations consider patient age and provide special dosage notes for children and elderly patients.

---

## 技术说明 | Technical Notes

### 数据模型 | Data Model

**PrescriptionPatentMedicine**
- `prescription` - 关联处方
- `medicine` - 关联中成药
- `quantity` - 数量（盒数/瓶数）
- `dosage_instruction` - 用法用量
- `duration_days` - 疗程天数
- `subtotal` - 小计金额（自动计算）

### URL路由 | URL Routes

- `/prescriptions/patent-medicines/` - 中成药列表
- `/prescriptions/patent-medicines/<id>/` - 中成药详情
- `/prescriptions/create/<patient_id>/` - 创建处方（含中成药）
- `/prescriptions/<id>/edit/` - 编辑处方（含中成药）

---

## 下一步开发计划 | Future Development

1. ✅ 中成药库管理
2. ✅ 处方开具功能
3. ✅ AI推荐功能
4. 🔲 库存管理
5. 🔲 处方打印优化
6. 🔲 统计报表（中成药使用频率）
7. 🔲 批量导入中成药数据

---

## 常见问题 | FAQ

**Q: 可以同时开草药和中成药吗？**
A: 是的，处方同时支持草药和中成药，可以配合使用。

**Q: Can I prescribe both herbs and patent medicines together?**
A: Yes, prescriptions support both herbal formulas and patent medicines simultaneously.

**Q: 如何添加新的中成药到系统？**
A: 通过管理后台(/admin/)的"Patent Medicines"模块添加。

**Q: How to add new patent medicines to the system?**
A: Use the admin panel (/admin/) "Patent Medicines" module.

**Q: 价格是否自动计算？**
A: 是的，选择中成药和输入数量后，系统自动计算小计。

**Q: Are prices calculated automatically?**
A: Yes, subtotals are calculated automatically when you select a medicine and enter quantity.

---

*最后更新：2025-11-21*
*Last Updated: 2025-11-21*
