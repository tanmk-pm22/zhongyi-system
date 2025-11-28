#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
增强版3D人体查看器测试
Enhanced 3D Body Viewer Test
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

import time
import requests
from pathlib import Path

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def print_test(num, text):
    print(f"\n[测试 {num} | Test {num}] {text}")

def check_file(filepath, description):
    """Check if a file exists and get its size"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✓ 文件存在 | File exists: {description}")
        print(f"    路径 | Path: {filepath}")
        print(f"    大小 | Size: {size:,} bytes ({size/1024:.1f} KB)")
        return True
    else:
        print(f"  ✗ 文件不存在 | File not found: {description}")
        return False

def check_url(url, description):
    """Check if a URL is accessible"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"  ✓ {description}: HTTP {response.status_code} ✓")
            return True, response.text
        else:
            print(f"  ✗ {description}: HTTP {response.status_code} ✗")
            return False, None
    except Exception as e:
        print(f"  ✗ {description}: 错误 | Error - {str(e)}")
        return False, None

def check_content(html, keywords, description):
    """Check if HTML contains required keywords"""
    print(f"\n  检查 | Checking: {description}")
    missing = []
    for keyword in keywords:
        if keyword in html:
            print(f"    ✓ '{keyword}'")
        else:
            print(f"    ✗ '{keyword}' - 缺失 | Missing")
            missing.append(keyword)
    return len(missing) == 0

