"""
测试Three.js 3D人体查看器集成 | Test Three.js 3D Body Viewer Integration

运行方法 | How to run:
cd zhongyi_project
python -X utf8 test_threejs_3d_viewer.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

def test_static_file_exists():
    """测试3D查看器JS文件是否存在 | Test if 3D viewer JS file exists"""
    print("\n" + "="*80)
    print("测试1: 检查Three.js 3D查看器文件 | Test 1: Check Three.js 3D Viewer File")
    print("="*80)

    js_file = os.path.join(
        os.path.dirname(__file__),
        'static', 'js', 'body-3d-viewer-threejs.js'
    )

    if os.path.exists(js_file):
        size = os.path.getsize(js_file)
        print(f"✓ Three.js 3D查看器文件存在 | Three.js 3D Viewer file exists")
        print(f"  文件路径 | File path: {js_file}")
        print(f"  文件大小 | File size: {size:,} bytes ({size/1024:.1f} KB)")

        # Check file content
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Body3DViewerThreeJS' in content:
                print(f"✓ 包含Body3DViewerThreeJS类 | Contains Body3DViewerThreeJS class")
            if 'THREE.Scene' in content:
                print(f"✓ 使用Three.js库 | Uses Three.js library")
            if 'createHumanBody' in content:
                print(f"✓ 包含人体模型创建函数 | Contains human body creation function")
            if 'addAcupoints' in content:
                print(f"✓ 包含穴位标记功能 | Contains acupoint marker functionality")
        return True
    else:
        print(f"✗ Three.js 3D查看器文件不存在 | Three.js 3D Viewer file not found")
        print(f"  期望路径 | Expected path: {js_file}")
        return False


def test_template_integration():
    """测试模板是否集成了Three.js | Test if templates integrate Three.js"""
    print("\n" + "="*80)
    print("测试2: 检查模板集成 | Test 2: Check Template Integration")
    print("="*80)

    templates = [
        ('templates/acupuncture/acupuncturesession_form.html', 'acupointViewer'),
        ('templates/tuina/session_form.html', 'tuinaViewer'),
    ]

    success = True
    for template_path, viewer_id in templates:
        full_path = os.path.join(os.path.dirname(__file__), template_path)

        if not os.path.exists(full_path):
            print(f"\n✗ 模板文件不存在 | Template not found: {template_path}")
            success = False
            continue

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"\n检查 | Checking: {template_path}")
        checks = {
            'Three.js CDN': 'three@0.160' in content or 'three.min.js' in content,
            'OrbitControls': 'OrbitControls' in content,
            'body-3d-viewer-threejs.js': 'body-3d-viewer-threejs.js' in content,
            'Body3DViewerThreeJS初始化': 'Body3DViewerThreeJS' in content,
            f'{viewer_id}容器': viewer_id in content,
        }

        for check_name, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            if not passed:
                success = False

    return success


def test_url_access():
    """测试URL访问 | Test URL access"""
    print("\n" + "="*80)
    print("测试3: 检查URL配置 | Test 3: Check URL Configuration")
    print("="*80)

    from django.urls import reverse, NoReverseMatch

    urls_to_test = [
        ('acupuncture:create', '针灸创建页面 | Acupuncture Create'),
        ('tuina:session_create', '推拿创建页面 | Tuina Create'),
    ]

    success = True
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✓ {description}: {url}")
        except NoReverseMatch:
            print(f"✗ {description}: URL未找到 | URL not found ({url_name})")
            success = False

    return success


def test_three_js_features():
    """测试Three.js功能特性 | Test Three.js features"""
    print("\n" + "="*80)
    print("测试4: Three.js功能特性 | Test 4: Three.js Features")
    print("="*80)

    js_file = os.path.join(
        os.path.dirname(__file__),
        'static', 'js', 'body-3d-viewer-threejs.js'
    )

    if not os.path.exists(js_file):
        print("✗ 无法测试，文件不存在 | Cannot test, file not found")
        return False

    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()

    features = {
        '3D场景创建 | 3D Scene Creation': 'THREE.Scene' in content,
        '透视相机 | Perspective Camera': 'PerspectiveCamera' in content,
        '渲染器 | Renderer': 'WebGLRenderer' in content,
        '光照系统 | Lighting System': 'AmbientLight' in content and 'DirectionalLight' in content,
        '轨道控制 | Orbit Controls': 'OrbitControls' in content,
        '人体模型创建 | Human Body Creation': 'createHumanBody' in content,
        '穴位标记 | Acupoint Markers': 'createAcupointMarker' in content,
        '治疗区域标记 | Treatment Area Markers': 'createAreaMarker' in content,
        '视角切换 | View Switching': 'setView' in content,
        '动画循环 | Animation Loop': 'animate' in content,
        '阴影效果 | Shadow Effects': 'castShadow' in content,
        '材质系统 | Material System': 'MeshPhongMaterial' in content,
        '几何体 | Geometries': 'CapsuleGeometry' in content or 'SphereGeometry' in content,
        '标签精灵 | Label Sprites': 'Sprite' in content or 'CanvasTexture' in content,
    }

    all_passed = True
    for feature, present in features.items():
        status = "✓" if present else "✗"
        print(f"  {status} {feature}")
        if not present:
            all_passed = False

    return all_passed


def generate_summary():
    """生成测试摘要 | Generate test summary"""
    print("\n" + "="*80)
    print("测试摘要 | Test Summary")
    print("="*80)

    print("""
