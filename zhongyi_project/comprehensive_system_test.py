#!/usr/bin/env python
"""
Comprehensive Test Script for Enhanced Zhongyi TCM System
测试增强版中医系统的所有新功能

This script tests all newly implemented features:
1. Patient MedicalHistoryTimeline
2. Constitution Analysis Module
3. Cupping Therapy Module
4. Tuina/Massage Module
5. Treatment Course Management
6. Appointment System
7. Prescription Templates and Decoction Methods

Run this script after migrations are complete.
"""

import os
import sys
import django
from datetime import datetime, timedelta, date, time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

# Import all models
from patients.models import Patient, MedicalRecord, MedicalHistoryTimeline
from constitution.models import (
    ConstitutionType, ConstitutionQuestionnaire,
    ConstitutionAssessment, ConstitutionAssessmentAnswer
)
from cupping.models import CuppingTechnique, CuppingSession, CuppingSessionTechnique
from tuina.models import TuinaTechnique, TuinaSession, TuinaSessionTechnique
from treatment_course.models import TreatmentCourse, CourseSession
from appointments.models import (
    AppointmentType, PractitionerSchedule, Appointment
)
from prescriptions.models import (
    Herb, ClassicFormula, DecoctionMethod,
    PrescriptionTemplate, PrescriptionTemplateItem
)

