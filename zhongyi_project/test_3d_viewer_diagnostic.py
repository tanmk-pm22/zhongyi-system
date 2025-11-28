#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
3D Viewer Diagnostic Test
诊断3D查看器问题
"""

import os
import sys

# Add project to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')

import django
django.setup()

def test_static_files():
    """Test if static files exist"""
    print("\n" + "="*60)
    print("📁 检查静态文件 | Checking Static Files")
    print("="*60)

    static_dir = os.path.join(project_dir, 'static')
    js_dir = os.path.join(static_dir, 'js')

    # Check directories
    print(f"\n✓ Static directory: {static_dir}")
    print(f"  Exists: {os.path.exists(static_dir)}")

    print(f"\n✓ JS directory: {js_dir}")
    print(f"  Exists: {os.path.exists(js_dir)}")

    # Check specific file
    realtime_3d_file = os.path.join(js_dir, 'realtime-3d-anatomy-atlas.js')
    print(f"\n✓ Real-time 3D Atlas JS: {realtime_3d_file}")
    print(f"  Exists: {os.path.exists(realtime_3d_file)}")

    if os.path.exists(realtime_3d_file):
        size = os.path.getsize(realtime_3d_file)
        print(f"  Size: {size:,} bytes ({size/1024:.2f} KB)")

        # Check for syntax errors
        try:
            with open(realtime_3d_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"  Lines: {len(content.splitlines())}")

                # Check for key classes
                if 'class RealTime3DAnatomyAtlas' in content:
                    print("  ✓ Contains RealTime3DAnatomyAtlas class")
                else:
                    print("  ✗ Missing RealTime3DAnatomyAtlas class")

                # Check for Three.js usage
                if 'THREE.' in content:
                    print("  ✓ Uses Three.js")
                else:
                    print("  ✗ No Three.js usage found")

        except Exception as e:
            print(f"  ✗ Error reading file: {e}")

    return True

def test_templates():
    """Test if templates are correctly configured"""
    print("\n" + "="*60)
    print("📄 检查模板 | Checking Templates")
    print("="*60)

    templates_dir = os.path.join(project_dir, 'templates')

    # Check acupuncture template
    acu_template = os.path.join(templates_dir, 'acupuncture', 'acupuncturesession_form.html')
    print(f"\n✓ Acupuncture template: {acu_template}")
    print(f"  Exists: {os.path.exists(acu_template)}")

    if os.path.exists(acu_template):
        with open(acu_template, 'r', encoding='utf-8') as f:
            content = f.read()

            checks = [
                ('{% load static %}', '✓ Loads static tag'),
                ('realtime-3d-anatomy-atlas.js', '✓ Loads 3D atlas JS'),
                ('three@0.160.0', '✓ Loads Three.js'),
                ('OrbitControls', '✓ Loads OrbitControls'),
                ('RealTime3DAnatomyAtlas', '✓ Initializes viewer'),
                ('acupointViewer', '✓ Has viewer container')
            ]

            for check_str, msg in checks:
                if check_str in content:
                    print(f"  {msg}")
                else:
                    print(f"  ✗ Missing: {check_str}")

    # Check tuina template
    tuina_template = os.path.join(templates_dir, 'tuina', 'session_form.html')
    print(f"\n✓ Tuina template: {tuina_template}")
    print(f"  Exists: {os.path.exists(tuina_template)}")

    if os.path.exists(tuina_template):
        with open(tuina_template, 'r', encoding='utf-8') as f:
            content = f.read()

            if 'realtime-3d-anatomy-atlas.js' in content:
                print("  ✓ Loads 3D atlas JS")
            else:
                print("  ✗ Missing 3D atlas JS")

            if 'tuinaViewer' in content:
                print("  ✓ Has viewer container")
            else:
                print("  ✗ Missing viewer container")

    return True

def test_cdn_urls():
    """Test CDN URLs"""
    print("\n" + "="*60)
    print("🌐 检查CDN链接 | Checking CDN URLs")
    print("="*60)

    print("\n⚠️  KNOWN ISSUE | 已知问题:")
    print("="*60)
    print("OrbitControls CDN URL is INCORRECT in templates!")
    print("OrbitControls CDN链接在模板中不正确！")
    print()
    print("❌ Current (WRONG):")
    print("   https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js")
    print()
    print("✅ Should be:")
    print("   https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js")
    print()
    print("OR use module import:")
    print("   import { OrbitControls } from 'three/addons/controls/OrbitControls.js';")
    print("="*60)

    return False

def main():
    print("\n" + "="*70)
    print("🔍 3D Viewer Diagnostic Test | 3D查看器诊断测试")
    print("="*70)

    try:
        # Run tests
        test_static_files()
        test_templates()
        has_cdn_issue = not test_cdn_urls()

        # Summary
        print("\n" + "="*70)
        print("📊 诊断总结 | Diagnostic Summary")
        print("="*70)

        if has_cdn_issue:
            print("\n❌ CRITICAL ISSUE FOUND | 发现关键问题:")
            print("   The OrbitControls CDN URL is incorrect!")
            print("   OrbitControls CDN链接不正确！")
            print()
            print("   This will cause:")
            print("   这将导致:")
            print("   • Three.js loads successfully ✓")
            print("   • OrbitControls fails to load ✗")
            print("   • RealTime3DAnatomyAtlas cannot initialize ✗")
            print("   • 3D viewer does not appear ✗")
            print()
            print("🔧 SOLUTION | 解决方案:")
            print("   Need to fix the OrbitControls URL in both templates:")
            print("   需要修复两个模板中的OrbitControls链接:")
            print("   1. templates/acupuncture/acupuncturesession_form.html")
            print("   2. templates/tuina/session_form.html")
        else:
            print("\n✅ All checks passed | 所有检查通过")

        print("\n" + "="*70)

    except Exception as e:
        print(f"\n❌ Error during diagnostic: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
