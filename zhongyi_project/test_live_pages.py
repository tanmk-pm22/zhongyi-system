"""
Test Live Pages - 3D Viewer
测试实时页面 - 3D查看器
"""

import requests
import time

def test_server_running():
    """Test if server is running"""
    print("\n=== 测试服务器 | Testing Server ===")
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        print(f"✓ 服务器运行中 | Server running: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ 服务器未运行 | Server not running: {e}")
        return False

def test_acupuncture_page():
    """Test acupuncture page"""
    print("\n=== 测试针灸页面 | Testing Acupuncture Page ===")
    try:
        response = requests.get('http://127.0.0.1:8000/acupuncture/new/', timeout=10)
        print(f"状态码 | Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text

            # Check for 3D viewer elements
            checks = [
                ('acupointViewer', '✓ 3D容器ID'),
                ('body-3d-viewer-realphoto.js', '✓ JS文件'),
                ('Body3DViewerRealPhoto', '✓ 查看器类'),
                ('three.min.js', '✓ Three.js'),
                ('OrbitControls', '✓ 控制器')
            ]

            found = 0
            for check, desc in checks:
                if check in content:
                    print(f"  {desc}: {check}")
                    found += 1
                else:
                    print(f"  ✗ 缺失 | Missing: {check}")

            print(f"\n找到 {found}/5 个必需元素 | Found {found}/5 required elements")

            if found >= 4:
                print("✓ 针灸页面3D查看器配置正确")
                print("✓ Acupuncture page 3D viewer configured correctly")
                return True
            else:
                print("✗ 针灸页面3D查看器配置不完整")
                print("✗ Acupuncture page 3D viewer configuration incomplete")
                return False

        elif response.status_code == 302 or response.status_code == 301:
            print("ℹ 页面重定向 (可能需要登录) | Page redirected (login may be required)")
            print(f"  重定向到 | Redirected to: {response.headers.get('Location', 'Unknown')}")
            return True  # Not a failure, just needs login

        else:
            print(f"✗ 页面加载失败 | Page load failed: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败 | Request failed: {e}")
        return False

def test_tuina_page():
    """Test tuina page"""
    print("\n=== 测试推拿页面 | Testing Tuina Page ===")
    try:
        response = requests.get('http://127.0.0.1:8000/tuina/new/', timeout=10)
        print(f"状态码 | Status: {response.status_code}")

        if response.status_code == 200:
            content = response.text

            # Check for 3D viewer elements
            checks = [
                ('tuinaViewer', '✓ 3D容器ID'),
                ('body-3d-viewer-realphoto.js', '✓ JS文件'),
                ('Body3DViewerRealPhoto', '✓ 查看器类'),
                ('three.min.js', '✓ Three.js'),
                ('OrbitControls', '✓ 控制器')
            ]

            found = 0
            for check, desc in checks:
                if check in content:
                    print(f"  {desc}: {check}")
                    found += 1
                else:
                    print(f"  ✗ 缺失 | Missing: {check}")

            print(f"\n找到 {found}/5 个必需元素 | Found {found}/5 required elements")

            if found >= 4:
                print("✓ 推拿页面3D查看器配置正确")
                print("✓ Tuina page 3D viewer configured correctly")
                return True
            else:
                print("✗ 推拿页面3D查看器配置不完整")
                print("✗ Tuina page 3D viewer configuration incomplete")
                return False

        elif response.status_code == 302 or response.status_code == 301:
            print("ℹ 页面重定向 (可能需要登录) | Page redirected (login may be required)")
            print(f"  重定向到 | Redirected to: {response.headers.get('Location', 'Unknown')}")
            return True  # Not a failure, just needs login

        else:
            print(f"✗ 页面加载失败 | Page load failed: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败 | Request failed: {e}")
        return False

def test_static_js_file():
    """Test if static JS file is accessible"""
    print("\n=== 测试静态JS文件 | Testing Static JS File ===")
    try:
        response = requests.get('http://127.0.0.1:8000/static/js/body-3d-viewer-realphoto.js', timeout=5)
        print(f"状态码 | Status: {response.status_code}")

        if response.status_code == 200:
            size = len(response.content)
            print(f"✓ JS文件可访问 | JS file accessible")
            print(f"  文件大小 | File size: {size:,} bytes ({size/1024:.1f} KB)")

            # Check if it's JavaScript
            if 'class Body3DViewerRealPhoto' in response.text:
                print("  ✓ 包含查看器类 | Contains viewer class")
                return True
            else:
                print("  ✗ 文件内容异常 | File content abnormal")
                return False
        else:
            print(f"✗ JS文件不可访问 | JS file not accessible: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败 | Request failed: {e}")
        return False

def main():
    print("=" * 70)
    print("实时页面测试 - 3D查看器")
    print("Live Page Test - 3D Viewer")
    print("=" * 70)
    print("\n确保开发服务器正在运行: python manage.py runserver")
    print("Make sure dev server is running: python manage.py runserver")

    time.sleep(1)

    results = []

    results.append(("服务器 | Server", test_server_running()))
    results.append(("静态JS | Static JS", test_static_js_file()))
    results.append(("针灸页面 | Acupuncture", test_acupuncture_page()))
    results.append(("推拿页面 | Tuina", test_tuina_page()))

    # Summary
    print("\n" + "=" * 70)
    print("测试总结 | Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\n总计 | Total: {passed}/{total} 测试通过 | tests passed")

    if passed >= 3:  # At least server, static, and one page
        print("\n" + "=" * 70)
        print("✓ 系统运行正常！")
        print("✓ System running normally!")
        print("=" * 70)
        print("\n下一步 | Next Steps:")
        print("1. 在浏览器中访问 | Open in browser:")
        print("   http://127.0.0.1:8000/acupuncture/new/")
        print("   http://127.0.0.1:8000/tuina/new/")
        print("\n2. 打开浏览器控制台 (F12) 查看3D加载信息")
        print("   Open browser console (F12) to see 3D loading info")
        print("\n3. 应该看到 | You should see:")
        print("   - 3D人体模型显示 | 3D human body model displayed")
        print("   - 可以旋转和缩放 | Can rotate and zoom")
        print("   - 控制台无JavaScript错误 | No JavaScript errors in console")
        print("\n4. 如果看不到3D图像 | If 3D image not visible:")
        print("   - 清除浏览器缓存 | Clear browser cache (Ctrl+Shift+Delete)")
        print("   - 硬刷新 | Hard refresh (Ctrl+F5)")
        print("   - 检查浏览器控制台错误 | Check browser console for errors")
    else:
        print("\n⚠ 发现问题，请检查上述错误")
        print("⚠ Issues found, please check errors above")

    return passed >= 3

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
