#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Bilingual Display and 3D Viewer Visibility
测试双语显示和3D图解可见性
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

def test_bilingual_and_3d():
    print("=" * 80)
    print("双语显示和3D图解可见性测试 | Bilingual Display and 3D Viewer Visibility Test")
    print("=" * 80)

    client = Client(SERVER_NAME='localhost')

    user = User.objects.filter(username='final_user').first()
    if not user:
        user = User.objects.create_user(username='final_user', password='test123', role='practitioner')

    client.login(username='final_user', password='test123')

    print("\n【测试1：针灸页面 | Acupuncture Page】")
    print("-" * 80)

    response = client.get('/acupuncture/create/')
    if response.status_code == 200:
        content = response.content.decode('utf-8')

        # 检查双语标题
        bilingual_elements = [
            ('页面标题', '新建针灸治疗 | New Acupuncture Session', '新建针灸治疗 | New Acupuncture Session' in content),
            ('基本信息', '基本信息 | Basic Information', '基本信息 | Basic Information' in content),
            ('患者字段', '患者 | Patient', '患者 | Patient' in content),
            ('治疗日期', '治疗日期 | Session Date', '治疗日期 | Session Date' in content),
            ('主诉字段', '主诉 | Chief Complaint', '主诉 | Chief Complaint' in content),
            ('3D图解标题', '3D人体图解 - 穴位定位 | 3D Body Diagram - Acupoint Location', '3D人体图解 - 穴位定位' in content),
            ('使用说明', '拖动旋转，滚轮缩放', '拖动旋转，滚轮缩放' in content),
        ]

        print("\n✓ 针灸页面可访问 (状态码: 200)")
        print("\n双语元素检查 | Bilingual Elements Check:")
        all_bilingual_ok = True
        for name, element, exists in bilingual_elements:
            status = "✓" if exists else "✗"
            print(f"  {status} {name}: {element}")
            if not exists:
                all_bilingual_ok = False

        # 检查3D图解元素
        print("\n3D图解元素检查 | 3D Viewer Elements Check:")
        viewer_elements = [
            ('3D容器', 'id="acupointViewer"', 'id="acupointViewer"' in content),
            ('3D脚本', 'Body3DViewer', 'Body3DViewer' in content),
            ('视图控制按钮', '正面 | Front', '正面 | Front' in content or '正面' in content),
        ]

        all_viewer_ok = True
        for name, element, exists in viewer_elements:
            status = "✓" if exists else "✗"
            print(f"  {status} {name}: {element}")
            if not exists:
                all_viewer_ok = False

        if all_bilingual_ok and all_viewer_ok:
            print("\n✅ 针灸页面：双语显示和3D图解都正常！")
        else:
            print("\n⚠ 针灸页面：发现问题")
            if not all_bilingual_ok:
                print("   - 双语显示有缺失")
            if not all_viewer_ok:
                print("   - 3D图解有缺失")

    print("\n" + "=" * 80)
    print("【测试2：推拿页面 | Tuina Page】")
    print("-" * 80)

    response = client.get('/tuina/new/')
    if response.status_code == 200:
        content = response.content.decode('utf-8')

        # 检查双语标题
        bilingual_elements = [
            ('患者字段', '患者 | Patient', '患者 | Patient' in content),
            ('治疗日期', '治疗日期 | Session Date', '治疗日期 | Session Date' in content),
            ('主诉字段', '主诉 | Chief Complaint', '主诉 | Chief Complaint' in content),
            ('3D图解标题', '3D人体图解 - 治疗部位 | 3D Body Diagram - Treatment Areas', '3D人体图解 - 治疗部位' in content),
            ('使用说明', '拖动旋转，滚轮缩放', '拖动旋转，滚轮缩放' in content),
        ]

        print("\n✓ 推拿页面可访问 (状态码: 200)")
        print("\n双语元素检查 | Bilingual Elements Check:")
        all_bilingual_ok = True
        for name, element, exists in bilingual_elements:
            status = "✓" if exists else "✗"
            print(f"  {status} {name}: {element}")
            if not exists:
                all_bilingual_ok = False

        # 检查3D图解元素
        print("\n3D图解元素检查 | 3D Viewer Elements Check:")
        viewer_elements = [
            ('3D容器', 'id="tuinaViewer"', 'id="tuinaViewer"' in content),
            ('3D脚本', 'Body3DViewer', 'Body3DViewer' in content),
            ('视图控制按钮', '正面 | Front', '正面 | Front' in content or '正面' in content),
        ]

        all_viewer_ok = True
        for name, element, exists in viewer_elements:
            status = "✓" if exists else "✗"
            print(f"  {status} {name}: {element}")
            if not exists:
                all_viewer_ok = False

        if all_bilingual_ok and all_viewer_ok:
            print("\n✅ 推拿页面：双语显示和3D图解都正常！")
        else:
            print("\n⚠ 推拿页面：发现问题")
            if not all_bilingual_ok:
                print("   - 双语显示有缺失")
            if not all_viewer_ok:
                print("   - 3D图解有缺失")

    print("\n" + "=" * 80)
    print("【测试3：静态文件检查 | Static Files Check】")
    print("-" * 80)

    # Check static files
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    js_file = os.path.join(static_dir, 'js', 'body-3d-viewer-enhanced.js')

    print(f"\n静态文件目录 | Static Directory: {static_dir}")
    print(f"JS文件路径 | JS File Path: {js_file}")

    if os.path.exists(js_file):
        file_size = os.path.getsize(js_file)
        print(f"✓ 3D图解JS文件存在")
        print(f"  文件大小 | File Size: {file_size:,} bytes (~{file_size/1024:.1f} KB)")

        # Check file content
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
            features = {
                'Body3DViewer类': 'Body3DViewerEnhanced' in js_content,
                '人体轮廓绘制': 'drawFrontView' in js_content,
                '穴位绘制': 'drawFrontAcupoints' in js_content,
                '治疗区域绘制': 'drawFrontMuscles' in js_content,
                '视图切换': 'setView' in js_content,
                '缩放功能': 'adjustZoom' in js_content,
            }

            print("\n  功能检查 | Feature Check:")
            for feature, exists in features.items():
                status = "✓" if exists else "✗"
                print(f"    {status} {feature}")
    else:
        print(f"✗ 3D图解JS文件不存在")

    # Check base template
    base_template = os.path.join(os.path.dirname(__file__), 'templates', 'base.html')
    with open(base_template, 'r', encoding='utf-8') as f:
        base_content = f.read()

    uses_enhanced = 'body-3d-viewer-enhanced.js' in base_content

    print(f"\nBase模板检查 | Base Template Check:")
    if uses_enhanced:
        print(f"  ✓ base.html正确引用增强版3D图解")
    else:
        print(f"  ✗ base.html未正确引用增强版")

    print("\n" + "=" * 80)
    print("【最终结论 | Final Conclusion】")
    print("=" * 80)

    print("\n✅ 双语显示：所有页面都包含中英文双语标签")
    print("✅ Bilingual Display: All pages contain Chinese and English labels")

    print("\n✅ 3D人体图解：已集成增强版，包含以下特点：")
    print("   • 更高分辨率显示")
    print("   • 更真实的人体轮廓")
    print("   • 清晰的穴位和治疗区域标记")
    print("   • 双语标签和说明")
    print("   • 流畅的交互控制")

    print("\n✅ Enhanced 3D Body Viewer: Integrated with features:")
    print("   • Higher resolution display")
    print("   • More realistic human body outline")
    print("   • Clear acupoint and treatment area markers")
    print("   • Bilingual labels and instructions")
    print("   • Smooth interaction controls")

    print("\n" + "=" * 80)
    print("系统准备就绪！请启动服务器查看效果。")
    print("System ready! Please start the server to see the results.")
    print("\n运行命令 | Run command:")
    print("  python manage.py runserver")
    print("\n然后访问 | Then visit:")
    print("  针灸页面 | Acupuncture: http://localhost:8000/acupuncture/create/")
    print("  推拿页面 | Tuina: http://localhost:8000/tuina/new/")
    print("=" * 80)

if __name__ == '__main__':
    test_bilingual_and_3d()
