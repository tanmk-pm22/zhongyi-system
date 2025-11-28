"""
Test live server URLs with HTTP requests
通过HTTP请求测试实时服务器URL
"""
import requests
import time

def test_live_urls():
    """Test all URLs on live server."""
    print("=" * 80)
    print("Testing Live Server URLs")
    print("测试实时服务器URL")
    print("=" * 80)
    print()

    base_url = "http://127.0.0.1:8000"

    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)

    # Test URLs
    urls_to_test = [
        ('/', '首页 | Home'),
        ('/tuina/', '推拿治疗 | Tuina'),
        ('/cupping/', '拔罐治疗 | Cupping'),
        ('/constitution/', '体质辨识 | Constitution'),
        ('/constitution/assessment/new/', '体质评估 | Constitution Assessment'),
        ('/treatment-course/', '疗程管理 | Treatment Course'),
        ('/appointments/', '预约管理 | Appointments'),
        ('/appointments/calendar/', '预约日历 | Appointment Calendar'),
        ('/patients/', '患者管理 | Patients'),
        ('/diagnosis/', '诊断系统 | Diagnosis'),
        ('/prescriptions/', '处方管理 | Prescriptions'),
        ('/acupuncture/', '针灸治疗 | Acupuncture'),
    ]

    results = []
    for url_path, name in urls_to_test:
        try:
            url = base_url + url_path
            response = requests.get(url, timeout=5, allow_redirects=True)
            status = response.status_code

            # Check if redirected to login (expected for authenticated pages)
            if status == 200 or (status == 302 and '/accounts/login/' in response.url):
                results.append((name, url_path, '✓ PASS', status))
                print(f"✓ PASS - {name}")
                print(f"  URL: {url_path}")
                print(f"  Status: {status}")
                if status == 302:
                    print(f"  Note: Redirected to login (expected)")
            else:
                results.append((name, url_path, '✗ FAIL', status))
                print(f"✗ FAIL - {name}")
                print(f"  URL: {url_path}")
                print(f"  Status: {status}")
        except Exception as e:
            results.append((name, url_path, '✗ ERROR', str(e)))
            print(f"✗ ERROR - {name}")
            print(f"  URL: {url_path}")
            print(f"  Error: {str(e)[:100]}")
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
        print("🎉 All URLs are working correctly!")
        print("🎉 所有URL都正常工作！")
        print()
        print("Server is running at: http://127.0.0.1:8000/")
        print("服务器运行在: http://127.0.0.1:8000/")
    else:
        print("⚠️  Some URLs failed. Please check the errors above.")
        print("⚠️  部分URL失败。请检查上面的错误。")

    print("=" * 80)

    return passed == total

if __name__ == '__main__':
    import sys
    success = test_live_urls()
    sys.exit(0 if success else 1)
