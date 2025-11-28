# Real Medical Photo 3D Viewer System | 真实医学照片3D查看器系统

## Overview | 概述

This document describes the real medical photograph texture system integrated into the zhongyi TCM system's 3D anatomical viewer. The system supports loading actual medical photography files as textures on the 3D human body model for acupuncture and tuina modules.

本文档描述了集成到中医系统3D解剖查看器的真实医学照片纹理系统。该系统支持加载真实的医学照片文件作为3D人体模型的纹理，用于针灸和推拿模块。

## System Architecture | 系统架构

### Components | 组件

1. **Body3DViewerRealPhoto Class** (`body-3d-viewer-realphoto.js`)
   - Main 3D viewer class with real photo texture loading capabilities
   - 主3D查看器类，具有真实照片纹理加载功能

2. **Template Integration**
   - Acupuncture session form: `templates/acupuncture/acupuncturesession_form.html`
   - Tuina session form: `templates/tuina/session_form.html`
   - 针灸治疗表单 和 推拿治疗表单

3. **Medical Photo Directory**
   - Location: `/static/textures/medical/`
   - 位置：`/static/textures/medical/`

## File Structure | 文件结构

```
zhongyi_project/
├── static/
│   ├── js/
│   │   └── body-3d-viewer-realphoto.js    # Main 3D viewer with photo loading
│   └── textures/
│       └── medical/                        # Medical photo directory
│           ├── head_front.jpg              # Head frontal view
│           ├── torso_front.jpg             # Torso frontal view
│           ├── back.jpg                    # Back view
│           ├── arm_left.jpg                # Left arm
│           ├── arm_right.jpg               # Right arm
│           ├── leg_left.jpg                # Left leg
│           └── leg_right.jpg               # Right leg
└── templates/
    ├── acupuncture/
    │   └── acupuncturesession_form.html    # Uses real photo viewer
    └── tuina/
        └── session_form.html               # Uses real photo viewer
```

## Medical Photo Requirements | 医学照片要求

### Image Specifications | 图像规格

- **Format | 格式**: JPEG (.jpg) or PNG (.png) recommended
- **Resolution | 分辨率**: Minimum 1024x1024 pixels (recommended 2048x2048 or higher for best quality)
- **Color Space | 色彩空间**: RGB
- **File Size | 文件大小**: Optimized for web (< 2MB per image recommended)

### Photo Types Needed | 所需照片类型

| Body Part | Filename | View | Description |
|-----------|----------|------|-------------|
| 头部 Head | `head_front.jpg` | Frontal | Front view of head and face |
| 躯干 Torso | `torso_front.jpg` | Frontal | Chest and abdomen front view |
| 背部 Back | `back.jpg` | Posterior | Back view of torso |
| 左臂 Left Arm | `arm_left.jpg` | Lateral | Left arm full view |
| 右臂 Right Arm | `arm_right.jpg` | Lateral | Right arm full view |
| 左腿 Left Leg | `leg_left.jpg` | Anterior | Left leg full view |
| 右腿 Right Leg | `leg_right.jpg` | Anterior | Right leg full view |

### Optional Additional Photos | 可选的额外照片

You can add more detailed photos for specific anatomical regions:

- `neck.jpg` - Neck region | 颈部
- `shoulder_left.jpg` - Left shoulder | 左肩
- `shoulder_right.jpg` - Right shoulder | 右肩
- `hand_left.jpg` - Left hand | 左手
- `hand_right.jpg` - Right hand | 右手
- `foot_left.jpg` - Left foot | 左脚
- `foot_right.jpg` - Right foot | 右脚

## Usage | 使用方法

### 1. Initialize Viewer | 初始化查看器

The viewer is automatically initialized in the acupuncture and tuina templates:

```javascript
const viewer = new Body3DViewerRealPhoto('acupointViewer', {
    showAcupoints: true,
    showMuscles: true,
    showMeridians: true,
    photoMode: 'real',
    textureQuality: 'ultra',
    selectedPoints: selectedPoints
});
```

### 2. Load Standard Medical Photos | 加载标准医学照片

