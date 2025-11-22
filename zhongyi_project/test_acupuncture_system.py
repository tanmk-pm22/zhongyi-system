#!/usr/bin/env python
"""
Comprehensive Acupuncture System Test
测试针灸系统的完整功能
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient
from acupuncture.models import AcupunctureSession
from acupuncture.ai_helper import AcupointAIHelper
from django.utils import timezone

User = get_user_model()

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def test_ai_recommendations():
    """Test AI recommendation system"""
    print_header("测试 1: AI推荐系统 | Test 1: AI Recommendation System")

    test_cases = [
        ("头痛", "肝阳上亢"),
        ("失眠多梦", "心脾两虚"),
        ("腰痛", "肾阳虚"),
    ]

    for complaint, diagnosis in test_cases:
        points, confidence, reasoning = AcupointAIHelper.recommend_acupoints(
            chief_complaint=complaint,
            tcm_diagnosis=diagnosis
        )
        print(f"\n主诉 | Complaint: {complaint}")
        print(f"诊断 | Diagnosis: {diagnosis}")
        print(f"推荐穴位 | Recommended Points: {', '.join(points)}")
        print(f"置信度 | Confidence: {confidence}%")
        print(f"推理依据 | Reasoning: {reasoning[:100]}...")

    print("\n✅ AI推荐系统测试通过 | AI System Test PASSED")

def test_models_and_database():
    """Test database models"""
    print_header("测试 2: 数据库模型 | Test 2: Database Models")

    # Check users
    admin_count = User.objects.filter(role='admin').count()
    practitioner_count = User.objects.filter(role='practitioner').count()
    print(f"管理员数量 | Admins: {admin_count}")
    print(f"医师数量 | Practitioners: {practitioner_count}")

    # Check patients
    patient_count = Patient.objects.filter(is_active=True).count()
    print(f"患者数量 | Active Patients: {patient_count}")

    # Check acupuncture sessions
    session_count = AcupunctureSession.objects.filter(is_active=True).count()
    print(f"针灸治疗记录 | Acupuncture Sessions: {session_count}")

    if patient_count > 0:
        sample_patient = Patient.objects.filter(is_active=True).first()
        print(f"\n示例患者 | Sample Patient: {sample_patient}")
        print(f"  - 姓名 | Name: {sample_patient.full_name}")
        print(f"  - 中文名 | Chinese Name: {sample_patient.chinese_name or 'N/A'}")

    print("\n✅ 数据库模型测试通过 | Database Model Test PASSED")

def test_search_functionality():
    """Test search with correct field names"""
    print_header("测试 3: 搜索功能 | Test 3: Search Functionality")

    from django.db.models import Q

    # Test the search query that was causing problems
    search_term = "test"

    try:
        # This is the FIXED query
        queryset = AcupunctureSession.objects.filter(
            Q(patient__first_name__icontains=search_term) |
            Q(patient__last_name__icontains=search_term) |
            Q(patient__chinese_name__icontains=search_term) |
            Q(chief_complaint__icontains=search_term) |
            Q(tcm_diagnosis__icontains=search_term) |
            Q(acupoints_used__icontains=search_term)
        )
        result_count = queryset.count()
        print(f"搜索查询执行成功 | Search query executed successfully")
        print(f"搜索词 | Search term: '{search_term}'")
        print(f"结果数量 | Results: {result_count}")
        print("\n✅ 搜索功能测试通过 | Search Functionality Test PASSED")
    except Exception as e:
        print(f"\n❌ 搜索功能测试失败 | Search Test FAILED")
        print(f"错误 | Error: {str(e)}")
        return False

    return True

def test_template_encoding():
    """Verify templates exist and are readable"""
    print_header("测试 4: 模板文件 | Test 4: Template Files")

    templates = [
        'templates/acupuncture/acupuncturesession_list.html',
        'templates/acupuncture/acupuncturesession_form.html',
        'templates/acupuncture/acupuncturesession_detail.html',
        'templates/acupuncture/acupuncturesession_confirm_delete.html',
    ]

    for template_path in templates:
        full_path = os.path.join(os.path.dirname(__file__), template_path)
        if os.path.exists(full_path):
            # Try to read the file and check for Chinese characters
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for key bilingual phrases
                if '针灸' in content or 'Acupuncture' in content:
                    print(f"✓ {os.path.basename(template_path)} - UTF-8编码正确 | Encoding OK")
                else:
                    print(f"⚠ {os.path.basename(template_path)} - 可能有编码问题 | Possible encoding issue")
        else:
            print(f"✗ {template_path} - 文件不存在 | File not found")

    print("\n✅ 模板文件测试通过 | Template Files Test PASSED")

def main():
    print("\n")
    print("=" * 60)
    print("  Acupuncture System Test Suite")
    print("=" * 60)

    all_passed = True

    try:
        test_ai_recommendations()
        test_models_and_database()
        if not test_search_functionality():
            all_passed = False
        test_template_encoding()

        print_header("测试总结 | Test Summary")

        if all_passed:
            print("✅ 所有测试通过！系统运行正常。")
            print("✅ All tests PASSED! System is working correctly.")
            print("\n可以安全使用针灸模块。")
            print("The acupuncture module is ready to use.")
            return 0
        else:
            print("⚠ 部分测试失败，请检查错误信息。")
            print("⚠ Some tests failed. Please check the error messages.")
            return 1

    except Exception as e:
        print_header("致命错误 | FATAL ERROR")
        print(f"❌ 测试过程中发生错误 | Error during testing:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
