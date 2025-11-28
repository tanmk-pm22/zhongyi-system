#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Final System Verification Test
最终系统验证测试
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

def final_verification():
    """Final verification of all critical features"""

    print("=" * 70)
    print("最终系统验证 | Final System Verification")
    print("=" * 70)

    client = Client(SERVER_NAME='localhost')

    # Create/get test user
    user = User.objects.filter(username='final_test_user').first()
    if not user:
        user = User.objects.create_user(
            username='final_test_user',
            password='testpass123',
            role='practitioner'
        )

    # Login
    client.login(username='final_test_user', password='testpass123')

    tests = [
        ("主页 | Homepage", "/"),
        ("患者列表 | Patient List", "/patients/"),
        ("诊断列表 | Diagnosis List", "/diagnosis/"),
        ("处方列表 | Prescription List", "/prescriptions/"),
        ("针灸列表 | Acupuncture List", "/acupuncture/"),
        ("针灸新建(含3D图解) | Acupuncture Create (with 3D)", "/acupuncture/create/"),
        ("穴位图库 | Acupoint Library", "/acupuncture/library/"),
        ("推拿列表 | Tuina List", "/tuina/"),
        ("推拿新建(含3D图解) | Tuina Create (with 3D)", "/tuina/new/"),
        ("拔罐列表 | Cupping List", "/cupping/"),
        ("体质辨识 | Constitution", "/constitution/"),
        ("疗程管理 | Treatment Course", "/treatment-course/"),
        ("预约管理 | Appointments", "/appointments/"),
    ]

    passed = 0
    total = len(tests)

    print(f"\n测试 {total} 个关键页面 | Testing {total} critical pages\n")

    for name, url in tests:
        response = client.get(url)
        status = "✓" if response.status_code == 200 else "✗"

        if response.status_code == 200:
            passed += 1
            print(f"{status} [{response.status_code}] {name}")

            # Extra checks for 3D viewer pages
            if "3D" in name:
                content = response.content.decode('utf-8')
                has_viewer = 'Body3DViewer' in content
                viewer_status = "✓ 包含3D图解" if has_viewer else "✗ 缺少3D图解"
                print(f"    {viewer_status}")
        else:
            print(f"{status} [{response.status_code}] {name}")

    print("\n" + "=" * 70)
    print(f"测试结果 | Test Results: {passed}/{total} 通过 | Passed")
    print("=" * 70)

    # Check critical features
    print("\n关键功能检查 | Critical Features Check:")

    features = []

    # Check 3D viewer JS exists
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'js', 'body-3d-viewer.js')
    features.append(("3D图解JS文件 | 3D Viewer JS", os.path.exists(js_path)))

    # Check templates exist
    acup_template = os.path.join(os.path.dirname(__file__), 'templates', 'acupuncture', 'acupuncturesession_form.html')
    features.append(("针灸表单模板 | Acupuncture Form", os.path.exists(acup_template)))

    tuina_template = os.path.join(os.path.dirname(__file__), 'templates', 'tuina', 'session_form.html')
    features.append(("推拿表单模板 | Tuina Form", os.path.exists(tuina_template)))

    # Check base template has JS
    base_template = os.path.join(os.path.dirname(__file__), 'templates', 'base.html')
    with open(base_template, 'r', encoding='utf-8') as f:
        base_content = f.read()
        features.append(("base.html包含3D JS | base.html has 3D JS", 'body-3d-viewer.js' in base_content))

    for feature_name, status in features:
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {feature_name}")

    all_passed = passed == total and all(status for _, status in features)

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 系统验证完成！所有功能正常！")
        print("🎉 System Verification Complete! All features working!")
        print("\n✅ 3D人体图解已成功集成到针灸和推拿模块")
        print("✅ 3D Body Viewer successfully integrated into acupuncture and tuina")
        print("\n可以开始使用系统 | System is ready to use")
    else:
        print("⚠ 部分功能需要检查 | Some features need attention")
    print("=" * 70)

    return all_passed

if __name__ == '__main__':
    success = final_verification()
    sys.exit(0 if success else 1)
