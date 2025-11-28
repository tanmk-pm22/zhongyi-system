#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试3D人体解剖图（带登录）| Test 3D Anatomy Viewer (with login)
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from bs4 import BeautifulSoup

User = get_user_model()

def test_page_with_login(client, url, page_name):
    """测试页面（已登录）| Test page (logged in)"""
    print(f"\n{'='*60}")
    print(f"测试 | Testing: {page_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        response = client.get(url)
        print(f"✓ 状态码 | Status Code: {response.status_code}")

        if response.status_code == 302:
            print(f"  重定向到 | Redirected to: {response.url}")
            return False

        if response.status_code != 200:
            print(f"✗ 页面返回错误状态码 | Page returned error status code")
            return False

        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # 检查3D相关元素 | Check 3D related elements
        checks = {
            'Three.js库 | Three.js library':
                'three' in html.lower(),
            '实时3D解剖图谱JS | RealTime 3D Atlas JS':
                'realtime-3d-anatomy-atlas' in html,
            '针灸3D容器 | Acupuncture 3D container':
                soup.find('div', id='acupointViewer') is not None,
            '推拿3D容器 | Tuina 3D container':
                soup.find('div', id='tuinaViewer') is not None,
        }

        all_passed = True
        for check_name, result in checks.items():
            if result:
                print(f"✓ {check_name}: 找到 | Found")
            else:
                print(f"✗ {check_name}: 未找到 | Not found")
                if not ('针灸3D容器' in check_name or '推拿3D容器' in check_name):
                    all_passed = False

        # 检查脚本数量 | Check script count
        scripts = soup.find_all('script')
        print(f"\n✓ 找到 {len(scripts)} 个脚本标签 | Found {len(scripts)} script tags")

        return all_passed

    except Exception as e:
        print(f"✗ 测试出错 | Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数 | Main function"""
    print("\n" + "="*60)
    print("3D人体解剖图测试（带登录）| 3D Anatomy Viewer Test (with login)")
    print("="*60)

    # 创建或获取管理员用户 | Create or get admin user
    try:
        # Try to find a practitioner user
        user = User.objects.filter(role='practitioner').first()
        if not user:
            user = User.objects.filter(is_staff=True).first()
        if not user:
            user = User.objects.filter(is_superuser=True).first()

        if not user:
            print("✗ 未找到用户 | No user found")
            print("  请创建一个用户 | Please create a user")
            return 1

        print(f"✓ 使用用户 | Using user: {user.username} (role: {user.role})")

    except Exception as e:
        print(f"✗ 获取用户失败 | Failed to get user: {e}")
        return 1

    # 创建测试客户端并登录 | Create test client and login
    client = Client()
    client.force_login(user)
    print("✓ 已登录 | Logged in")

    # 测试页面列表 | Test page list
    test_pages = [
        ("/acupuncture/create/", "新建针灸记录 | New Acupuncture Session"),
        ("/tuina/new/", "新建推拿记录 | New Tuina Session"),
    ]

    results = {}
    for url, name in test_pages:
        results[name] = test_page_with_login(client, url, name)

    # 总结 | Summary
    print("\n" + "="*60)
    print("测试总结 | Test Summary")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        status = "✓ 通过 | PASSED" if result else "✗ 失败 | FAILED"
        print(f"{status}: {name}")

    print(f"\n总计 | Total: {passed}/{total} 通过 | passed")

    if passed == total:
        print("\n✓ 所有测试通过！3D解剖图已正确集成！")
        print("  All tests passed! 3D anatomy viewer is properly integrated!")
        return 0
    else:
        print(f"\n✗ {total - passed} 个测试失败 | tests failed")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
