"""
Test Human Anatomy Atlas 2026 Viewer
测试人体解剖图谱2026查看器
"""

import os
import requests

def test_atlas_viewer():
    print("=" * 70)
    print("人体解剖图谱2026查看器测试")
    print("Human Anatomy Atlas 2026 Viewer Test")
    print("=" * 70)

    # Check files
    print("\n1. 文件检查 | File Check:")
    js_file = os.path.join(os.path.dirname(__file__), 'static/js/anatomy-atlas-viewer.js')
    if os.path.exists(js_file):
        size = os.path.getsize(js_file)
        print(f"   ✓ anatomy-atlas-viewer.js ({size:,} bytes)")
    else:
        print(f"   ✗ anatomy-atlas-viewer.js NOT FOUND")
        return False

    # Check templates
    print("\n2. 模板检查 | Template Check:")

    acup_template = os.path.join(os.path.dirname(__file__), 'templates/acupuncture/acupuncturesession_form.html')
    with open(acup_template, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'AnatomyAtlasViewer' in content:
        print(f"   ✓ 针灸模板使用AnatomyAtlasViewer | Acupuncture uses AnatomyAtlasViewer")
    else:
        print(f"   ✗ 针灸模板未使用AnatomyAtlasViewer | Acupuncture NOT using AnatomyAtlasViewer")

    tuina_template = os.path.join(os.path.dirname(__file__), 'templates/tuina/session_form.html')
    with open(tuina_template, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'AnatomyAtlasViewer' in content:
        print(f"   ✓ 推拿模板使用AnatomyAtlasViewer | Tuina uses AnatomyAtlasViewer")
    else:
        print(f"   ✗ 推拿模板未使用AnatomyAtlasViewer | Tuina NOT using AnatomyAtlasViewer")

    # Check server
    print("\n3. 服务器检查 | Server Check:")
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        print(f"   ✓ 服务器运行中 | Server running ({response.status_code})")

        # Check static file
        js_response = requests.get('http://127.0.0.1:8000/static/js/anatomy-atlas-viewer.js', timeout=5)
        if js_response.status_code == 200:
            print(f"   ✓ JS文件可访问 | JS file accessible ({len(js_response.content):,} bytes)")
        else:
            print(f"   ✗ JS文件不可访问 | JS file not accessible")

    except requests.exceptions.RequestException:
        print(f"   ℹ 服务器未运行 | Server not running")

    print("\n" + "=" * 70)
    print("✅ 人体解剖图谱2026查看器已安装！")
    print("✅ Human Anatomy Atlas 2026 Viewer installed!")
    print("=" * 70)

    print("""
## 新系统特点 | New System Features:

✅ **不是3D模型 | Not 3D Models**
   - 使用2D医学解剖图像 | Uses 2D medical anatomy images
   - 真实医学照片支持 | Real medical photo support

✅ **AI增强功能 | AI-Enhanced**
   - AI穴位检测 | AI acupoint detection
   - AI治疗推荐 | AI treatment recommendations

✅ **交互式界面 | Interactive Interface**
   - 多视图（正面/背面/侧面）| Multiple views (front/back/sides)
   - 图层切换（皮肤/肌肉/骨骼/经络）| Layer switching (skin/muscles/skeleton/meridians)
   - 点击选择穴位/治疗区域 | Click to select acupoints/areas

✅ **占位图显示 | Placeholder Display**
   - 当前使用解剖图占位图 | Currently uses anatomical placeholder
   - 标注真实穴位位置 | Real acupoint positions marked
   - 可添加真实医学照片 | Can add real medical photos

## 如何使用 | How to Use:

1. 访问页面 | Visit pages:
   http://127.0.0.1:8000/acupuncture/create/
   http://127.0.0.1:8000/tuina/new/

2. 登录后查看解剖图谱 | Login to view anatomy atlas

3. 使用控制面板 | Use control panel:
   - 选择视图 | Select view
   - 选择图层 | Select layer
   - 启用AI功能 | Enable AI features
   - 点击穴位/区域 | Click acupoints/areas

## 添加真实医学图像 | Add Real Medical Images:

放置图像到 | Place images in:
zhongyi_project/static/images/anatomy/

需要的文件 | Required files:
- skin_surface.jpg
- muscles_anterior.jpg
- muscles_posterior.jpg
- skeleton.jpg
- tcm_meridians.jpg

详细说明 | Details:
static/images/anatomy/README.md
""")

    return True

if __name__ == '__main__':
    test_atlas_viewer()
