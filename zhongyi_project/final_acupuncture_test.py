#!/usr/bin/env python
"""
Final Acupuncture System Comprehensive Test
针灸系统最终综合测试
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from acupuncture.models import AcupunctureSession, AcupointReference
from acupuncture.ai_helper import AcupointAIHelper
import urllib.request

def test_acupoint_library():
    """Test acupoint library"""
    print("=" * 60)
    print("Test 1: Acupoint Library (穴位图库)")
    print("=" * 60)

    count = AcupointReference.objects.filter(is_active=True).count()
    print(f"Acupoints in library: {count}")

    if count >= 10:
        print("SUCCESS: 10 sample acupoints loaded")

        # Show sample
        samples = AcupointReference.objects.filter(is_active=True)[:3]
        print("\nSample Acupoints:")
        for acupoint in samples:
            print(f"  - {acupoint.code}: {acupoint.chinese_name} ({acupoint.get_meridian_display()})")
        return True
    else:
        print(f"ERROR: Expected 10+ acupoints, found {count}")
        return False

def test_ai_system():
    """Test AI recommendation"""
    print("\n" + "=" * 60)
    print("Test 2: AI Recommendation System (AI推荐系统)")
    print("=" * 60)

    try:
        points, confidence, reasoning = AcupointAIHelper.recommend_acupoints(
            chief_complaint='headache',
            tcm_diagnosis='liver yang rising'
        )
        print(f"Test case: headache + liver yang rising")
        print(f"Recommended points: {', '.join(points)}")
        print(f"Confidence: {confidence}%")

        if len(points) > 0 and confidence >= 60:
            print("SUCCESS: AI system working correctly")
            return True
        else:
            print(f"ERROR: AI system not working properly (confidence: {confidence})")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_urls():
    """Test URL accessibility"""
    print("\n" + "=" * 60)
    print("Test 3: URL Accessibility (URL访问测试)")
    print("=" * 60)

    urls = [
        ('Acupuncture Sessions', 'http://127.0.0.1:8000/acupuncture/'),
        ('Acupoint Library', 'http://127.0.0.1:8000/acupuncture/library/'),
        ('Acupoint Detail', 'http://127.0.0.1:8000/acupuncture/library/LI4/'),
    ]

    all_passed = True
    for name, url in urls:
        try:
            response = urllib.request.urlopen(url, timeout=5)
            status = response.getcode()
            if status in [200, 302]:
                print(f"  - {name}: HTTP {status} - OK")
            else:
                print(f"  - {name}: HTTP {status} - Unexpected")
                all_passed = False
        except Exception as e:
            print(f"  - {name}: ERROR - {e}")
            all_passed = False

    if all_passed:
        print("SUCCESS: All URLs accessible")
    return all_passed

def test_database_models():
    """Test database models"""
    print("\n" + "=" * 60)
    print("Test 4: Database Models (数据库模型)")
    print("=" * 60)

    # Test AcupunctureSession model
    session_count = AcupunctureSession.objects.filter(is_active=True).count()
    print(f"Acupuncture sessions: {session_count}")

    # Test AcupointReference model
    acupoint_count = AcupointReference.objects.filter(is_active=True).count()
    print(f"Acupoint references: {acupoint_count}")

    # Test meridian types
    meridians = AcupointReference.objects.filter(is_active=True).values_list('meridian', flat=True).distinct()
    print(f"Meridians with data: {len(meridians)}")

    if acupoint_count >= 10:
        print("SUCCESS: Database models working correctly")
        return True
    else:
        print("ERROR: Insufficient data")
        return False

def main():
    print("\n")
    print("*" * 60)
    print("  FINAL ACUPUNCTURE SYSTEM TEST")
    print("  针灸系统最终测试")
    print("*" * 60)

    results = []
    results.append(("Acupoint Library", test_acupoint_library()))
    results.append(("AI System", test_ai_system()))
    results.append(("URL Access", test_urls()))
    results.append(("Database Models", test_database_models()))

    print("\n" + "=" * 60)
    print("FINAL RESULTS (最终结果)")
    print("=" * 60)

    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {name}: {status}")

    all_passed = all(result[1] for result in results)

    print("=" * 60)
    if all_passed:
        print("\n✅ ALL TESTS PASSED - SYSTEM READY")
        print("✅ 所有测试通过 - 系统就绪")
        print("\nAccess Acupoint Library at:")
        print("http://127.0.0.1:8000/acupuncture/library/")
        print("\n包含10个常用穴位的详细信息：")
        print("合谷(LI4), 足三里(ST36), 太冲(LR3), 内关(PC6), 三阴交(SP6),")
        print("风池(GB20), 百会(GV20), 神门(HT7), 肾俞(BL23), 关元(CV4)")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
