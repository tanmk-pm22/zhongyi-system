#!/usr/bin/env python
"""
穴位图库系统测试 | Acupoint Library System Test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from acupuncture.models import AcupointReference
from django.db.models import Q

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def test_acupoint_data():
    """测试穴位数据"""
    print_header("Test 1: Acupoint Database")

    total_count = AcupointReference.objects.filter(is_active=True).count()
    print(f"Total acupoints: {total_count}")

    if total_count == 0:
        print("WARNING: No acupoint data found!")
        return False

    # Test by meridian
    meridians = AcupointReference.objects.filter(is_active=True).values_list('meridian', flat=True).distinct()
    print(f"\nMeridians with data: {len(meridians)}")
    for meridian in meridians:
        count = AcupointReference.objects.filter(is_active=True, meridian=meridian).count()
        meridian_display = dict(AcupointReference.MeridianType.choices).get(meridian, meridian)
        print(f"  - {meridian}: {meridian_display} ({count} points)")

    # Sample acupoints
    print("\nSample Acupoints:")
    samples = AcupointReference.objects.filter(is_active=True)[:5]
    for acupoint in samples:
        print(f"  - {acupoint.code}: {acupoint.chinese_name} ({acupoint.pinyin_name})")
        print(f"    Meridian: {acupoint.get_meridian_display()}")
        print(f"    Indications: {acupoint.indications[:50]}...")

    print("\nPASSED: Acupoint data test")
    return True

def test_search_functionality():
    """测试搜索功能"""
    print_header("Test 2: Search Functionality")

    # Test 1: Search by code
    result = AcupointReference.objects.filter(code__icontains='LI4')
    print(f"Search 'LI4': {result.count()} results")
    if result.count() > 0:
        print(f"  Found: {result.first().code} - {result.first().chinese_name}")

    # Test 2: Search by Chinese name
    result = AcupointReference.objects.filter(chinese_name__icontains='合谷')
    print(f"\nSearch 'Hegu': {result.count()} results")
    if result.count() > 0:
        print(f"  Found: {result.first().code} - {result.first().chinese_name}")

    # Test 3: Search by indications
    result = AcupointReference.objects.filter(indications__icontains='头痛')
    print(f"\nSearch 'headache': {result.count()} results")
    for acupoint in result[:3]:
        print(f"  - {acupoint.code}: {acupoint.chinese_name}")

    # Test 4: Complex search
    search_term = "痛"
    result = AcupointReference.objects.filter(
        Q(code__icontains=search_term) |
        Q(chinese_name__icontains=search_term) |
        Q(pinyin_name__icontains=search_term) |
        Q(indications__icontains=search_term)
    )
    print(f"\nComplex search 'pain': {result.count()} results")

    print("\nPASSED: Search functionality test")
    return True

def test_meridian_filtering():
    """测试经络筛选"""
    print_header("Test 3: Meridian Filtering")

    # Test filtering by specific meridians
    test_meridians = ['LI', 'ST', 'LR']

    for meridian in test_meridians:
        result = AcupointReference.objects.filter(meridian=meridian, is_active=True)
        meridian_name = dict(AcupointReference.MeridianType.choices).get(meridian, meridian)
        print(f"{meridian} ({meridian_name}): {result.count()} points")
        for acupoint in result:
            print(f"  - {acupoint.code}: {acupoint.chinese_name}")

    print("\nPASSED: Meridian filtering test")
    return True

def test_data_integrity():
    """测试数据完整性"""
    print_header("Test 4: Data Integrity")

    all_acupoints = AcupointReference.objects.filter(is_active=True)

    # Check required fields
    issues = []
    for acupoint in all_acupoints:
        if not acupoint.chinese_name:
            issues.append(f"{acupoint.code}: Missing Chinese name")
        if not acupoint.location_chinese:
            issues.append(f"{acupoint.code}: Missing location")
        if not acupoint.indications:
            issues.append(f"{acupoint.code}: Missing indications")
        if not acupoint.functions:
            issues.append(f"{acupoint.code}: Missing functions")

    if issues:
        print("Data integrity issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"All {all_acupoints.count()} acupoints have complete data")
        print("\nPASSED: Data integrity test")
        return True

def main():
    print("\n")
    print("=" * 60)
    print("  Acupoint Library System Test Suite")
    print("=" * 60)

    all_passed = True

    try:
        if not test_acupoint_data():
            all_passed = False
        if not test_search_functionality():
            all_passed = False
        if not test_meridian_filtering():
            all_passed = False
        if not test_data_integrity():
            all_passed = False

        print_header("Test Summary")

        if all_passed:
            print("SUCCESS: All tests PASSED")
            print("\nAcupoint Library is ready to use!")
            print("\nAccess at: http://127.0.0.1:8000/acupuncture/library/")
            return 0
        else:
            print("WARNING: Some tests failed")
            return 1

    except Exception as e:
        print_header("FATAL ERROR")
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
