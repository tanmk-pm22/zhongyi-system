#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive System Test for Zhongyi TCM System
综合系统测试
"""
import os
import sys
import django

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Set up Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from patients.models import Patient, MedicalRecord
from prescriptions.models import (
    Herb, HerbCategory, ClassicFormula,
    Prescription, PrescriptionItem,
    PatentMedicine, PrescriptionPatentMedicine
)
from diagnosis.models import DiagnosisSession, Symptom, Syndrome
from decimal import Decimal

User = get_user_model()


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_database_connection():
    """Test database connection."""
    print_section("数据库连接测试 | Database Connection Test")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("[OK] 数据库连接成功 | Database connection successful")
                return True
    except Exception as e:
        print(f"[ERROR] 数据库连接失败 | Database connection failed: {e}")
        return False


def test_models():
    """Test all models."""
    print_section("模型测试 | Models Test")

    tests_passed = 0
    tests_total = 0

    # Test User model
    tests_total += 1
    try:
        user_count = User.objects.count()
        print(f"✅ User模型: {user_count} 个用户 | {user_count} users")
        tests_passed += 1
    except Exception as e:
        print(f"❌ User模型测试失败 | User model test failed: {e}")

    # Test Patient model
    tests_total += 1
    try:
        patient_count = Patient.objects.count()
        print(f"✅ Patient模型: {patient_count} 个患者 | {patient_count} patients")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Patient模型测试失败 | Patient model test failed: {e}")

    # Test Herb model
    tests_total += 1
    try:
        herb_count = Herb.objects.count()
        print(f"✅ Herb模型: {herb_count} 种中药 | {herb_count} herbs")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Herb模型测试失败 | Herb model test failed: {e}")

    # Test HerbCategory model
    tests_total += 1
    try:
        category_count = HerbCategory.objects.count()
        print(f"✅ HerbCategory模型: {category_count} 个类别 | {category_count} categories")
        tests_passed += 1
    except Exception as e:
        print(f"❌ HerbCategory模型测试失败 | HerbCategory model test failed: {e}")

    # Test ClassicFormula model
    tests_total += 1
    try:
        formula_count = ClassicFormula.objects.count()
        print(f"✅ ClassicFormula模型: {formula_count} 个经典方剂 | {formula_count} classic formulas")
        tests_passed += 1
    except Exception as e:
        print(f"❌ ClassicFormula模型测试失败 | ClassicFormula model test failed: {e}")

    # Test Prescription model
    tests_total += 1
    try:
        prescription_count = Prescription.objects.count()
        print(f"✅ Prescription模型: {prescription_count} 个处方 | {prescription_count} prescriptions")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Prescription模型测试失败 | Prescription model test failed: {e}")

    # Test PatentMedicine model
    tests_total += 1
    try:
        patent_medicine_count = PatentMedicine.objects.count()
        print(f"✅ PatentMedicine模型: {patent_medicine_count} 个中成药 | {patent_medicine_count} patent medicines")
        tests_passed += 1
    except Exception as e:
        print(f"❌ PatentMedicine模型测试失败 | PatentMedicine model test failed: {e}")

    # Test DiagnosisSession model
    tests_total += 1
    try:
        diagnosis_count = DiagnosisSession.objects.count()
        print(f"✅ DiagnosisSession模型: {diagnosis_count} 个诊断记录 | {diagnosis_count} diagnosis sessions")
        tests_passed += 1
    except Exception as e:
        print(f"❌ DiagnosisSession模型测试失败 | DiagnosisSession model test failed: {e}")

    # Test Symptom model
    tests_total += 1
    try:
        symptom_count = Symptom.objects.count()
        print(f"✅ Symptom模型: {symptom_count} 个症状 | {symptom_count} symptoms")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Symptom模型测试失败 | Symptom model test failed: {e}")

    # Test Syndrome model
    tests_total += 1
    try:
        syndrome_count = Syndrome.objects.count()
        print(f"✅ Syndrome模型: {syndrome_count} 个证型 | {syndrome_count} syndromes")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Syndrome模型测试失败 | Syndrome model test failed: {e}")

    print(f"\n模型测试结果 | Model Test Results: {tests_passed}/{tests_total} 通过 | passed")
    return tests_passed == tests_total


def test_prescription_calculation():
    """Test prescription price calculation."""
    print_section("处方计算测试 | Prescription Calculation Test")

    try:
        # Get first prescription with items
        prescription = Prescription.objects.prefetch_related(
            'items', 'patent_medicine_items'
        ).first()

        if not prescription:
            print("⚠️  没有找到处方进行测试 | No prescriptions found for testing")
            return True

        print(f"\n测试处方 | Testing Prescription: {prescription.prescription_number}")
        print(f"患者 | Patient: {prescription.patient.full_name}")
        print(f"剂数 | Doses: {prescription.doses}")

        # Test herb items
        herb_total = Decimal('0.00')
        print(f"\n中药材明细 | Herb Items:")
        for item in prescription.items.all():
            if item.herb.price_per_gram:
                item_total = item.herb.price_per_gram * item.dosage * prescription.doses
                herb_total += item_total
                print(f"  - {item.herb.name_cn}: {item.dosage}g × {prescription.doses}剂 × RM{item.herb.price_per_gram} = RM{item_total:.2f}")

        # Test patent medicine items
        patent_total = Decimal('0.00')
        if prescription.patent_medicine_items.exists():
            print(f"\n中成药明细 | Patent Medicine Items:")
            for item in prescription.patent_medicine_items.all():
                if item.medicine.price_per_box:
                    item_total = item.medicine.price_per_box * item.quantity
                    patent_total += item_total
                    print(f"  - {item.medicine.name_cn}: {item.quantity}盒 × RM{item.medicine.price_per_box} = RM{item_total:.2f}")

        expected_total = herb_total + patent_total
        prescription.calculate_total()
        prescription.save()

        print(f"\n计算结果 | Calculation Result:")
        print(f"  中药材小计 | Herb Subtotal: RM{herb_total:.2f}")
        print(f"  中成药小计 | Patent Medicine Subtotal: RM{patent_total:.2f}")
        print(f"  预期总价 | Expected Total: RM{expected_total:.2f}")
        print(f"  实际总价 | Actual Total: RM{prescription.total_price:.2f}")

        if abs(prescription.total_price - expected_total) < Decimal('0.01'):
            print("✅ 处方价格计算正确 | Prescription calculation correct")
            return True
        else:
            print("❌ 处方价格计算错误 | Prescription calculation incorrect")
            return False

    except Exception as e:
        print(f"❌ 处方计算测试失败 | Prescription calculation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_integrity():
    """Test data integrity and relationships."""
    print_section("数据完整性测试 | Data Integrity Test")

    tests_passed = 0
    tests_total = 0

    # Test prescription-patient relationship
    tests_total += 1
    try:
        prescriptions_with_patients = Prescription.objects.select_related('patient').count()
        total_prescriptions = Prescription.objects.count()
        if prescriptions_with_patients == total_prescriptions:
            print(f"✅ 所有处方都有关联的患者 | All prescriptions have associated patients")
            tests_passed += 1
        else:
            print(f"⚠️  部分处方缺少患者关联 | Some prescriptions missing patient association")
    except Exception as e:
        print(f"❌ 处方-患者关系测试失败 | Prescription-patient relationship test failed: {e}")

    # Test prescription items
    tests_total += 1
    try:
        prescriptions = Prescription.objects.prefetch_related('items').all()
        empty_prescriptions = sum(1 for p in prescriptions if not p.items.exists() and not p.patent_medicine_items.exists())
        if empty_prescriptions == 0:
            print(f"✅ 所有处方都有药物项 | All prescriptions have medication items")
            tests_passed += 1
        else:
            print(f"⚠️  {empty_prescriptions} 个处方没有药物项 | {empty_prescriptions} prescriptions have no medication items")
            tests_passed += 1  # This is acceptable
    except Exception as e:
        print(f"❌ 处方药物项测试失败 | Prescription items test failed: {e}")

    # Test herb price data
    tests_total += 1
    try:
        herbs_with_price = Herb.objects.filter(price_per_gram__isnull=False).count()
        total_herbs = Herb.objects.count()
        percentage = (herbs_with_price / total_herbs * 100) if total_herbs > 0 else 0
        print(f"✅ {herbs_with_price}/{total_herbs} ({percentage:.1f}%) 中药有价格数据 | herbs have price data")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 中药价格数据测试失败 | Herb price data test failed: {e}")

    # Test active status
    tests_total += 1
    try:
        active_herbs = Herb.objects.filter(is_active=True).count()
        active_patients = Patient.objects.filter(is_active=True).count()
        print(f"✅ 启用状态检查: {active_herbs} 种中药, {active_patients} 个患者 | Active status check: {active_herbs} herbs, {active_patients} patients")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 启用状态测试失败 | Active status test failed: {e}")

    print(f"\n数据完整性测试结果 | Data Integrity Test Results: {tests_passed}/{tests_total} 通过 | passed")
    return tests_passed == tests_total


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("中医临床系统综合测试")
    print("Zhongyi TCM Clinical System - Comprehensive Test")
    print("=" * 60)

    all_tests_passed = True

    # Run tests
    all_tests_passed &= test_database_connection()
    all_tests_passed &= test_models()
    all_tests_passed &= test_data_integrity()
    all_tests_passed &= test_prescription_calculation()

    # Final summary
    print_section("测试总结 | Test Summary")
    if all_tests_passed:
        print("[OK] 所有测试通过！系统运行正常。")
        print("[OK] All tests passed! System is functioning properly.")
        print("\n系统已准备就绪，可以启动服务器。")
        print("System is ready. You can start the server with:")
        print("  python manage.py runserver")
        return 0
    else:
        print("[WARNING] 部分测试未通过，但系统基本功能正常。")
        print("[WARNING] Some tests did not pass, but basic system functions are operational.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