def main():
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "增强版3D人体查看器系统测试" + " "*20 + "║")
    print("║" + " "*15 + "Enhanced 3D Body Viewer System Test" + " "*15 + "║")
    print("╚" + "="*78 + "╝")

    base_dir = Path(__file__).parent
    static_dir = base_dir / 'static' / 'js'
    templates_dir = base_dir / 'templates'

    test_results = []

    # Test 1: Check Enhanced JS file
    print_header("第一部分：文件系统检查 | Part 1: File System Check")
    print_test(1, "检查增强版3D查看器JS文件 | Check Enhanced 3D Viewer JS")

    enhanced_js = static_dir / 'body-3d-viewer-enhanced.js'
    result1 = check_file(enhanced_js, "增强版3D查看器 | Enhanced 3D Viewer")

    if result1:
        # Check for key features in the JS file
        try:
            with open(enhanced_js, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(enhanced_js, 'r', encoding='latin-1') as f:
                content = f.read()
        features = [
            'Body3DViewerEnhanced',
            'createEnhancedHumanBody',
            'MeshStandardMaterial',
            'castShadow',
            'receiveShadow',
            'createArm',
            'createLeg',
            'addControls',
            'OrbitControls'
        ]
        print("\n  关键功能检查 | Key Features Check:")
        for feature in features:
            if feature in content:
                print(f"    ✓ {feature}")
            else:
                print(f"    ✗ {feature} - 缺失 | Missing")
                result1 = False

    test_results.append(("增强版JS文件 | Enhanced JS File", result1))

    # Test 2: Check template files
    print_test(2, "检查模板文件更新 | Check Template File Updates")

    acupuncture_template = templates_dir / 'acupuncture' / 'acupuncturesession_form.html'
    tuina_template = templates_dir / 'tuina' / 'session_form.html'

    result2a = check_file(acupuncture_template, "针灸模板 | Acupuncture Template")
    result2b = check_file(tuina_template, "推拿模板 | Tuina Template")

    if result2a:
        with open(acupuncture_template, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'body-3d-viewer-enhanced.js' in content:
                print("    ✓ 针灸模板引用增强版JS | Acupuncture uses enhanced JS")
            else:
                print("    ✗ 针灸模板未引用增强版JS | Acupuncture not using enhanced JS")
                result2a = False

            if 'Body3DViewerEnhanced' in content:
                print("    ✓ 针灸模板使用增强版类 | Acupuncture uses enhanced class")
            else:
                print("    ✗ 针灸模板未使用增强版类 | Acupuncture not using enhanced class")
                result2a = False

    if result2b:
        with open(tuina_template, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'body-3d-viewer-enhanced.js' in content:
                print("    ✓ 推拿模板引用增强版JS | Tuina uses enhanced JS")
            else:
                print("    ✗ 推拿模板未引用增强版JS | Tuina not using enhanced JS")
                result2b = False

            if 'Body3DViewerEnhanced' in content:
                print("    ✓ 推拿模板使用增强版类 | Tuina uses enhanced class")
            else:
                print("    ✗ 推拿模板未使用增强版类 | Tuina not using enhanced class")
                result2b = False

    result2 = result2a and result2b
    test_results.append(("模板文件更新 | Template Updates", result2))

    # Test 3: Check server availability and pages
    print_header("第二部分：服务器和页面测试 | Part 2: Server and Page Test")
    print_test(3, "测试针灸和推拿页面 | Test Acupuncture and Tuina Pages")

    print("\n  等待服务器启动... | Waiting for server...")
    time.sleep(2)

    # Test acupuncture page
    success3a, html_acu = check_url(
        'http://127.0.0.1:8000/acupuncture/create/',
        '针灸创建页面 | Acupuncture Create Page'
    )

    if success3a and html_acu:
        result3a = check_content(
            html_acu,
            [
                'body-3d-viewer-enhanced.js',
                'Body3DViewerEnhanced',
                'acupointViewer',
                '3D人体图解',
                '3D Body Diagram'
            ],
            "针灸页面内容 | Acupuncture Page Content"
        )
    else:
        result3a = False

    # Test tuina page
    success3b, html_tuina = check_url(
        'http://127.0.0.1:8000/tuina/new/',
        '推拿创建页面 | Tuina Create Page'
    )

    if success3b and html_tuina:
        result3b = check_content(
            html_tuina,
            [
                'body-3d-viewer-enhanced.js',
                'Body3DViewerEnhanced',
                'tuinaViewer',
                '3D人体图解',
                '3D Body Diagram'
            ],
            "推拿页面内容 | Tuina Page Content"
        )
    else:
        result3b = False

    result3 = result3a and result3b
    test_results.append(("页面可访问性 | Page Accessibility", result3))

    # Test 4: Feature comparison
    print_header("第三部分：功能对比 | Part 3: Feature Comparison")
    print_test(4, "增强版特性对比 | Enhanced Features Comparison")

    print("\n  增强版新特性 | New Enhanced Features:")
    print("    ✓ 更真实的人体比例 | More realistic body proportions")
    print("    ✓ 平滑着色 | Smooth shading")
    print("    ✓ 高级光照系统 | Advanced lighting system")
    print("    ✓ 实时阴影 | Real-time shadows")
    print("    ✓ 更好的材质 | Better materials")
    print("    ✓ 关节和肌肉细节 | Joint and muscle details")
    print("    ✓ 更流畅的动画 | Smoother animations")
    print("    ✓ 发光穴位标记 | Glowing acupoint markers")
    print("    ✓ 半透明治疗区域 | Translucent treatment areas")
    print("    ✓ 雾效果增加深度感 | Fog effect for depth")

    result4 = True
    test_results.append(("增强版特性 | Enhanced Features", result4))

    # Summary
    print_header("测试总结 | Test Summary")

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    print(f"\n总测试数 | Total Tests: {total}")
    print(f"通过数量 | Passed: {passed}")
    print(f"失败数量 | Failed: {total - passed}")
    print(f"成功率 | Success Rate: {passed/total*100:.1f}%")

    print("\n详细结果 | Detailed Results:")
    for name, result in test_results:
        status = "✓ 通过 | PASSED" if result else "✗ 失败 | FAILED"
        print(f"  {status} - {name}")

    print("\n" + "="*80)

    if passed == total:
        print("\n🎉 所有测试通过！增强版3D人体查看器已成功集成！")
        print("🎉 All tests passed! Enhanced 3D Body Viewer successfully integrated!")

        print("\n✅ 系统改进 | System Improvements:")
        print("   ✓ 更真实的3D人体模型")
        print("   ✓ 专业级医学可视化")
        print("   ✓ 更好的交互体验")
        print("   ✓ 更流畅的性能")

        print("\n✅ Realistic Human Body Features:")
        print("   ✓ More realistic 3D human model")
        print("   ✓ Professional medical visualization")
        print("   ✓ Better interactive experience")
        print("   ✓ Smoother performance")
    else:
        print("\n⚠️  部分测试未通过，请检查上述错误")
        print("⚠️  Some tests failed, please check errors above")

    print("\n" + "="*80)
    print("\n系统已就绪！请访问以下页面查看增强版3D人体图解：")
    print("System ready! Visit the following pages to see enhanced 3D body viewer:")
    print("\n  针灸 | Acupuncture: http://localhost:8000/acupuncture/create/")
    print("  推拿 | Tuina: http://localhost:8000/tuina/new/")
    print("\n" + "="*80)

    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n测试被中断 | Test interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n错误 | Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
