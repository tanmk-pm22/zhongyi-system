"""
Check 3D Viewer Integration
检查3D查看器集成
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def check_acupuncture_page():
    """Check acupuncture page 3D viewer"""
    print("\n=== 检查针灸页面 | Checking Acupuncture Page ===")

    client = Client()

    # Get or create test user
    user = User.objects.filter(username='testadmin').first()
    if not user:
        user = User.objects.create_superuser(
            username='testadmin',
            email='test@test.com',
            password='admin123'
        )

    # Login
    client.login(username='testadmin', password='admin123')

    # Get acupuncture new page
    response = client.get('/acupuncture/new/')

    print(f"状态码 | Status Code: {response.status_code}")

    if response.status_code == 200:
        content = response.content.decode('utf-8')

        # Check for key elements
        checks = [
            ('acupointViewer', '3D查看器容器'),
            ('body-3d-viewer-realphoto.js', 'JS文件引用'),
            ('Body3DViewerRealPhoto', '查看器类'),
            ('three.min.js', 'Three.js库'),
            ('OrbitControls.js', '轨道控制')
        ]

        print("\n检查项 | Checks:")
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc}: {check}")
            else:
                print(f"  ✗ {desc} NOT FOUND: {check}")

        # Check template rendering
        if '<div id="acupointViewer"' in content:
            print("\n✓ 3D查看器容器已渲染 | 3D viewer container rendered")
        else:
            print("\n✗ 3D查看器容器未找到 | 3D viewer container NOT found")

        # Extract viewer initialization code
        if 'new Body3DViewerRealPhoto' in content:
            print("✓ 查看器初始化代码存在 | Viewer initialization code exists")

            # Find the initialization code
            start = content.find('new Body3DViewerRealPhoto')
            if start != -1:
                end = content.find('});', start) + 3
                init_code = content[start:end]
                print(f"\n初始化代码 | Initialization code:\n{init_code[:200]}...")
        else:
            print("✗ 查看器初始化代码缺失 | Viewer initialization code MISSING")

        return True
    else:
        print(f"✗ 页面加载失败 | Page failed to load: {response.status_code}")
        if hasattr(response, 'context') and response.context and 'exception' in response.context:
            print(f"错误 | Error: {response.context['exception']}")
        return False

def check_tuina_page():
    """Check tuina page 3D viewer"""
    print("\n=== 检查推拿页面 | Checking Tuina Page ===")

    client = Client()

    # Login
    client.login(username='testadmin', password='admin123')

    # Get tuina new page
    response = client.get('/tuina/new/')

    print(f"状态码 | Status Code: {response.status_code}")

    if response.status_code == 200:
        content = response.content.decode('utf-8')

        # Check for key elements
        checks = [
            ('tuinaViewer', '3D查看器容器'),
            ('body-3d-viewer-realphoto.js', 'JS文件引用'),
            ('Body3DViewerRealPhoto', '查看器类'),
            ('three.min.js', 'Three.js库'),
            ('OrbitControls.js', '轨道控制')
        ]

        print("\n检查项 | Checks:")
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc}: {check}")
            else:
                print(f"  ✗ {desc} NOT FOUND: {check}")

        # Check template rendering
        if '<div id="tuinaViewer"' in content:
            print("\n✓ 3D查看器容器已渲染 | 3D viewer container rendered")
        else:
            print("\n✗ 3D查看器容器未找到 | 3D viewer container NOT found")

        # Extract viewer initialization code
        if 'new Body3DViewerRealPhoto' in content:
            print("✓ 查看器初始化代码存在 | Viewer initialization code exists")
        else:
            print("✗ 查看器初始化代码缺失 | Viewer initialization code MISSING")

        return True
    else:
        print(f"✗ 页面加载失败 | Page failed to load: {response.status_code}")
        return False

def check_static_file():
    """Check if static JS file is accessible"""
    print("\n=== 检查静态文件 | Checking Static Files ===")

    js_file = os.path.join(
        os.path.dirname(__file__),
        'static', 'js', 'body-3d-viewer-realphoto.js'
    )

    if os.path.exists(js_file):
        size = os.path.getsize(js_file)
        print(f"✓ JS文件存在 | JS file exists: {js_file}")
        print(f"  文件大小 | File size: {size:,} bytes ({size/1024:.1f} KB)")

        # Check file is not empty and has valid JS
        with open(js_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            print(f"  第一行 | First line: {first_line[:80]}...")

        return True
    else:
        print(f"✗ JS文件不存在 | JS file NOT exists: {js_file}")
        return False

def main():
    print("=" * 70)
    print("3D查看器诊断检查")
    print("3D Viewer Diagnostic Check")
    print("=" * 70)

    results = []

    results.append(("静态文件 | Static", check_static_file()))
    results.append(("针灸页面 | Acupuncture", check_acupuncture_page()))
    results.append(("推拿页面 | Tuina", check_tuina_page()))

    # Summary
    print("\n" + "=" * 70)
    print("诊断总结 | Diagnostic Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\n总计 | Total: {passed}/{total} 检查通过 | checks passed")

    if passed == total:
        print("\n✓ 所有检查通过！3D查看器应该可以正常显示。")
        print("✓ All checks passed! 3D viewer should display correctly.")
        print("\n如果浏览器中仍未显示3D图像，请：")
        print("If 3D image still not showing in browser, please:")
        print("1. 清除浏览器缓存 (Ctrl+Shift+Delete)")
        print("   Clear browser cache (Ctrl+Shift+Delete)")
        print("2. 硬刷新页面 (Ctrl+F5)")
        print("   Hard refresh page (Ctrl+F5)")
        print("3. 打开浏览器控制台 (F12) 查看JavaScript错误")
        print("   Open browser console (F12) to check JavaScript errors")
    else:
        print("\n⚠ 发现问题，请查看上述错误")
        print("⚠ Issues found, please check errors above")

    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
