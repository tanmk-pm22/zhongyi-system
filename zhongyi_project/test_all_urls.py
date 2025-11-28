"""
Test all treatment module URLs
测试所有治疗模块URL
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_urls():
    """Test all new module URLs."""
    print("=" * 80)
    print("Testing All Treatment Module URLs")
    print("测试所有治疗模块URL")
    print("=" * 80)
    print()

    # Create test client with SERVER_NAME
    client = Client(SERVER_NAME='localhost')

    # Create or get test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'role': 'admin',
            'is_staff': True,
            'is_active': True,
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()

    # Login
    client.login(username='testuser', password='testpass123')

    # Test URLs
    urls_to_test = [
        ('/tuina/', '推拿治疗 | Tuina'),
        ('/cupping/', '拔罐治疗 | Cupping'),
        ('/constitution/', '体质辨识 | Constitution'),
        ('/constitution/assessment/new/', '体质评估 | Constitution Assessment'),
        ('/treatment-course/', '疗程管理 | Treatment Course'),
        ('/appointments/', '预约管理 | Appointments'),
        ('/appointments/calendar/', '预约日历 | Appointment Calendar'),
    ]

    results = []
    for url, name in urls_to_test:
        try:
            response = client.get(url)
            status = response.status_code
            if status == 200:
                results.append((name, url, '✓ PASS', status))
                print(f"✓ PASS - {name}")
                print(f"  URL: {url}")
                print(f"  Status: {status}")
            else:
                results.append((name, url, '✗ FAIL', status))
                print(f"✗ FAIL - {name}")
                print(f"  URL: {url}")
                print(f"  Status: {status}")
        except Exception as e:
            results.append((name, url, '✗ ERROR', str(e)))
            print(f"✗ ERROR - {name}")
            print(f"  URL: {url}")
            print(f"  Error: {str(e)}")
        print()

    # Summary
    print("=" * 80)
    print("Test Summary | 测试摘要")
    print("=" * 80)
    passed = sum(1 for r in results if r[2] == '✓ PASS')
    failed = sum(1 for r in results if r[2] in ['✗ FAIL', '✗ ERROR'])
    total = len(results)

    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print()

    if passed == total:
        print("🎉 All URLs are accessible!")
        print("🎉 所有URL都可以访问！")
    else:
        print("⚠️  Some URLs failed. Please check the errors above.")
        print("⚠️  部分URL失败。请检查上面的错误。")

    print("=" * 80)

    return passed == total

if __name__ == '__main__':
    success = test_urls()
    sys.exit(0 if success else 1)