User = get_user_model()


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_patient_history_timeline():
    """Test 1: Patient Medical History Timeline"""
    print_section("测试 1: 患者病史时间线 | Test 1: Patient Medical History Timeline")

    try:
        # Get or create a test patient
        patient = Patient.objects.first()
        if not patient:
            print("  ❌ No patients found. Please create a patient first.")
            return False

        print(f"  ✓ Found patient: {patient.full_name}")

        # Create a timeline event
        event = MedicalHistoryTimeline.objects.create(
            patient=patient,
            event_type='diagnosis',
            event_date=timezone.now(),
            title='首次诊断 | Initial Diagnosis',
            description='患者首次就诊，诊断为气虚质 | Patient first visit, diagnosed with Qi deficiency',
            is_important=True
        )

        print(f"  ✓ Created timeline event: {event.title}")

        # Query timeline
        timeline_count = MedicalHistoryTimeline.objects.filter(patient=patient).count()
        print(f"  ✓ Patient has {timeline_count} timeline event(s)")

        print("  ✅ Patient History Timeline: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Patient History Timeline: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_constitution_module():
    """Test 2: Constitution Analysis Module"""
    print_section("测试 2: 体质辨识模块 | Test 2: Constitution Analysis Module")

    try:
        # Create constitution types (9 types)
        constitution_types = [
            ('balanced', '平和质', 'Balanced Constitution'),
            ('qi_def', '气虚质', 'Qi Deficiency Constitution'),
            ('yang_def', '阳虚质', 'Yang Deficiency Constitution'),
            ('yin_def', '阴虚质', 'Yin Deficiency Constitution'),
            ('phlegm_damp', '痰湿质', 'Phlegm-Dampness Constitution'),
            ('damp_heat', '湿热质', 'Damp-Heat Constitution'),
            ('blood_stasis', '血瘀质', 'Blood Stasis Constitution'),
            ('qi_stag', '气郁质', 'Qi Stagnation Constitution'),
            ('special', '特禀质', 'Special Diathesis Constitution'),
        ]

        created_count = 0
        for code, name_cn, name_en in constitution_types:
            const_type, created = ConstitutionType.objects.get_or_create(
                code=code,
                defaults={
                    'name_cn': name_cn,
                    'name_en': name_en,
                    'description': f'{name_cn}的详细描述',
                    'display_order': created_count
                }
            )
            if created:
                created_count += 1

        print(f"  ✓ Created {created_count} constitution type(s)")

        total_types = ConstitutionType.objects.count()
        print(f"  ✓ Total constitution types in database: {total_types}")

        # Create assessment for a patient
        patient = Patient.objects.first()
        if patient:
            primary_const = ConstitutionType.objects.first()
            assessment = ConstitutionAssessment.objects.create(
                patient=patient,
                primary_constitution=primary_const,
                primary_score=75.5,
                scores={'qi_def': 75.5, 'balanced': 45.0}
            )
            print(f"  ✓ Created constitution assessment for {patient.full_name}")
            print(f"    Primary constitution: {primary_const.name_cn}")

        print("  ✅ Constitution Analysis Module: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Constitution Analysis Module: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_cupping_module():
    """Test 3: Cupping Therapy Module"""
    print_section("测试 3: 拔罐治疗模块 | Test 3: Cupping Therapy Module")

    try:
        # Create cupping techniques
        techniques = [
            ('retained', '留罐', 'Retained Cupping'),
            ('flash', '闪罐', 'Flash Cupping'),
            ('moving', '走罐', 'Moving Cupping'),
            ('bloodletting', '刺络拔罐', 'Bloodletting Cupping'),
        ]

        created_count = 0
        for code, name_cn, name_en in techniques:
            technique, created = CuppingTechnique.objects.get_or_create(
                code=code,
                defaults={
                    'name_cn': name_cn,
                    'name_en': name_en,
                    'description': f'{name_cn}的操作方法',
                    'typical_duration': 10
                }
            )
            if created:
                created_count += 1

        print(f"  ✓ Created {created_count} cupping technique(s)")

        # Create a cupping session
        patient = Patient.objects.first()
        practitioner = User.objects.filter(role='practitioner').first()

        if patient and practitioner:
            session = CuppingSession.objects.create(
                patient=patient,
                practitioner=practitioner,
                session_date=timezone.now(),
                chief_complaint='腰痛 | Lower back pain',
                tcm_diagnosis='寒湿痹痛 | Cold-Damp Bi Syndrome',
                duration_minutes=20,
                pain_level_before=7,
                pain_level_after=3
            )
            print(f"  ✓ Created cupping session for {patient.full_name}")
            print(f"    Pain improvement: {session.pain_level_before} → {session.pain_level_after}")

        total_sessions = CuppingSession.objects.count()
        print(f"  ✓ Total cupping sessions: {total_sessions}")

        print("  ✅ Cupping Therapy Module: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Cupping Therapy Module: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_tuina_module():
    """Test 4: Tuina/Massage Module"""
    print_section("测试 4: 推拿治疗模块 | Test 4: Tuina/Massage Module")

    try:
        # Create tuina techniques
        techniques = [
            ('tui', '推法', 'Pushing'),
            ('na', '拿法', 'Grasping'),
            ('an', '按法', 'Pressing'),
            ('mo', '摩法', 'Rubbing'),
            ('rou', '揉法', 'Kneading'),
        ]

        created_count = 0
        for code, name_cn, name_en in techniques:
            technique, created = TuinaTechnique.objects.get_or_create(
                code=code,
                defaults={
                    'name_cn': name_cn,
                    'name_en': name_en,
                    'category': '基本手法',
                    'description': f'{name_cn}的操作方法'
                }
            )
            if created:
                created_count += 1

        print(f"  ✓ Created {created_count} tuina technique(s)")

        # Create a tuina session
        patient = Patient.objects.first()
        practitioner = User.objects.filter(role='practitioner').first()

        if patient and practitioner:
            session = TuinaSession.objects.create(
                patient=patient,
                practitioner=practitioner,
                session_date=timezone.now(),
                chief_complaint='颈椎病 | Cervical spondylosis',
                tcm_diagnosis='气血瘀滞 | Qi and Blood Stagnation',
                primary_focus='颈部 | Neck',
                duration_minutes=30,
                pain_level_before=8,
                pain_level_after=4
            )
            print(f"  ✓ Created tuina session for {patient.full_name}")
            print(f"    Focus: {session.primary_focus}")

        total_sessions = TuinaSession.objects.count()
        print(f"  ✓ Total tuina sessions: {total_sessions}")

        print("  ✅ Tuina/Massage Module: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Tuina/Massage Module: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_treatment_course():
    """Test 5: Treatment Course Management"""
    print_section("测试 5: 疗程管理模块 | Test 5: Treatment Course Management")

    try:
        patient = Patient.objects.first()
        practitioner = User.objects.filter(role='practitioner').first()

        if not (patient and practitioner):
            print("  ❌ Need both patient and practitioner for this test")
            return False

        # Create a treatment course
        course = TreatmentCourse.objects.create(
            patient=patient,
            practitioner=practitioner,
            course_name='颈椎病综合治疗 | Comprehensive Cervical Treatment',
            primary_diagnosis='颈椎病 | Cervical Spondylosis',
            treatment_goal='缓解疼痛，改善活动度 | Relieve pain, improve mobility',
            treatment_plan='针灸+推拿+中药内服 | Acupuncture + Tuina + Herbal medicine',
            start_date=date.today(),
            planned_end_date=date.today() + timedelta(days=30),
            planned_sessions_total=10,
            planned_frequency='每周3次 | 3 times per week',
            includes_acupuncture=True,
            includes_tuina=True,
            includes_herbal_medicine=True,
            status='active'
        )

        print(f"  ✓ Created treatment course: {course.course_number}")
        print(f"    Course: {course.course_name}")
        print(f"    Planned sessions: {course.planned_sessions_total}")

        # Create a course session
        course_session = CourseSession.objects.create(
            course=course,
            session_number=1,
            session_type='acupuncture',
            scheduled_date=timezone.now(),
            status='completed'
        )

        print(f"  ✓ Created course session #{course_session.session_number}")
        print(f"    Progress: {course.progress_percentage}%")

        print("  ✅ Treatment Course Management: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Treatment Course Management: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_appointment_system():
    """Test 6: Appointment System"""
    print_section("测试 6: 预约管理系统 | Test 6: Appointment System")

    try:
        # Create appointment types
        apt_types = [
            ('initial', '初诊 | Initial Consultation', 60),
            ('followup', '复诊 | Follow-up', 30),
            ('acupuncture', '针灸治疗 | Acupuncture', 45),
            ('tuina', '推拿治疗 | Tuina', 30),
        ]

        created_count = 0
        for code, name, duration in apt_types:
            apt_type, created = AppointmentType.objects.get_or_create(
                code=code,
                defaults={
                    'name_cn': name.split(' | ')[0],
                    'name_en': name.split(' | ')[1],
                    'duration_minutes': duration
                }
            )
            if created:
                created_count += 1

        print(f"  ✓ Created {created_count} appointment type(s)")

        # Create practitioner schedule
        practitioner = User.objects.filter(role='practitioner').first()
        if practitioner:
            schedule, created = PractitionerSchedule.objects.get_or_create(
                practitioner=practitioner,
                day_of_week=1,  # Monday
                defaults={
                    'start_time': time(9, 0),
                    'end_time': time(17, 0),
                    'slot_duration_minutes': 30
                }
            )
            print(f"  ✓ Created schedule for {practitioner.get_full_name()} on Monday")

        # Create an appointment
        patient = Patient.objects.first()
        apt_type = AppointmentType.objects.first()

        if patient and practitioner and apt_type:
            appointment = Appointment.objects.create(
                patient=patient,
                practitioner=practitioner,
                appointment_type=apt_type,
                appointment_date=date.today() + timedelta(days=1),
                start_time=time(10, 0),
                end_time=time(10, 30),
                reason='定期检查 | Regular check-up',
                status='confirmed'
            )
            print(f"  ✓ Created appointment: {appointment.appointment_number}")
            print(f"    Date: {appointment.appointment_date} at {appointment.start_time}")

        total_appointments = Appointment.objects.count()
        print(f"  ✓ Total appointments: {total_appointments}")

        print("  ✅ Appointment System: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Appointment System: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_prescription_enhancements():
    """Test 7: Prescription Templates and Decoction Methods"""
    print_section("测试 7: 处方模板和煎药方法 | Test 7: Prescription Templates & Decoction")

    try:
        # Create decoction methods
        methods = [
            ('standard', '常规煎煮法 | Standard Decoction'),
            ('first_boil', '先煎法 | First Boil Method'),
            ('late_add', '后下法 | Late Addition Method'),
        ]

        created_count = 0
        for code, name in methods:
            method, created = DecoctionMethod.objects.get_or_create(
                code=code,
                defaults={
                    'name_cn': name.split(' | ')[0],
                    'name_en': name.split(' | ')[1],
                    'description': f'{name.split(" | ")[0]}的详细说明',
                    'first_decoction': '大火煮沸后转小火煎30分钟',
                    'second_decoction': '加水再煎20分钟'
                }
            )
            if created:
                created_count += 1

        print(f"  ✓ Created {created_count} decoction method(s)")

        # Create prescription template
        formula = ClassicFormula.objects.first()

        template, created = PrescriptionTemplate.objects.get_or_create(
            code='TEMPLATE001',
            defaults={
                'name_cn': '感冒基础方',
                'name_en': 'Common Cold Base Formula',
                'category': '感冒',
                'based_on_formula': formula,
                'is_public': True
            }
        )

        if created:
            print(f"  ✓ Created prescription template: {template.name_cn}")

            # Add herbs to template if available
            herb = Herb.objects.first()
            if herb:
                PrescriptionTemplateItem.objects.create(
                    template=template,
                    herb=herb,
                    dosage=10.0,
                    sequence=1
                )
                print(f"    Added herb: {herb.name_cn}")

        total_templates = PrescriptionTemplate.objects.count()
        print(f"  ✓ Total prescription templates: {total_templates}")

        print("  ✅ Prescription Enhancements: PASSED")
        return True

    except Exception as e:
        print(f"  ❌ Prescription Enhancements: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all comprehensive tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  增强版中医系统综合测试".center(74) + "  ║")
    print("║" + "  Zhongyi TCM System - Comprehensive Test Suite".center(74) + "  ║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    print(f"\n开始时间 | Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    tests = [
        ("患者病史时间线 | Patient History Timeline", test_patient_history_timeline),
        ("体质辨识模块 | Constitution Analysis", test_constitution_module),
        ("拔罐治疗模块 | Cupping Therapy", test_cupping_module),
        ("推拿治疗模块 | Tuina/Massage", test_tuina_module),
        ("疗程管理模块 | Treatment Course", test_treatment_course),
        ("预约管理系统 | Appointment System", test_appointment_system),
        ("处方模板和煎药 | Prescription Enhancements", test_prescription_enhancements),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {str(e)}")
            results.append((name, False))

    # Print summary
    print_section("测试总结 | Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n  测试结果 | Test Results:")
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"    {status} - {name}")

    print(f"\n  总计 | Total: {passed}/{total} tests passed")
    print(f"  成功率 | Success Rate: {(passed/total*100):.1f}%")

    print(f"\n完成时间 | Completion Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if passed == total:
        print("\n  🎉 所有测试通过！| All tests passed!")
        print("  ✅ 系统功能正常 | System is functioning correctly")
    else:
        print(f"\n  ⚠️  {total - passed} 个测试失败 | {total - passed} test(s) failed")
        print("  请检查错误信息并修复 | Please review errors and fix issues")

    print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n测试被中断 | Tests interrupted by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n严重错误 | Critical Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
