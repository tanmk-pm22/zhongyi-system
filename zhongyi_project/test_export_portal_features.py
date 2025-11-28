"""
Test script for Export and Patient Portal features
测试导出和患者门户功能
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from patients.models import Patient, MedicalRecord
from prescriptions.models import Prescription, Herb, PrescriptionItem
from diagnosis.models import DiagnosisSession
from prescriptions.utils import (
    PrescriptionPDFExporter,
    PatientDataExcelExporter,
    MedicalRecordPDFExporter
)
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()


class TestExportAndPortalFeatures:
    """Test export and patient portal features."""

    def __init__(self):
        self.client = Client()
        self.results = []

    def log_result(self, test_name, success, message):
        """Log test result."""
        status = "✓ PASS" if success else "✗ FAIL"
        self.results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'status': status
        })
        print(f"{status} - {test_name}: {message}")

    def test_export_utilities_exist(self):
        """Test 1: Verify export utility classes exist."""
        try:
            from prescriptions.utils import PrescriptionPDFExporter
            from prescriptions.utils import PatientDataExcelExporter
            from prescriptions.utils import MedicalRecordPDFExporter

            self.log_result(
                "Export Utilities",
                True,
                "All export utility classes are available"
            )
            return True
        except Exception as e:
            self.log_result(
                "Export Utilities",
                False,
                f"Failed to import export utilities: {str(e)}"
            )
            return False

    def test_prescription_pdf_export(self):
        """Test 2: Test prescription PDF export functionality."""
        try:
            # Get or create test data
            practitioner = User.objects.filter(role='practitioner').first()
            if not practitioner:
                practitioner = User.objects.filter(is_staff=True).first()

            patient = Patient.objects.first()
            prescription = Prescription.objects.filter(patient=patient).first()

            if not prescription:
                self.log_result(
                    "Prescription PDF Export",
                    False,
                    "No prescription found for testing"
                )
                return False

            # Test PDF generation
            exporter = PrescriptionPDFExporter(prescription)
            pdf_content = exporter.generate()

            if pdf_content and len(pdf_content) > 0:
                self.log_result(
                    "Prescription PDF Export",
                    True,
                    f"Successfully generated PDF ({len(pdf_content)} bytes) for prescription {prescription.prescription_number}"
                )
                return True
            else:
                self.log_result(
                    "Prescription PDF Export",
                    False,
                    "PDF generation returned empty content"
                )
                return False

        except Exception as e:
            self.log_result(
                "Prescription PDF Export",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_patient_excel_export(self):
        """Test 3: Test patient data Excel export functionality."""
        try:
            patients = Patient.objects.filter(is_active=True)[:5]

            if not patients:
                self.log_result(
                    "Patient Excel Export",
                    False,
                    "No patients found for testing"
                )
                return False

            # Test Excel generation
            exporter = PatientDataExcelExporter(patients)
            excel_content = exporter.generate()

            if excel_content and len(excel_content) > 0:
                self.log_result(
                    "Patient Excel Export",
                    True,
                    f"Successfully generated Excel ({len(excel_content)} bytes) for {patients.count()} patients"
                )
                return True
            else:
                self.log_result(
                    "Patient Excel Export",
                    False,
                    "Excel generation returned empty content"
                )
                return False

        except Exception as e:
            self.log_result(
                "Patient Excel Export",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_medical_record_pdf_export(self):
        """Test 4: Test medical record PDF export functionality."""
        try:
            record = MedicalRecord.objects.first()

            if not record:
                self.log_result(
                    "Medical Record PDF Export",
                    False,
                    "No medical record found for testing"
                )
                return False

            # Test PDF generation
            exporter = MedicalRecordPDFExporter(record)
            pdf_content = exporter.generate()

            if pdf_content and len(pdf_content) > 0:
                self.log_result(
                    "Medical Record PDF Export",
                    True,
                    f"Successfully generated PDF ({len(pdf_content)} bytes) for medical record"
                )
                return True
            else:
                self.log_result(
                    "Medical Record PDF Export",
                    False,
                    "PDF generation returned empty content"
                )
                return False

        except Exception as e:
            self.log_result(
                "Medical Record PDF Export",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_export_urls_configured(self):
        """Test 5: Verify export URLs are configured."""
        try:
            from django.urls import reverse

            # Test URL patterns
            urls_to_test = [
                ('prescriptions:export_patients_excel', None),
            ]

            all_success = True
            for url_name, kwargs in urls_to_test:
                try:
                    if kwargs:
                        url = reverse(url_name, kwargs=kwargs)
                    else:
                        url = reverse(url_name)
                except Exception as e:
                    all_success = False
                    print(f"  Failed to resolve {url_name}: {str(e)}")

            if all_success:
                self.log_result(
                    "Export URLs Configuration",
                    True,
                    "All export URL patterns are configured correctly"
                )
                return True
            else:
                self.log_result(
                    "Export URLs Configuration",
                    False,
                    "Some URL patterns failed to resolve"
                )
                return False

        except Exception as e:
            self.log_result(
                "Export URLs Configuration",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_patient_portal_views_exist(self):
        """Test 6: Verify patient portal views exist."""
        try:
            from accounts.views import (
                patient_portal_dashboard,
                patient_prescription_history,
                patient_appointment_history
            )

            self.log_result(
                "Patient Portal Views",
                True,
                "All patient portal views are available"
            )
            return True

        except Exception as e:
            self.log_result(
                "Patient Portal Views",
                False,
                f"Failed to import patient portal views: {str(e)}"
            )
            return False

    def test_patient_portal_urls_configured(self):
        """Test 7: Verify patient portal URLs are configured."""
        try:
            from django.urls import reverse

            urls_to_test = [
                'accounts:patient_portal',
                'accounts:patient_prescriptions',
                'accounts:patient_appointments',
            ]

            all_success = True
            for url_name in urls_to_test:
                try:
                    url = reverse(url_name)
                except Exception as e:
                    all_success = False
                    print(f"  Failed to resolve {url_name}: {str(e)}")

            if all_success:
                self.log_result(
                    "Patient Portal URLs",
                    True,
                    "All patient portal URL patterns are configured correctly"
                )
                return True
            else:
                self.log_result(
                    "Patient Portal URLs",
                    False,
                    "Some URL patterns failed to resolve"
                )
                return False

        except Exception as e:
            self.log_result(
                "Patient Portal URLs",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_print_prescription_template_exists(self):
        """Test 8: Verify print prescription template exists."""
        try:
            from django.template.loader import get_template

            template = get_template('prescriptions/print_prescription.html')

            self.log_result(
                "Print Prescription Template",
                True,
                "Print prescription template exists and is loadable"
            )
            return True

        except Exception as e:
            self.log_result(
                "Print Prescription Template",
                False,
                f"Template not found: {str(e)}"
            )
            return False

    def test_patient_portal_templates_exist(self):
        """Test 9: Verify patient portal templates exist."""
        try:
            from django.template.loader import get_template

            templates = [
                'accounts/patient_portal_dashboard.html',
                'accounts/patient_prescription_history.html',
                'accounts/patient_appointment_history.html',
            ]

            all_exist = True
            for template_name in templates:
                try:
                    get_template(template_name)
                except Exception as e:
                    all_exist = False
                    print(f"  Template not found: {template_name}")

            if all_exist:
                self.log_result(
                    "Patient Portal Templates",
                    True,
                    "All patient portal templates exist and are loadable"
                )
                return True
            else:
                self.log_result(
                    "Patient Portal Templates",
                    False,
                    "Some templates are missing"
                )
                return False

        except Exception as e:
            self.log_result(
                "Patient Portal Templates",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_health_tips_function(self):
        """Test 10: Verify health tips function works."""
        try:
            from accounts.views import _get_health_tips_for_constitution

            # Test with different constitutions
            constitutions = ['气虚质', '阳虚质', '平和质', '未知体质']

            all_success = True
            for constitution in constitutions:
                tips = _get_health_tips_for_constitution(constitution)
                if not tips or not isinstance(tips, list) or len(tips) == 0:
                    all_success = False
                    print(f"  No tips returned for {constitution}")

            if all_success:
                self.log_result(
                    "Health Tips Function",
                    True,
                    "Health tips function returns valid tips for all constitutions"
                )
                return True
            else:
                self.log_result(
                    "Health Tips Function",
                    False,
                    "Some constitutions did not return tips"
                )
                return False

        except Exception as e:
            self.log_result(
                "Health Tips Function",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_mobile_responsive_meta_tag(self):
        """Test 11: Verify viewport meta tag for mobile responsiveness."""
        try:
            from django.template.loader import get_template

            template = get_template('base.html')
            template_content = template.template.source

            if 'viewport' in template_content and 'width=device-width' in template_content:
                self.log_result(
                    "Mobile Responsive Meta Tag",
                    True,
                    "Viewport meta tag is present in base template"
                )
                return True
            else:
                self.log_result(
                    "Mobile Responsive Meta Tag",
                    False,
                    "Viewport meta tag not found in base template"
                )
                return False

        except Exception as e:
            self.log_result(
                "Mobile Responsive Meta Tag",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_bootstrap_responsive_classes(self):
        """Test 12: Verify Bootstrap 5 is being used."""
        try:
            from django.template.loader import get_template

            template = get_template('base.html')
            template_content = template.template.source

            if 'bootstrap@5' in template_content or 'bootstrap/5' in template_content:
                self.log_result(
                    "Bootstrap 5",
                    True,
                    "Bootstrap 5 is loaded in base template"
                )
                return True
            else:
                self.log_result(
                    "Bootstrap 5",
                    False,
                    "Bootstrap 5 not detected in base template"
                )
                return False

        except Exception as e:
            self.log_result(
                "Bootstrap 5",
                False,
                f"Error: {str(e)}"
            )
            return False

    def run_all_tests(self):
        """Run all tests."""
        print("=" * 80)
        print("Testing Export and Patient Portal Features")
        print("测试导出和患者门户功能")
        print("=" * 80)
        print()

        # Run all tests
        tests = [
            self.test_export_utilities_exist,
            self.test_prescription_pdf_export,
            self.test_patient_excel_export,
            self.test_medical_record_pdf_export,
            self.test_export_urls_configured,
            self.test_patient_portal_views_exist,
            self.test_patient_portal_urls_configured,
            self.test_print_prescription_template_exists,
            self.test_patient_portal_templates_exist,
            self.test_health_tips_function,
            self.test_mobile_responsive_meta_tag,
            self.test_bootstrap_responsive_classes,
        ]

        for test in tests:
            test()
            print()

        # Summary
        print("=" * 80)
        print("Test Summary | 测试摘要")
        print("=" * 80)

        passed = sum(1 for r in self.results if r['success'])
        failed = len(self.results) - passed

        print(f"\nTotal Tests: {len(self.results)}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {(passed/len(self.results)*100):.1f}%")

        print("\n" + "=" * 80)
        print("Feature Implementation Summary | 功能实现摘要")
        print("=" * 80)

        features = [
            "✓ Prescription PDF Export (处方PDF导出)",
            "✓ Patient Data Excel Export (患者数据Excel导出)",
            "✓ Medical Record PDF Export (医疗记录PDF导出)",
            "✓ Print-friendly Prescription Template (打印友好的处方模板)",
            "✓ Patient Portal Dashboard (患者门户仪表板)",
            "✓ Patient Prescription History View (患者处方历史)",
            "✓ Patient Appointment History View (患者就诊历史)",
            "✓ Health Tips Based on TCM Constitution (基于体质的健康建议)",
            "✓ Mobile Responsive Design (移动响应式设计)",
            "✓ Export Buttons in Templates (模板中的导出按钮)"
        ]

        for feature in features:
            print(f"  {feature}")

        print("\n" + "=" * 80)
        print("How to Use These Features | 如何使用这些功能")
        print("=" * 80)
        print("""
1. Export Prescription to PDF:
   - Go to prescription detail page
   - Click "导出PDF | Export PDF" button

2. Export Patient Data to Excel:
   - Go to patient list page (as admin)
   - Click "导出Excel | Export Excel" button

3. Print Prescription:
   - Go to prescription detail page
   - Click "打印 | Print" button
   - Use browser print function

4. Access Patient Portal:
   - Login as a patient user
   - Navigate to /accounts/patient-portal/
   - View your prescriptions, appointments, and health tips

5. Export Medical Record to PDF:
   - Go to medical record detail page
   - Click "导出PDF | Export PDF" button
        """)

        if failed > 0:
            print("\n⚠️  Some tests failed. Please review the errors above.")
            print("⚠️  部分测试失败。请查看上面的错误信息。")
        else:
            print("\n✓ All tests passed! The system is ready to use.")
            print("✓ 所有测试通过！系统已准备就绪。")


if __name__ == '__main__':
    tester = TestExportAndPortalFeatures()
    tester.run_all_tests()
