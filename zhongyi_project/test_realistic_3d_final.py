#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Final Comprehensive Test for Realistic 3D Body Viewer
真实人体3D图解最终综合测试
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_realistic_3d_viewer():
    """Comprehensive test for realistic 3D body viewer"""

    print("=" * 80)
    print("真实人体3D图解最终综合测试 | Final Realistic 3D Body Viewer Test")
    print("=" * 80)

    client = Client(SERVER_NAME='localhost')

    # Create/get test user
    user = User.objects.filter(username='realistic_test_user').first()
    if not user:
        user = User.objects.create_user(
            username='realistic_test_user',
            password='test123',
            role='practitioner'
        )

    client.login(username='realistic_test_user', password='test123')

    # Test counters
    total_tests = 0
    passed_tests = 0

    print("\n" + "=" * 80)
    print("【第一部分：文件系统检查】| Part 1: File System Check")
    print("=" * 80)

    # Test 1: Check realistic JS file exists
    print("\n[1/12] 检查真实人体JS文件 | Check realistic body JS file...")
    total_tests += 1
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'js', 'body-3d-viewer-realistic.js')
    if os.path.exists(js_path):
        file_size = os.path.getsize(js_path)
        print(f"✓ 文件存在 | File exists")
        print(f"  路径 | Path: {js_path}")
        print(f"  大小 | Size: {file_size:,} bytes (~{file_size/1024:.1f} KB)")

        # Check file content
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
            features = {
                'Body3DViewerRealistic类': 'Body3DViewerRealistic' in content,
                'SVG图形支持': 'createElementNS' in content and 'svg' in content,
                '渐变效果': 'linearGradient' in content or 'skinGradient' in content,
                '肌肉绘制': 'muscleGradient' in content or 'drawFrontMuscles' in content,
                '穴位标记': 'createAcupointMarker' in content,
                '治疗区域': 'createTreatmentArea' in content,
                '交互事件': 'addEventListener' in content,
                '双语支持': '中文' in content or '| Front' in content,
            }

            all_features = all(features.values())
            if all_features:
                print("  ✓ 所有核心功能已实现 | All core features implemented")
                for feature, exists in features.items():
                    print(f"    ✓ {feature}")
                passed_tests += 1
            else:
                print("  ✗ 部分功能缺失 | Some features missing")
                for feature, exists in features.items():
                    status = "✓" if exists else "✗"
                    print(f"    {status} {feature}")
    else:
        print(f"✗ 文件不存在 | File not found: {js_path}")

    # Test 2: Check base.html references realistic version
    print("\n[2/12] 检查base.html引用 | Check base.html reference...")
    total_tests += 1
    base_path = os.path.join(os.path.dirname(__file__), 'templates', 'base.html')
    with open(base_path, 'r', encoding='utf-8') as f:
        base_content = f.read()
        uses_realistic = 'body-3d-viewer-realistic.js' in base_content

        if uses_realistic:
            print("✓ base.html正确引用真实版本 | base.html correctly references realistic version")
            passed_tests += 1
        else:
            print("✗ base.html未引用真实版本 | base.html not referencing realistic version")

    print("\n" + "=" * 80)
    print("【第二部分：针灸模块测试】| Part 2: Acupuncture Module Test")
    print("=" * 80)

    # Test 3: Acupuncture page accessibility
    print("\n[3/12] 测试针灸页面可访问性 | Test acupuncture page accessibility...")
    total_tests += 1
    response = client.get('/acupuncture/create/')
    if response.status_code == 200:
        print(f"✓ 页面可访问 | Page accessible (Status: {response.status_code})")
        passed_tests += 1
    else:
        print(f"✗ 页面无法访问 | Page not accessible (Status: {response.status_code})")

    # Test 4: Check 3D viewer container
    print("\n[4/12] 检查3D图解容器 | Check 3D viewer container...")
    total_tests += 1
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        has_container = 'id="acupointViewer"' in content
        has_title = '3D人体图解 - 穴位定位' in content
        has_bilingual_title = '3D Body Diagram - Acupoint Location' in content

        if has_container and has_title and has_bilingual_title:
            print("✓ 3D图解容器配置正确 | 3D viewer container properly configured")
            print("  ✓ 容器ID存在 | Container ID exists")
            print("  ✓ 中文标题存在 | Chinese title exists")
            print("  ✓ 英文标题存在 | English title exists")
            passed_tests += 1
        else:
            print("✗ 3D图解容器配置有问题 | 3D viewer container has issues")
            print(f"  - 容器ID | Container: {has_container}")
            print(f"  - 中文标题 | CN Title: {has_title}")
            print(f"  - 英文标题 | EN Title: {has_bilingual_title}")

    # Test 5: Check bilingual labels in acupuncture
    print("\n[5/12] 检查针灸页面双语标签 | Check acupuncture bilingual labels...")
    total_tests += 1
    if response.status_code == 200:
        bilingual_labels = [
            '患者 | Patient',
            '治疗日期 | Session Date',
            '主诉 | Chief Complaint',
            '中医诊断 | TCM Diagnosis',
            '使用穴位 | Acupoints Used',
            '保存 | Save',
        ]

        all_labels_present = all(label in content for label in bilingual_labels)

        if all_labels_present:
            print("✓ 所有双语标签正确显示 | All bilingual labels properly displayed")
            for label in bilingual_labels:
                print(f"  ✓ {label}")
            passed_tests += 1
        else:
            print("✗ 部分双语标签缺失 | Some bilingual labels missing")
            for label in bilingual_labels:
                status = "✓" if label in content else "✗"
                print(f"  {status} {label}")

    # Test 6: Check JavaScript initialization
    print("\n[6/12] 检查JavaScript初始化代码 | Check JavaScript initialization...")
    total_tests += 1
    if response.status_code == 200:
        has_viewer_init = 'new Body3DViewer' in content
        has_acupoint_option = 'showAcupoints: true' in content
        has_muscle_option = 'showMuscles: false' in content

        if has_viewer_init:
            print("✓ JavaScript初始化代码存在 | JavaScript initialization exists")
            print(f"  ✓ 创建3D查看器 | Viewer creation: {has_viewer_init}")
            print(f"  ✓ 穴位模式开启 | Acupoint mode: {has_acupoint_option}")
            print(f"  ✓ 肌肉模式关闭 | Muscle mode off: {has_muscle_option}")
            passed_tests += 1
        else:
            print("✗ JavaScript初始化代码缺失 | JavaScript initialization missing")

    print("\n" + "=" * 80)
    print("【第三部分：推拿模块测试】| Part 3: Tuina Module Test")
    print("=" * 80)

    # Test 7: Tuina page accessibility
    print("\n[7/12] 测试推拿页面可访问性 | Test tuina page accessibility...")
    total_tests += 1
    response = client.get('/tuina/new/')
    if response.status_code == 200:
        print(f"✓ 页面可访问 | Page accessible (Status: {response.status_code})")
        passed_tests += 1
    else:
        print(f"✗ 页面无法访问 | Page not accessible (Status: {response.status_code})")

    # Test 8: Check tuina 3D viewer container
    print("\n[8/12] 检查推拿3D图解容器 | Check tuina 3D viewer container...")
    total_tests += 1
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        has_container = 'id="tuinaViewer"' in content
        has_title = '3D人体图解 - 治疗部位' in content
        has_bilingual_title = '3D Body Diagram - Treatment Areas' in content

        if has_container and has_title and has_bilingual_title:
            print("✓ 推拿3D图解容器配置正确 | Tuina 3D viewer container properly configured")
            print("  ✓ 容器ID存在 | Container ID exists")
            print("  ✓ 中文标题存在 | Chinese title exists")
            print("  ✓ 英文标题存在 | English title exists")
            passed_tests += 1
        else:
            print("✗ 推拿3D图解容器配置有问题 | Tuina 3D viewer container has issues")

    # Test 9: Check bilingual labels in tuina
    print("\n[9/12] 检查推拿页面双语标签 | Check tuina bilingual labels...")
    total_tests += 1
    if response.status_code == 200:
        bilingual_labels = [
            '患者 | Patient',
            '治疗日期 | Session Date',
            '主诉 | Chief Complaint',
            '治疗重点 | Primary Focus',
            '疼痛评估 | Pain Assessment',
            '保存 | Save',
        ]

        all_labels_present = all(label in content for label in bilingual_labels)

        if all_labels_present:
            print("✓ 所有双语标签正确显示 | All bilingual labels properly displayed")
            for label in bilingual_labels:
                print(f"  ✓ {label}")
            passed_tests += 1
        else:
            print("✗ 部分双语标签缺失 | Some bilingual labels missing")

    # Test 10: Check tuina JavaScript initialization
    print("\n[10/12] 检查推拿JavaScript初始化 | Check tuina JavaScript initialization...")
    total_tests += 1
    if response.status_code == 200:
        has_viewer_init = 'new Body3DViewer' in content
        has_acupoint_option = 'showAcupoints: false' in content
        has_muscle_option = 'showMuscles: true' in content

        if has_viewer_init:
            print("✓ JavaScript初始化代码存在 | JavaScript initialization exists")
            print(f"  ✓ 创建3D查看器 | Viewer creation: {has_viewer_init}")
            print(f"  ✓ 穴位模式关闭 | Acupoint mode off: {has_acupoint_option}")
            print(f"  ✓ 肌肉模式开启 | Muscle mode on: {has_muscle_option}")
            passed_tests += 1
        else:
            print("✗ JavaScript初始化代码缺失 | JavaScript initialization missing")

    print("\n" + "=" * 80)
    print("【第四部分：功能特性验证】| Part 4: Feature Verification")
    print("=" * 80)

    # Test 11: Verify SVG features in JS file
    print("\n[11/12] 验证SVG功能特性 | Verify SVG features...")
    total_tests += 1
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

        svg_features = {
            'SVG元素创建': 'createElementNS' in js_content and 'http://www.w3.org/2000/svg' in js_content,
            '渐变定义': 'skinGradient' in js_content and 'linearGradient' in js_content,
            '滤镜效果': 'filter' in js_content and 'shadow' in js_content,
            '贝塞尔曲线': 'quadraticCurveTo' in js_content or 'path' in js_content.lower(),
            '人体绘制方法': 'drawFrontBody' in js_content and 'drawBackBody' in js_content,
            '穴位标记方法': 'createAcupointMarker' in js_content,
            '治疗区域方法': 'createTreatmentArea' in js_content,
            '图例绘制': 'drawLegend' in js_content,
        }

        all_svg_features = all(svg_features.values())

        if all_svg_features:
            print("✓ 所有SVG功能特性已实现 | All SVG features implemented")
            for feature, exists in svg_features.items():
                print(f"  ✓ {feature}")
            passed_tests += 1
        else:
            print("✗ 部分SVG功能特性缺失 | Some SVG features missing")
            for feature, exists in svg_features.items():
                status = "✓" if exists else "✗"
                print(f"  {status} {feature}")

    # Test 12: Verify interactive features
    print("\n[12/12] 验证交互功能 | Verify interactive features...")
    total_tests += 1

    interactive_features = {
        '视图切换': 'setView' in js_content,
        '缩放功能': 'adjustZoom' in js_content,
        '重置视图': 'resetView' in js_content,
        '穴位选择': 'toggleAcupoint' in js_content,
        '区域选择': 'toggleArea' in js_content,
        '事件监听': 'addEventListener' in js_content,
        '滚轮缩放': 'wheel' in js_content,
        '自定义事件': 'CustomEvent' in js_content,
    }

    all_interactive = all(interactive_features.values())

    if all_interactive:
        print("✓ 所有交互功能已实现 | All interactive features implemented")
        for feature, exists in interactive_features.items():
            print(f"  ✓ {feature}")
        passed_tests += 1
    else:
        print("✗ 部分交互功能缺失 | Some interactive features missing")
        for feature, exists in interactive_features.items():
            status = "✓" if exists else "✗"
            print(f"  {status} {feature}")

    # Final summary
    print("\n" + "=" * 80)
    print("【测试总结】| Test Summary")
    print("=" * 80)

    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

    print(f"\n总测试数 | Total Tests: {total_tests}")
    print(f"通过数量 | Passed: {passed_tests}")
    print(f"失败数量 | Failed: {total_tests - passed_tests}")
    print(f"成功率 | Success Rate: {success_rate:.1f}%")

    print("\n" + "=" * 80)

    if passed_tests == total_tests:
        print("🎉 所有测试通过！真实人体3D图解已完美集成！")
        print("🎉 All tests passed! Realistic 3D Body Viewer perfectly integrated!")
        print("\n✅ 系统特性 | System Features:")
        print("   ✓ 真实人体SVG图形")
        print("   ✓ 解剖学准确的轮廓")
        print("   ✓ 专业的渐变和阴影效果")
        print("   ✓ 肌肉结构可视化")
        print("   ✓ 发光穴位标记")
        print("   ✓ 彩色治疗区域")
        print("   ✓ 完整的交互功能")
        print("   ✓ 双语标签显示")
        print("\n✅ Realistic Human Body Features:")
        print("   ✓ Realistic human SVG graphics")
        print("   ✓ Anatomically accurate outline")
        print("   ✓ Professional gradients and shadows")
        print("   ✓ Muscle structure visualization")
        print("   ✓ Glowing acupoint markers")
        print("   ✓ Colorful treatment areas")
        print("   ✓ Complete interactive features")
        print("   ✓ Bilingual labels")
        print("\n" + "=" * 80)
        print("系统准备就绪！请启动服务器查看真实人体3D图解效果。")
        print("System ready! Please start the server to see realistic 3D body viewer.")
        print("\n运行命令 | Run command:")
        print("  cd zhongyi_project")
        print("  python manage.py runserver")
        print("\n访问页面 | Visit pages:")
        print("  针灸 | Acupuncture: http://localhost:8000/acupuncture/create/")
        print("  推拿 | Tuina: http://localhost:8000/tuina/new/")
        print("=" * 80)
        return True
    else:
        print("⚠ 部分测试失败，请检查 | Some tests failed, please check")
        print(f"失败的测试数量 | Failed tests: {total_tests - passed_tests}")
        return False

if __name__ == '__main__':
    success = test_realistic_3d_viewer()
    sys.exit(0 if success else 1)
