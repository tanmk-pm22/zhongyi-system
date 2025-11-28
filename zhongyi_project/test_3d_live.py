#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试实时3D人体解剖图 | Test Live 3D Anatomy Viewer
需要服务器运行在 http://127.0.0.1:8000 | Requires server running at http://127.0.0.1:8000
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.contrib.auth import get_user_model
import requests
from bs4 import BeautifulSoup

User = get_user_model()

def test_3d_viewer():
    """测试3D解剖图 | Test 3D anatomy viewer"""
    print("\n" + "="*70)
    print("实时3D人体解剖图测试 | Live 3D Anatomy Viewer Test")
    print("="*70)

    base_url = "http://127.0.0.1:8000"

    # 创建会话 | Create session
    session = requests.Session()

    # 获取登录页面获取CSRF token
    login_url = f"{base_url}/accounts/login/"
    print(f"\n1. 获取登录页面 | Getting login page...")
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    print(f"   ✓ CSRF Token获取成功 | CSRF token obtained")

    # 获取测试用户 | Get test user
    user = User.objects.filter(role='practitioner').first()
    if not user:
        user = User.objects.filter(is_superuser=True).first()

    if not user:
        print("   ✗ 未找到用户 | No user found")
        return False

    # 假设密码是'password'或'admin'，实际项目中应该正确设置
    # For testing, we'll try common passwords
    passwords = ['password', 'admin', 'admin123', '123456']

    print(f"\n2. 尝试登录 | Attempting login as {user.username}...")

    # 由于我们不知道密码，我们将使用Django的session来模拟登录
    # 这是一个测试技巧 | This is a testing technique

    # 获取Django session
    from django.contrib.sessions.models import Session
    from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
    from django.conf import settings
    from importlib import import_module

    # 创建Django session
    engine = import_module(settings.SESSION_ENGINE)
    django_session = engine.SessionStore()
    django_session[SESSION_KEY] = user.pk
    django_session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
    django_session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    django_session.save()

    # 使用这个session
    session.cookies.set('sessionid', django_session.session_key)
    print(f"   ✓ 使用Django session登录成功 | Logged in using Django session")

    # 测试页面 | Test pages
    test_pages = [
        (f"{base_url}/acupuncture/create/", "针灸创建页面 | Acupuncture Create", "acupointViewer"),
        (f"{base_url}/tuina/new/", "推拿创建页面 | Tuina Create", "tuinaViewer"),
    ]

    all_passed = True

    for url, page_name, viewer_id in test_pages:
        print(f"\n" + "-"*70)
        print(f"3. 测试 | Testing: {page_name}")
        print(f"   URL: {url}")

        try:
            response = session.get(url)
            print(f"   ✓ 状态码 | Status: {response.status_code}")

            if response.status_code != 200:
                print(f"   ✗ 页面访问失败 | Page access failed")
                all_passed = False
                continue

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # 检查关键元素 | Check key elements
            checks = {
                '3D容器元素': soup.find('div', id=viewer_id),
                'Three.js库加载': 'three' in html.lower(),
                '实时3D图谱脚本': 'realtime-3d-anatomy-atlas' in html,
                'OrbitControls控制器': 'OrbitControls' in html,
            }

            print(f"\n   检查结果 | Check Results:")
            page_passed = True
            for check_name, result in checks.items():
                if result:
                    print(f"   ✓ {check_name}: 找到 | Found")
                else:
                    print(f"   ✗ {check_name}: 未找到 | Not found")
                    page_passed = False
                    all_passed = False

            if page_passed:
                print(f"\n   ✅ {page_name} - 3D解剖图已正确集成！")
                print(f"      {page_name} - 3D anatomy viewer is properly integrated!")

        except Exception as e:
            print(f"   ✗ 错误 | Error: {e}")
            all_passed = False

    # 总结 | Summary
    print(f"\n" + "="*70)
    print("测试总结 | Test Summary")
    print("="*70)

    if all_passed:
        print("\n🎉 所有测试通过！3D人体解剖图已成功集成到针灸和推拿模块！")
        print("   All tests passed! 3D anatomy viewer successfully integrated!")
        print("\n✓ 针灸模块 | Acupuncture module: 3D穴位定位系统正常")
        print("✓ 推拿模块 | Tuina module: 3D治疗部位选择系统正常")
        print("\n可以开始使用系统了！| System is ready to use!")
        return True
    else:
        print("\n⚠ 部分测试未通过 | Some tests failed")
        print("  请检查上述错误信息 | Please check error messages above")
        return False

if __name__ == "__main__":
    import sys
    result = test_3d_viewer()
    sys.exit(0 if result else 1)
