"""Tests for Patients app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Patient, MedicalRecord

User = get_user_model()


class PatientModelTests(TestCase):
    """Tests for Patient model."""

    def setUp(self):
        """Set up test practitioner."""
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
        )

    def test_create_patient(self):
        """Test creating a patient."""
        patient = Patient.objects.create(
            first_name='李',
            last_name='明',
            ic_number='900101-14-5678',
            date_of_birth='1990-01-01',
            gender='M',
            phone='0123456789',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )
        self.assertEqual(patient.first_name, '李')
        self.assertEqual(patient.last_name, '明')
        self.assertIsNotNone(patient.patient_id)

    def test_patient_full_name(self):
        """Test patient full_name property."""
        patient = Patient.objects.create(
            first_name='王',
            last_name='芳',
            ic_number='850515-14-1234',
            date_of_birth='1985-05-15',
            gender='F',
            phone='0129876543',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )
        self.assertEqual(patient.full_name, '王 芳')

    def test_patient_age_calculation(self):
        """Test patient age calculation."""
        from datetime import date
        patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            ic_number='000101-14-9999',
            date_of_birth=date(2000, 1, 1),
            gender='M',
            phone='0121234567',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )
        self.assertIsNotNone(patient.age)
        self.assertGreater(patient.age, 0)

    def test_patient_uuid_generation(self):
        """Test patient UUID is generated automatically."""
        patient = Patient.objects.create(
            first_name='Test',
            last_name='UUID',
            ic_number='950320-14-5555',
            date_of_birth='1995-03-20',
            gender='F',
            phone='0127654321',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )
        self.assertIsNotNone(patient.patient_id)
        self.assertEqual(len(str(patient.patient_id)), 36)

    def test_patient_pdpa_consent(self):
        """Test PDPA consent fields."""
        patient = Patient.objects.create(
            first_name='Consent',
            last_name='Test',
            ic_number='880808-14-8888',
            date_of_birth='1988-08-08',
            gender='M',
            phone='0128888888',
            address='Test Address',
            consent_data_sharing=True,
            consent_date=timezone.now(),
            assigned_practitioner=self.practitioner
        )
        self.assertTrue(patient.consent_data_sharing)
        self.assertIsNotNone(patient.consent_date)


class MedicalRecordModelTests(TestCase):
    """Tests for MedicalRecord model."""

    def setUp(self):
        """Set up test patient and practitioner."""
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
        )
        self.patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            ic_number='900101-01-1234',
            date_of_birth='1990-01-01',
            gender='M',
            phone='0123456789',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )

    def test_create_medical_record(self):
        """Test creating a medical record."""
        from django.utils import timezone
        record = MedicalRecord.objects.create(
            patient=self.patient,
            practitioner=self.practitioner,
            visit_date=timezone.now(),
            chief_complaint='头痛三天',
            record_type='initial'
        )
        self.assertEqual(record.chief_complaint, '头痛三天')
        self.assertEqual(record.patient, self.patient)

    def test_four_examinations(self):
        """Test four examinations fields."""
        from django.utils import timezone
        record = MedicalRecord.objects.create(
            patient=self.patient,
            practitioner=self.practitioner,
            visit_date=timezone.now(),
            chief_complaint='失眠一周',
            # Inspection (望诊)
            inspection_notes='神志清，面色萎黄',
            tongue_diagnosis='舌淡苔薄白',
            # Auscultation (闻诊)
            auscultation_notes='语声低微',
            # Inquiry (问诊)
            inquiry_notes='入睡困难',
            # Palpation (切诊)
            pulse_diagnosis='细弱'
        )
        self.assertEqual(record.inspection_notes, '神志清，面色萎黄')
        self.assertEqual(record.tongue_diagnosis, '舌淡苔薄白')
        self.assertEqual(record.pulse_diagnosis, '细弱')


class PatientViewTests(TestCase):
    """Tests for Patient views."""

    def setUp(self):
        """Set up test client and users."""
        self.client = Client()
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
        )
        self.patient_user = User.objects.create_user(
            username='patient',
            password='patientpass',
            role=User.Role.PATIENT
        )
        self.patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            ic_number='900101-14-0001',
            date_of_birth='1990-01-01',
            gender='M',
            phone='0120000001',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )

    def test_patient_list_requires_login(self):
        """Test patient list requires authentication."""
        response = self.client.get(reverse('patients:list'))
        self.assertEqual(response.status_code, 302)

    def test_patient_list_practitioner(self):
        """Test practitioner can view patient list."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('patients:list'))
        self.assertEqual(response.status_code, 200)

    def test_patient_detail_view(self):
        """Test patient detail view."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(
            reverse('patients:detail', kwargs={'pk': self.patient.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_patient_create_view(self):
        """Test patient create view is accessible."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('patients:create'))
        self.assertEqual(response.status_code, 200)


class PatientAPITests(TestCase):
    """Tests for Patient API endpoints."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.practitioner = User.objects.create_user(
            username='doctor',
            email='doctor@clinic.com',
            password='doctorpass',
            role=User.Role.PRACTITIONER
        )
        self.patient = Patient.objects.create(
            first_name='API',
            last_name='Test',
            ic_number='900101-14-3333',
            date_of_birth='1990-01-01',
            gender='M',
            phone='0123456789',
            address='Test Address',
            assigned_practitioner=self.practitioner
        )

    def test_api_patient_list(self):
        """Test patient list API."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, 200)

    def test_api_patient_detail(self):
        """Test patient detail API."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(f'/api/patients/{self.patient.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_api_patient_search(self):
        """Test patient search API."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get('/api/patients/search/?q=API')
        self.assertEqual(response.status_code, 200)

    def test_api_requires_auth(self):
        """Test API requires authentication."""
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, 403)


class PatientSearchTests(TestCase):
    """Tests for patient search functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
        )
        # Create multiple patients
        Patient.objects.create(
            first_name='张',
            last_name='三',
            ic_number='900101-14-1111',
            date_of_birth='1990-01-01',
            gender='M',
            phone='0123456789',
            address='Test Address 1',
            assigned_practitioner=self.practitioner
        )
        Patient.objects.create(
            first_name='李',
            last_name='四',
            ic_number='850515-14-2222',
            date_of_birth='1985-05-15',
            gender='F',
            phone='0198765432',
            address='Test Address 2',
            assigned_practitioner=self.practitioner
        )

    def test_search_by_name(self):
        """Test searching patients by name."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('patients:list') + '?q=张')
        self.assertEqual(response.status_code, 200)

    def test_search_by_phone(self):
        """Test searching patients by phone."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('patients:list') + '?q=0123')
        self.assertEqual(response.status_code, 200)