To automatically load all standard medical photos (if they exist):

```javascript
// This will attempt to load all standard photos from /static/textures/medical/
viewer.loadStandardMedicalPhotos();
```

### 3. Load Custom Medical Photo | 加载自定义医学照片

To load a specific medical photo for a specific body part:

```javascript
// Load a custom photo
viewer.loadMedicalPhoto('/static/textures/medical/custom_photo.jpg', 'head');

// Parameters:
// - photoPath: Full path to the medical photo file
// - bodyPart: Body part identifier ('head', 'torso', 'back', 'arm_left', etc.)
```

### 4. Fallback Behavior | 回退行为

If medical photo files are not found, the system automatically uses **ultra-realistic procedural textures** as fallback:

- 1024x1024 resolution skin texture with 15,000+ detail points
- Realistic pores, veins, and skin color variation
- Muscle fiber textures with 400+ striations
- No errors or broken images

如果找不到医学照片文件，系统会自动使用**超逼真的程序纹理**作为回退。

## Configuration Options | 配置选项

### Viewer Options | 查看器选项

```javascript
const options = {
    // Photo loading mode
    photoMode: 'real',              // 'real' for medical photos, 'procedural' for generated textures

    // Texture base path
    textureBasePath: '/static/textures/medical/',

    // Texture quality
    textureQuality: 'ultra',        // 'low', 'medium', 'high', 'ultra'

    // Display options
    showAcupoints: true,            // Show acupuncture points
    showMuscles: true,              // Show muscle anatomy
    showMeridians: true,            // Show TCM meridians

    // Selected items (for highlighting)
    selectedPoints: [],             // Array of acupoint codes (e.g., ['LI4', 'ST36'])
    selectedAreas: []               // Array of body area codes (e.g., ['neck', 'shoulder'])
};
```

## Implementation Details | 实现细节

### Photo Loading Process | 照片加载流程

1. **Initialization | 初始化**
   - Viewer creates Three.js TextureLoader
   - 查看器创建Three.js纹理加载器

2. **Photo Request | 照片请求**
   - `loadMedicalPhoto()` method is called
   - 调用`loadMedicalPhoto()`方法

3. **Texture Loading | 纹理加载**
   - TextureLoader attempts to load image file
   - 纹理加载器尝试加载图像文件

4. **Success Handler | 成功处理**
   - Texture is stored in `loadedTextures` cache
   - `applyMedicalPhotoTexture()` is called
   - Texture is applied to matching body parts via UV mapping
   - 纹理存储在缓存中并应用到匹配的身体部位

5. **Error Handler | 错误处理**
   - Warning logged to console
   - Procedural texture remains as fallback
   - 记录警告并保持程序纹理作为回退

### UV Mapping System | UV映射系统

The system uses `userData.bodyPart` tags to identify which mesh objects correspond to which anatomical regions:

```javascript
// Body parts are tagged during creation
mesh.userData.bodyPart = 'head';

// Photos are applied to matching tagged meshes
viewer.loadMedicalPhoto('/path/to/photo.jpg', 'head');
```

## Adding Medical Photos | 添加医学照片

### Step 1: Prepare Photos | 准备照片

1. Obtain high-quality medical photographs (ensure proper licensing)
2. Resize to at least 1024x1024 pixels
3. Optimize file size (use JPEG quality 85-95%)
4. Name files according to the standard naming convention

### Step 2: Upload to Server | 上传到服务器

1. Create directory if it doesn't exist:
   ```bash
   mkdir -p zhongyi_project/static/textures/medical/
   ```

2. Copy medical photos to the directory:
   ```bash
   cp your_photos/*.jpg zhongyi_project/static/textures/medical/
   ```

3. Collect static files (if using production settings):
   ```bash
   python manage.py collectstatic
   ```

### Step 3: Load Photos in Templates | 在模板中加载照片

