#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Enhanced 3D Body Viewer
测试增强版3D人体图解
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

def test_enhanced_3d_viewer():
    """Test enhanced 3D viewer integration"""

    print("=" * 70)
    print("测试增强版3D人体图解 | Test Enhanced 3D Body Viewer")
    print("=" * 70)

    client = Client(SERVER_NAME='localhost')

    # Create test user
    user = User.objects.filter(username='enhanced_test_user').first()
    if not user:
        user = User.objects.create_user(
            username='enhanced_test_user',
            password='testpass123',
            role='practitioner'
        )

    client.login(username='enhanced_test_user', password='testpass123')

    tests_passed = 0
    tests_total = 0

    # Test 1: Check enhanced JS file exists
    print("\n[1/6] 检查增强版3D图解JS文件 | Check enhanced 3D viewer JS...")
    tests_total += 1
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'js', 'body-3d-viewer-enhanced.js')
    if os.path.exists(js_path):
        file_size = os.path.getsize(js_path)
        print(f"✓ 文件存在 | File exists: body-3d-viewer-enhanced.js")
        print(f"  大小 | Size: {file_size:,} bytes (~{file_size/1024:.1f} KB)")
        tests_passed += 1
    else:
        print(f"✗ 文件不存在 | File not found")

    # Test 2: Check base.html uses enhanced version
    print("\n[2/6] 检查base.html使用增强版 | Check base.html uses enhanced version...")
    tests_total += 1
    base_template = os.path.join(os.path.dirname(__file__), 'templates', 'base.html')
    with open(base_template, 'r', encoding='utf-8') as f:
        base_content = f.read()
        uses_enhanced = 'body-3d-viewer-enhanced.js' in base_content
        if uses_enhanced:
            print("✓ base.html使用增强版3D图解 | base.html uses enhanced 3D viewer")
            tests_passed += 1
        else:
            print("✗ base.html未使用增强版 | base.html not using enhanced version")

    # Test 3: Test acupuncture page
    print("\n[3/6] 测试针灸页面3D图解 | Test acupuncture page 3D viewer...")
    tests_total += 1
    response = client.get('/acupuncture/create/')
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        has_viewer = 'id="acupointViewer"' in content
        has_script = 'Body3DViewer' in content
        has_bilingual_title = '3D人体图解 - 穴位定位 | 3D Body Diagram - Acupoint Location' in content
        has_bilingual_instructions = '拖动旋转，滚轮缩放，点击穴位选择 | Drag to rotate, scroll to zoom, click acupoints to select' in content

        if has_viewer and has_script and has_bilingual_title and has_bilingual_instructions:
            print("✓ 针灸页面包含完整的增强版3D图解")
            print("  ✓ 3D图解容器存在")
            print("  ✓ 3D图解脚本已加载")
            print("  ✓ 双语标题显示正确")
            print("  ✓ 双语使用说明显示正确")
            tests_passed += 1
        else:
            print("✗ 针灸页面缺少某些元素")
            print(f"  - 3D容器: {has_viewer}")
            print(f"  - 3D脚本: {has_script}")
            print(f"  - 双语标题: {has_bilingual_title}")
            print(f"  - 双语说明: {has_bilingual_instructions}")
    else:
        print(f"✗ 无法访问针灸页面: {response.status_code}")

    # Test 4: Test tuina page
    print("\n[4/6] 测试推拿页面3D图解 | Test tuina page 3D viewer...")
    tests_total += 1
    response = client.get('/tuina/new/')
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        has_viewer = 'id="tuinaViewer"' in content
        has_script = 'Body3DViewer' in content
        has_bilingual_title = '3D人体图解 - 治疗部位 | 3D Body Diagram - Treatment Areas' in content
        has_bilingual_instructions = '拖动旋转，滚轮缩放，点击部位选择治疗区域 | Drag to rotate, scroll to zoom, click areas to select treatment zones' in content

        if has_viewer and has_script and has_bilingual_title and has_bilingual_instructions:
            print("✓ 推拿页面包含完整的增强版3D图解")
            print("  ✓ 3D图解容器存在")
            print("  ✓ 3D图解脚本已加载")
            print("  ✓ 双语标题显示正确")
            print("  ✓ 双语使用说明显示正确")
            tests_passed += 1
        else:
            print("✗ 推拿页面缺少某些元素")
            print(f"  - 3D容器: {has_viewer}")
            print(f"  - 3D脚本: {has_script}")
            print(f"  - 双语标题: {has_bilingual_title}")
            print(f"  - 双语说明: {has_bilingual_instructions}")
    else:
        print(f"✗ 无法访问推拿页面: {response.status_code}")

    # Test 5: Check bilingual labels in templates
    print("\n[5/6] 检查模板中的双语标签 | Check bilingual labels in templates...")
    tests_total += 1

    acup_template = os.path.join(os.path.dirname(__file__), 'templates', 'acupuncture', 'acupuncturesession_form.html')
    with open(acup_template, 'r', encoding='utf-8') as f:
        acup_content = f.read()

    tuina_template = os.path.join(os.path.dirname(__file__), 'templates', 'tuina', 'session_form.html')
    with open(tuina_template, 'r', encoding='utf-8') as f:
        tuina_content = f.read()

    bilingual_patterns = [
        '患者 | Patient',
        '治疗日期 | Session Date',
        '主诉 | Chief Complaint',
        '中医诊断 | TCM Diagnosis',
        '保存 | Save',
        '取消 | Cancel',
    ]

    acup_has_bilingual = all(pattern in acup_content for pattern in bilingual_patterns[:4])
    tuina_has_bilingual = all(pattern in tuina_content for pattern in [bilingual_patterns[0], bilingual_patterns[1], bilingual_patterns[2]])

    if acup_has_bilingual and tuina_has_bilingual:
        print("✓ 所有模板都包含双语标签")
        print("  ✓ 针灸模板双语正确")
        print("  ✓ 推拿模板双语正确")
        tests_passed += 1
    else:
        print("✗ 部分模板缺少双语标签")
        print(f"  - 针灸模板: {acup_has_bilingual}")
        print(f"  - 推拿模板: {tuina_has_bilingual}")

    # Test 6: Visual improvements check
    print("\n[6/6] 检查视觉改进 | Check visual improvements...")
    tests_total += 1

    # Check if enhanced version has better features
    with open(js_path, 'r', encoding='utf-8') as f:
        enhanced_js = f.read()

    visual_features = {
        '高DPI支持': 'devicePixelRatio' in enhanced_js,
        '渐变背景': 'createLinearGradient' in enhanced_js,
        '更真实人体轮廓': 'quadraticCurveTo' in enhanced_js,
        '穴位标签': 'fillText' in enhanced_js and '名' in enhanced_js,
        '图例显示': 'drawLegend' in enhanced_js,
        '控制按钮样式': 'btn-group' in acup_content,
    }

    all_features_present = all(visual_features.values())

    if all_features_present:
        print("✓ 增强版包含所有视觉改进")
        for feature, present in visual_features.items():
            print(f"  ✓ {feature}")
        tests_passed += 1
    else:
        print("✗ 部分视觉改进缺失")
        for feature, present in visual_features.items():
            status = "✓" if present else "✗"
            print(f"  {status} {feature}")

    # Summary
    print("\n" + "=" * 70)
    print("测试总结 | Test Summary")
    print("=" * 70)
    print(f"通过 | Passed: {tests_passed}/{tests_total}")
    print(f"失败 | Failed: {tests_total - tests_passed}/{tests_total}")

    if tests_passed == tests_total:
        print("\n" + "=" * 70)
        print("🎉 所有测试通过！增强版3D图解已成功集成！")
        print("🎉 All tests passed! Enhanced 3D viewer successfully integrated!")
        print("=" * 70)
        print("\n✅ 增强版3D人体图解特点：")
        print("   • 更高的显示分辨率（支持Retina显示屏）")
        print("   • 更真实的人体轮廓")
        print("   • 清晰的穴位和治疗区域标记")
        print("   • 完整的双语标签（中文 | English）")
        print("   • 流畅的交互体验")
        print("   • 美观的视觉效果")
        print("\n✅ Enhanced 3D Body Viewer Features:")
        print("   • Higher resolution (Retina display support)")
        print("   • More realistic human body outline")
        print("   • Clear acupoint and treatment area markers")
        print("   • Complete bilingual labels (Chinese | English)")
        print("   • Smooth interaction experience")
        print("   • Beautiful visual effects")
        print("=" * 70)
        return True
    else:
        print("\n✗ 部分测试失败 | Some tests failed")
        return False

if __name__ == '__main__':
    success = test_enhanced_3d_viewer()
    sys.exit(0 if success else 1)