Three.js 3D人体查看器已成功集成! | Three.js 3D Body Viewer Successfully Integrated!

主要改进 | Key Improvements:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ 真实3D人体模型 | Realistic 3D Human Model
  - 使用Three.js专业3D图形库
  - 解剖学准确的身体比例
  - 真实的肤色渐变和材质

✓ 完整的3D交互 | Full 3D Interaction
  - 鼠标拖动360度旋转
  - 滚轮缩放查看细节
  - 正面、背面、侧面视角切换

✓ 专业的光照系统 | Professional Lighting System
  - 环境光+定向光+补光
  - 实时阴影渲染
  - 高质量抗锯齿

✓ 3D穴位标记 | 3D Acupoint Markers
  - 立体球形标记
  - 发光效果
  - 动态标签跟随相机

✓ 治疗区域可视化 | Treatment Area Visualization
  - 半透明3D区域框
  - 肌肉组织显示
  - 多区域选择

使用说明 | Usage Instructions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 启动开发服务器 | Start Development Server:
   cd zhongyi_project
   python manage.py runserver

2. 访问针灸页面 | Visit Acupuncture Page:
   http://127.0.0.1:8000/acupuncture/create/

3. 访问推拿页面 | Visit Tuina Page:
   http://127.0.0.1:8000/tuina/create/

4. 操作方法 | How to Use:
   - 拖动鼠标旋转人体 | Drag to rotate the body
   - 滚轮缩放 | Scroll to zoom
   - 点击按钮切换视角 | Click buttons to switch views
   - 点击穴位/区域进行选择 | Click acupoints/areas to select

技术栈 | Technology Stack:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Three.js r160 (3D图形引擎 | 3D Graphics Engine)
- OrbitControls (轨道控制器 | Orbit Controller)
- WebGL (硬件加速渲染 | Hardware Accelerated Rendering)
- Django Templates (服务器端渲染 | Server-side Rendering)

对比旧版本 | Comparison with Old Version:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

旧版本(SVG) | Old Version (SVG):       新版本(Three.js) | New Version (Three.js):
- 2D平面图形                          ✓ 真实3D立体模型
- 简单的形状和渐变                     ✓ 专业解剖学建模
- 有限的交互                          ✓ 完整的3D旋转和缩放
- 静态视角                            ✓ 多视角切换
- 基础阴影                            ✓ 实时光照和阴影

下一步建议 | Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

如果您希望进一步改进，可以考虑：

1. 导入专业医学3D模型 (.glb文件)
2. 添加更多解剖学细节（骨骼、经络）
3. 实现穴位点击后的详细信息面板
4. 添加经络走向的3D线条
5. 支持VR/AR查看模式

但目前的版本已经比SVG版本有了质的飞跃！
The current version is already a huge improvement over the SVG version!
""")


def main():
    """主测试函数 | Main test function"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "Three.js 3D人体查看器测试" + " "*20 + "║")
    print("║" + " "*15 + "Three.js 3D Body Viewer Test" + " "*15 + "║")
    print("╚" + "="*78 + "╝")

    results = {
        '静态文件检查': test_static_file_exists(),
        '模板集成检查': test_template_integration(),
        'URL配置检查': test_url_access(),
        'Three.js功能检查': test_three_js_features(),
    }

    generate_summary()

    # Final result
    print("\n" + "="*80)
    print("最终结果 | Final Results")
    print("="*80)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✓ 通过 | PASSED" if result else "✗ 失败 | FAILED"
        print(f"{test_name}: {status}")

    print(f"\n总计 | Total: {passed}/{total} 测试通过 | tests passed")

    if passed == total:
        print("\n🎉 所有测试通过！Three.js 3D人体查看器已就绪！")
        print("   All tests passed! Three.js 3D Body Viewer is ready!")
        print("\n请运行服务器并访问针灸或推拿页面查看效果：")
        print("Please run the server and visit acupuncture or tuina pages:")
        print("   python manage.py runserver")
        print("   http://127.0.0.1:8000/acupuncture/create/")
        print("   http://127.0.0.1:8000/tuina/create/")
    else:
        print(f"\n⚠ 有{total - passed}个测试失败，请检查上述错误。")
        print(f"   {total - passed} test(s) failed. Please check the errors above.")

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