Photos are automatically loaded if you call `loadStandardMedicalPhotos()`:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const viewer = new Body3DViewerRealPhoto('acupointViewer', options);

    // Automatically load all standard photos
    viewer.loadStandardMedicalPhotos();
});
```

## Testing | 测试

### Check if Photos are Loading | 检查照片是否加载

1. Open browser developer console (F12)
2. Navigate to acupuncture or tuina session form
3. Look for console messages:

Success:
```
真实医学照片3D查看器已初始化 | Real medical photo 3D viewer initialized
开始加载标准医学照片 | Loading standard medical photos...
✓ 已加载医学照片 | Loaded medical photo: head
✓ 已应用医学照片纹理 | Applied medical photo texture to head
```

Error (fallback active):
```
无法加载医学照片 | Cannot load: /static/textures/medical/head_front.jpg
(Procedural texture remains active as fallback)
```

### Verify Photo Display | 验证照片显示

1. Check that the 3D body model displays photographic textures
2. Rotate the model to inspect texture quality
3. Verify that textures align properly with body geometry

## Technical Features | 技术特性

### High-Quality Rendering | 高质量渲染

- **11 Professional Medical Studio Lights** | 11个专业医学演播室灯光
- **4096x4096 Shadow Resolution** | 4096x4096阴影分辨率
- **Physically Based Rendering (PBR)** | 基于物理的渲染
- **Anisotropic Filtering** | 各向异性过滤
- **Tone Mapping** | 色调映射

### Texture Processing | 纹理处理

- **Automatic Anisotropy** | 自动各向异性
- **Normal Mapping** | 法线贴图
- **Roughness Mapping** | 粗糙度贴图
- **UV Wrapping** | UV包装

### Performance | 性能

- **Texture Caching** | 纹理缓存
- **Lazy Loading** | 延迟加载
- **Fallback System** | 回退系统
- **Optimized Geometry** | 优化几何体

## Troubleshooting | 故障排除

### Photos Not Loading | 照片无法加载

**Problem**: Console shows "Cannot load" errors
**Solution**:
1. Verify file exists at exact path
2. Check file permissions (readable by web server)
3. Check filename spelling and case sensitivity
4. Verify CORS settings if serving from different domain

### Photos Look Distorted | 照片看起来扭曲

**Problem**: Textures appear stretched or misaligned
**Solution**:
1. Ensure photos have correct aspect ratio
2. Check that photo orientation matches body part
3. Consider using square images (1:1 ratio)
4. May need to adjust UV mapping in code

### Poor Performance | 性能差

**Problem**: 3D viewer is slow or laggy
**Solution**:
1. Reduce photo resolution (use 1024x1024 instead of 4096x4096)
2. Compress JPEG files (quality 80-85%)
3. Consider using WebP format for better compression
4. Reduce number of loaded photos (load on demand)

## Future Enhancements | 未来增强

Potential improvements to the system:

- [ ] Support for multiple views per body part (front/back/side)
- [ ] Dynamic texture switching (swap between different photo sets)
- [ ] Integration with DICOM medical imaging formats
- [ ] Texture annotation tools (mark specific anatomical features)
- [ ] Photo upload interface in admin panel
- [ ] Automatic photo alignment and UV mapping tools
- [ ] Support for transparent PNG overlays (e.g., for meridians)

## License and Medical Imagery | 许可和医学图像

**Important**: When using real medical photographs, ensure you have:

1. **Proper Licensing** | 适当的许可
   - Rights to use the medical imagery
   - Patient consent (if applicable)
   - Compliance with medical privacy laws (HIPAA, GDPR, etc.)

2. **Attribution** | 归属
   - Credit original photographers/institutions if required
   - Follow Creative Commons or other license terms

3. **Professional Standards** | 专业标准
   - Use only appropriate medical imagery
   - Ensure accuracy of anatomical representation
   - Maintain professional and educational context

## Support | 支持

For questions or issues with the medical photo 3D system:

1. Check console logs for error messages
2. Verify file paths and permissions
3. Review this documentation
4. Contact system administrator

---

**Version**: 1.0
**Last Updated**: 2025-11-26
**System**: Zhongyi TCM Management System
**Module**: 3D Anatomical Viewer (Real Photo Edition)
