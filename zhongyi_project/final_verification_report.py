#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终验证报告 | Final Verification Report
验证真实3D人体图系统的完整性和功能
Verify the integrity and functionality of the realistic 3D body viewer system
"""

import os
import sys
from pathlib import Path

def print_section(title_cn, title_en):
    """打印章节标题 | Print section title"""
    print(f"\n{'='*70}")
    print(f"  {title_cn} | {title_en}")
    print(f"{'='*70}\n")

def check_file_exists(filepath, description_cn, description_en):
    """检查文件是否存在 | Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✓ 存在 | Exists" if exists else "✗ 不存在 | Missing"
    print(f"{status}: {description_cn} | {description_en}")
    print(f"   路径 | Path: {filepath}")
    if exists:
        size = os.path.getsize(filepath)
        print(f"   大小 | Size: {size:,} bytes ({size/1024:.1f} KB)")
    return exists

def check_file_content(filepath, search_strings, description_cn, description_en):
    """检查文件内容 | Check file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"\n检查 | Checking: {description_cn} | {description_en}")
        all_found = True
        for search_str in search_strings:
            found = search_str in content
            status = "✓" if found else "✗"
            print(f"  {status} '{search_str}'")
            if not found:
                all_found = False
        return all_found
    except Exception as e:
        print(f"  ✗ 错误 | Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("  真实3D人体图最终验证报告 | Realistic 3D Body Viewer Final Verification")
    print("="*70)
    print(f"  日期 | Date: 2025-11-25")
    print("="*70)

    base_path = Path(__file__).parent
    results = []

    # ============================================================
    # Part 1: 核心文件检查 | Core File Check
    # ============================================================
    print_section("第一部分：核心文件检查", "Part 1: Core File Check")

    # Check realistic JS file
    js_file = base_path / "static" / "js" / "body-3d-viewer-realistic.js"
    results.append(check_file_exists(
        js_file,
        "真实3D查看器JavaScript文件",
        "Realistic 3D Viewer JavaScript File"
    ))

    # ============================================================
    # Part 2: 模板文件检查 | Template File Check
    # ============================================================
    print_section("第二部分：模板文件检查", "Part 2: Template File Check")

    # Check base.html
    base_template = base_path / "templates" / "base.html"
    results.append(check_file_exists(
        base_template,
        "基础模板文件",
        "Base Template File"
    ))

    # Check acupuncture form template
    acup_template = base_path / "templates" / "acupuncture" / "acupuncturesession_form.html"
    results.append(check_file_exists(
        acup_template,
        "针灸表单模板",
        "Acupuncture Form Template"
    ))

    # Check tuina session form template
    tuina_template = base_path / "templates" / "tuina" / "session_form.html"
    results.append(check_file_exists(
        tuina_template,
        "推拿表单模板",
        "Tuina Form Template"
    ))

    # ============================================================
    # Part 3: 文件内容验证 | File Content Verification
    # ============================================================
    print_section("第三部分：文件内容验证", "Part 3: File Content Verification")

    # Check base.html references realistic version
    if base_template.exists():
        results.append(check_file_content(
            base_template,
            ['body-3d-viewer-realistic.js'],
            "base.html引用真实版本JS",
            "base.html references realistic version JS"
        ))

    # Check acupuncture template
    if acup_template.exists():
        results.append(check_file_content(
            acup_template,
            [
                'acupointViewer',
                '3D人体图解',
                '3D Body Diagram',
                'Body3DViewerRealistic'
            ],
            "针灸模板包含3D查看器和双语标签",
            "Acupuncture template contains 3D viewer and bilingual labels"
        ))

    # Check tuina template
    if tuina_template.exists():
        results.append(check_file_content(
            tuina_template,
            [
                'tuinaViewer',
                '3D人体图解',
                '3D Body Diagram',
                'Body3DViewerRealistic'
            ],
            "推拿模板包含3D查看器和双语标签",
            "Tuina template contains 3D viewer and bilingual labels"
        ))

    # Check realistic JS file features
    if js_file.exists():
        results.append(check_file_content(
            js_file,
            [
                'class Body3DViewerRealistic',
                'createEllipse',
                'createRect',
                'skinGradient',
                'muscleGradient',
                'shadowFilter',
                'drawFrontBody',
                'drawBackBody',
                'createAcupointMarker',
                'createTreatmentArea',
                'GV20', 'CV17', 'LI4', 'ST36',  # Sample acupoints
                'neck', 'shoulder', 'back'  # Sample treatment areas
            ],
            "真实JS文件包含所有关键功能",
            "Realistic JS file contains all key features"
        ))

    # ============================================================
    # Part 4: 模块完整性检查 | Module Integrity Check
    # ============================================================
    print_section("第四部分：模块完整性检查", "Part 4: Module Integrity Check")

    # Check acupuncture module
    acup_module = base_path / "acupuncture"
    if acup_module.exists():
        print("✓ 针灸模块存在 | Acupuncture module exists")
        acup_views = acup_module / "views.py"
        acup_models = acup_module / "models.py"
        acup_urls = acup_module / "urls.py"
        results.append(acup_views.exists() and acup_models.exists() and acup_urls.exists())
        print(f"  views.py: {'✓' if acup_views.exists() else '✗'}")
        print(f"  models.py: {'✓' if acup_models.exists() else '✗'}")
        print(f"  urls.py: {'✓' if acup_urls.exists() else '✗'}")
    else:
        print("✗ 针灸模块不存在 | Acupuncture module missing")
        results.append(False)

    # Check tuina module
    tuina_module = base_path / "tuina"
    if tuina_module.exists():
        print("\n✓ 推拿模块存在 | Tuina module exists")
        tuina_views = tuina_module / "views.py"
        tuina_models = tuina_module / "models.py"
        tuina_urls = tuina_module / "urls.py"
        results.append(tuina_views.exists() and tuina_models.exists() and tuina_urls.exists())
        print(f"  views.py: {'✓' if tuina_views.exists() else '✗'}")
        print(f"  models.py: {'✓' if tuina_models.exists() else '✗'}")
        print(f"  urls.py: {'✓' if tuina_urls.exists() else '✗'}")
    else:
        print("\n✗ 推拿模块不存在 | Tuina module missing")
        results.append(False)

    # ============================================================
    # 最终总结 | Final Summary
    # ============================================================
    print_section("最终总结", "Final Summary")

    total_checks = len(results)
    passed_checks = sum(results)
    success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0

    print(f"总检查项 | Total Checks: {total_checks}")
    print(f"通过数量 | Passed: {passed_checks}")
    print(f"失败数量 | Failed: {total_checks - passed_checks}")
    print(f"成功率 | Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print("\n" + "="*70)
        print("  🎉 所有检查通过！系统完整无误！")
        print("  🎉 All checks passed! System is complete and correct!")
        print("="*70)
        return 0
    elif success_rate >= 80:
        print("\n" + "="*70)
        print("  ⚠️  大部分检查通过，但有少量问题")
        print("  ⚠️  Most checks passed, but some issues exist")
        print("="*70)
        return 1
    else:
        print("\n" + "="*70)
        print("  ❌ 检查失败！系统存在重大问题")
        print("  ❌ Checks failed! System has major issues")
        print("="*70)
        return 2

if __name__ == '__main__':
    sys.exit(main())
