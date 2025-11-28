# Medical Anatomy Images Directory
# 医学解剖图像目录

## Purpose | 用途

This directory stores real medical anatomy photographs for the Human Anatomy Atlas 2026 Viewer.
此目录存储真实的医学解剖照片，用于人体解剖图谱2026查看器。

## Required Images | 所需图像

Place high-quality medical anatomy photographs here:
请在此处放置高质量的医学解剖照片：

### Surface Anatomy | 表面解剖
- `skin_surface.jpg` - Complete body surface view (front)
  完整身体表面视图（正面）

### Muscular System | 肌肉系统
- `muscles_anterior.jpg` - Anterior (front) muscle anatomy
  前面肌肉解剖
- `muscles_posterior.jpg` - Posterior (back) muscle anatomy
  后面肌肉解剖

### Skeletal System | 骨骼系统
- `skeleton.jpg` - Complete skeleton view
  完整骨骼视图

### TCM Meridians | 中医经络
- `tcm_meridians.jpg` - Traditional Chinese Medicine meridian pathways
  中医经络路径图

## Image Specifications | 图像规格

### Format | 格式
- JPEG (.jpg) or PNG (.png)
- RGB color space

### Resolution | 分辨率
- Minimum: 800x1000 pixels
- Recommended: 1200x1500 pixels or higher
- Aspect ratio: 4:5 (portrait orientation)

### File Size | 文件大小
- Optimized for web: < 500KB per image
- High quality: 85-95% JPEG quality

### Content Requirements | 内容要求
- Medical-grade anatomical photographs
- Clear, well-lit images
- Front-facing human body view
- Professional medical photography
- Appropriate for medical/educational use

## Image Sources | 图像来源

You can obtain medical anatomy images from:
您可以从以下来源获取医学解剖图像：

### Free/Open Source | 免费/开源
1. **Visible Human Project**
   - https://www.nlm.nih.gov/research/visible/visible_human.html
   - High-quality anatomical images

2. **Open-i (NIH)**
   - https://openi.nlm.nih.gov/
   - Medical imaging database

3. **Anatomy Atlases**
   - http://www.anatomyatlases.org/
   - Free anatomical resources

4. **WikiMedia Commons**
   - Medical anatomy category
   - Licensed images available

### Commercial Options | 商业选项
1. **Complete Anatomy by 3D4Medical**
2. **Primal Pictures**
3. **Visible Body**
4. **Biodigital Human**

### Integration with Human Anatomy Atlas 2026 | 与人体解剖图谱2026集成

If you have access to Human Anatomy Atlas 2026:
如果您可以访问人体解剖图谱2026：

1. Export high-resolution images from the atlas
2. Save as JPEG with the specified filenames
3. Place in this directory
4. System will automatically load them

## Current Status | 当前状态

**No real medical images added yet | 尚未添加真实医学图像**

The system currently uses:
系统当前使用：
- ✅ Placeholder anatomical drawings
- ✅ AI-powered acupoint overlay
- ✅ Interactive treatment area selection
- ✅ Bilingual labels (中文 | English)

## Adding Images | 添加图像

### Step 1: Obtain Images | 获取图像
- Use legal, licensed medical photographs
- Ensure proper permissions for medical use
- Follow HIPAA/privacy guidelines if using patient images

### Step 2: Prepare Images | 准备图像
- Resize to recommended dimensions
- Optimize file size
- Name according to convention above

### Step 3: Copy to Directory | 复制到目录
```bash
# Place images in this directory
cp your_images/*.jpg zhongyi_project/static/images/anatomy/
```

### Step 4: Verify | 验证
- Refresh browser (Ctrl+F5)
- Images should load automatically
- Check browser console for confirmation

## Legal Considerations | 法律考虑

⚠ **Important | 重要提示**:

1. **Copyright | 版权**
   - Ensure you have rights to use images
   - Follow license terms for any sourced images

2. **Medical Privacy | 医疗隐私**
   - Patient consent required for clinical photos
   - Remove identifying information (HIPAA compliance)
   - Use de-identified anatomical images when possible

3. **Educational Use | 教育用途**
   - Clearly label system as educational/medical tool
   - Follow medical ethics guidelines
   - Maintain professional standards

## Support | 支持

For questions about:
- Image format: Check file specifications above
- Loading issues: See browser console (F12)
- Integration: Review anatomy-atlas-viewer.js

---

**Version**: 1.0
**Last Updated**: 2025-11-26
**System**: Zhongyi TCM - Human Anatomy Atlas 2026 Viewer
