# 3D人体图解快速使用指南 | 3D Body Viewer Quick Start Guide

## 🎯 功能概述 | Feature Overview

中医系统现已集成交互式3D人体图解，可用于：
- **针灸模块**：选择穴位
- **推拿模块**：选择治疗部位

The TCM system now includes interactive 3D body diagrams for:
- **Acupuncture Module**: Select acupoints
- **Tuina Module**: Select treatment areas

---

## 🔍 如何使用 | How to Use

### 针灸模块 | Acupuncture Module

#### 访问路径 | Access Path
```
主菜单 → 针灸 | Acupuncture → 新建治疗 | New Session
或 | Or
直接访问 | Direct URL: /acupuncture/create/
```

#### 使用步骤 | Steps

1. **查看3D图解 | View 3D Diagram**
   - 页面中部显示3D人体图解
   - 3D body diagram appears in the middle of the page

2. **选择穴位 | Select Acupoints**
   - 点击图中红色穴位标记
   - Click red acupoint markers on the diagram
   - 选中后变为深红色
   - Selected points turn dark red

3. **自动填充 | Auto-Fill**
   - 选中的穴位自动填入"使用穴位"字段
   - Selected acupoints auto-fill "Acupoints Used" field
   - 格式：合谷(LI4), 足三里(ST36)
   - Format: Chinese name(Code), ...

4. **调整视图 | Adjust View**
   - 点击 **正面|Front** / **背面|Back** / **侧面|Side** 按钮切换视角
   - Click view buttons to switch angles
   - 拖动鼠标旋转 | Drag to rotate
   - 滚轮缩放 | Scroll to zoom
   - 点击 🔄 重置视图 | Click 🔄 to reset view

#### 可用穴位 | Available Acupoints

| 穴位代码 | 中文名 | English Name | 位置 |
|---------|--------|--------------|------|
| LI4     | 合谷   | He Gu        | 手部 Hand |
| ST36    | 足三里 | Zu San Li    | 小腿 Lower Leg |
| LR3     | 太冲   | Tai Chong    | 足部 Foot |
| PC6     | 内关   | Nei Guan     | 前臂 Forearm |
| SP6     | 三阴交 | San Yin Jiao | 小腿 Lower Leg |
| GB20    | 风池   | Feng Chi     | 颈部 Neck |
| GV20    | 百会   | Bai Hui      | 头顶 Top of Head |
| HT7     | 神门   | Shen Men     | 手腕 Wrist |
| BL23    | 肾俞   | Shen Shu     | 腰部 Lower Back |
| CV4     | 关元   | Guan Yuan    | 小腹 Lower Abdomen |

---

### 推拿模块 | Tuina Module

#### 访问路径 | Access Path
```
主菜单 → 治疗方法 | Treatments → 推拿治疗 | Tuina → 新建 | New
或 | Or
直接访问 | Direct URL: /tuina/new/
```

#### 使用步骤 | Steps

1. **查看3D图解 | View 3D Diagram**
   - 页面中部显示3D人体图解
   - 3D body diagram appears in the middle of the page

2. **选择治疗部位 | Select Treatment Areas**
   - 点击图中绿色治疗区域
   - Click green treatment areas on the diagram
   - 选中后变为深绿色
   - Selected areas turn dark green

3. **自动填充 | Auto-Fill**
   - 选中的部位自动填入"治疗重点"字段
   - Selected areas auto-fill "Primary Focus" field
   - 格式：颈椎、肩部、腰部
   - Format: Neck, Shoulder, Lower Back (in Chinese)

4. **调整视图 | Adjust View**
   - 同针灸模块 | Same as acupuncture module
   - 点击视图按钮、拖动、缩放
   - Click view buttons, drag, zoom

#### 可用治疗部位 | Available Treatment Areas

| 部位代码    | 中文名  | English Name | 前/后视图 |
|------------|---------|--------------|----------|
| neck       | 颈椎    | Neck         | 前/后 Both |
| shoulder   | 肩部    | Shoulder     | 前/后 Both |
| upper_back | 上背部  | Upper Back   | 后 Back |
| lower_back | 腰部    | Lower Back   | 后 Back |
| hip        | 臀部    | Hip          | 后 Back |
| leg        | 下肢    | Leg          | 前/后 Both |
| arm        | 上肢    | Arm          | 前/后 Both |

---

## ⌨️ 快捷操作 | Keyboard Shortcuts

| 操作 | 方法 |
|------|------|
| 旋转视图 | 按住左键拖动 | Rotate View | Hold left mouse and drag |
| 缩放 | 滚轮上下 | Zoom | Mouse wheel up/down |
| 重置视图 | 点击🔄按钮 | Reset View | Click 🔄 button |
| 前视图 | 点击"正面" | Front View | Click "Front" |
| 后视图 | 点击"背面" | Back View | Click "Back" |
| 侧视图 | 点击"侧面" | Side View | Click "Side" |

---

## 📱 移动端使用 | Mobile Usage

- ✅ 支持触摸拖动 | Touch drag supported
- ✅ 支持双指缩放 | Pinch to zoom supported
- ✅ 响应式布局 | Responsive layout
- ✅ 点击选择穴位/部位 | Tap to select points/areas

---

## 🎨 视觉指南 | Visual Guide

### 针灸模式 | Acupuncture Mode
```
🔴 红色圆点 = 穴位标记
🔴 深红色 = 已选中的穴位
```

### 推拿模式 | Tuina Mode
```
🟢 绿色区域 = 治疗部位
🟢 深绿色 = 已选中的部位
```

---

## ❓ 常见问题 | FAQ

### Q1: 看不到3D图解？
**A:** 检查浏览器是否支持Canvas。建议使用Chrome、Firefox或Edge最新版本。

### Q2: 如何取消选择？
**A:** 再次点击已选中的穴位或部位即可取消。

### Q3: 可以选择多个穴位/部位吗？
**A:** 可以！点击多个位置，所有选中的项目会以逗号分隔自动填入表单。

### Q4: 3D图解是否保存选择？
**A:** 是的！编辑已有记录时，之前选择的穴位/部位会自动高亮显示。

### Q5: 图解太小/太大？
**A:** 使用🔍+和🔍-按钮调整缩放，或使用滚轮缩放。

---

## 🔧 技术支持 | Technical Support

### 浏览器要求 | Browser Requirements
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ✅ 移动浏览器 | Mobile browsers

### 性能建议 | Performance Tips
- 关闭其他标签页以获得最佳性能
- 建议屏幕分辨率 ≥ 1280x720
- 确保浏览器硬件加速已启用

---

## 📚 更多资源 | More Resources

- **完整实施文档**: `3D_VIEWER_IMPLEMENTATION_SUMMARY.md`
- **测试脚本**: `zhongyi_project/test_3d_viewer.py`
- **源代码**: `zhongyi_project/static/js/body-3d-viewer.js`

---

## ✅ 系统状态 | System Status

- ✅ 针灸模块3D图解：已启用 | Acupuncture 3D: Enabled
- ✅ 推拿模块3D图解：已启用 | Tuina 3D: Enabled
- ✅ 所有测试：通过 | All Tests: Passed
- ✅ 系统检查：无错误 | System Check: No Errors

---

**🎉 开始使用3D人体图解，提升中医诊疗体验！**

**🎉 Start using 3D body diagrams to enhance your TCM practice!**
