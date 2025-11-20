"""Tests for diagnosis app."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from patients.models import Patient
from .models import (
    Symptom, Syndrome, SyndromeSysmptomWeight, DiagnosisSession
)
from .serializers import (
    SymptomSerializer, SyndromeSerializer,
    DiagnosisSessionSerializer, DiagnosisSessionCreateSerializer
)

User = get_user_model()


class SymptomModelTest(TestCase):
    """Test Symptom model."""

    def setUp(self):
        """Set up test data."""
        self.symptom = Symptom.objects.create(
            code='SYM001',
            name_en='Fever',
            name_cn='发热',
            category='general',
            description='Body temperature above normal'
        )

    def test_symptom_creation(self):
        """Test symptom is created successfully."""
        self.assertEqual(self.symptom.code, 'SYM001')
        self.assertEqual(self.symptom.name_en, 'Fever')
        self.assertEqual(self.symptom.name_cn, '发热')
        self.assertTrue(self.symptom.is_active)

    def test_symptom_str(self):
        """Test symptom string representation."""
        expected = f"{self.symptom.name_en} ({self.symptom.name_cn})"
        self.assertEqual(str(self.symptom), expected)


class SyndromeModelTest(TestCase):
    """Test Syndrome model."""

    def setUp(self):
        """Set up test data."""
        self.syndrome = Syndrome.objects.create(
            code='SYN001',
            name_en='Wind-Cold Exterior Pattern',
            name_cn='风寒表证',
            category='exterior',
            description='Wind-cold attacking the exterior',
            treatment_principle='Release the exterior and dispel cold'
        )

        self.symptom1 = Symptom.objects.create(
            code='SYM001',
            name_en='Chills',
            name_cn='恶寒',
            category='general'
        )

        self.symptom2 = Symptom.objects.create(
            code='SYM002',
            name_en='Fever',
            name_cn='发热',
            category='general'
        )

    def test_syndrome_creation(self):
        """Test syndrome is created successfully."""
        self.assertEqual(self.syndrome.code, 'SYN001')
        self.assertEqual(self.syndrome.name_cn, '风寒表证')
        self.assertTrue(self.syndrome.is_active)

    def test_syndrome_symptom_relationship(self):
        """Test many-to-many relationship with symptoms."""
        SyndromeSysmptomWeight.objects.create(
            syndrome=self.syndrome,
            symptom=self.symptom1,
            weight=2.0,
            is_primary=True
        )
        SyndromeSysmptomWeight.objects.create(
            syndrome=self.syndrome,
            symptom=self.symptom2,
            weight=1.5,
            is_primary=False
        )

        self.assertEqual(self.syndrome.symptoms.count(), 2)
        self.assertIn(self.symptom1, self.syndrome.symptoms.all())


class DiagnosisSessionModelTest(TestCase):
    """Test DiagnosisSession model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testpractitioner',
            email='practitioner@test.com',
            password='testpass123',
            role='practitioner',
            first_name='Test',
            last_name='Practitioner'
        )

        self.patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            chinese_name='测试患者',
            ic_number='123456-78-9012',
            phone='0123456789',
            gender='male',
            date_of_birth='1990-01-01'
        )

        self.session = DiagnosisSession.objects.create(
            patient=self.patient,
            practitioner=self.user,
            chief_complaint='Fever and chills',
            tongue_body_color='red',
            tongue_coating_color='white',
            selected_symptoms=['SYM001', 'SYM002']
        )

    def test_diagnosis_session_creation(self):
        """Test diagnosis session is created successfully."""
        self.assertEqual(self.session.patient, self.patient)
        self.assertEqual(self.session.practitioner, self.user)
        self.assertEqual(self.session.chief_complaint, 'Fever and chills')
        self.assertFalse(self.session.is_complete)

    def test_diagnosis_session_str(self):
        """Test diagnosis session string representation."""
        expected = f"{self.patient} - {self.session.session_date.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.session), expected)


class SymptomSerializerTest(TestCase):
    """Test SymptomSerializer."""

    def setUp(self):
        """Set up test data."""
        self.symptom = Symptom.objects.create(
            code='SYM001',
            name_en='Headache',
            name_cn='头痛',
            category='head',
            description='Pain in the head'
        )

    def test_symptom_serialization(self):
        """Test symptom can be serialized."""
        serializer = SymptomSerializer(self.symptom)
        data = serializer.data

        self.assertEqual(data['code'], 'SYM001')
        self.assertEqual(data['name_en'], 'Headache')
        self.assertEqual(data['name_cn'], '头痛')
        self.assertEqual(data['category'], 'head')


class SyndromeSerializerTest(TestCase):
    """Test SyndromeSerializer."""

    def setUp(self):
        """Set up test data."""
        self.syndrome = Syndrome.objects.create(
            code='SYN001',
            name_en='Qi Deficiency',
            name_cn='气虚证',
            category='qi',
            treatment_principle='Tonify Qi'
        )

        self.symptom = Symptom.objects.create(
            code='SYM001',
            name_en='Fatigue',
            name_cn='乏力',
            category='general'
        )

        SyndromeSysmptomWeight.objects.create(
            syndrome=self.syndrome,
            symptom=self.symptom,
            weight=2.0,
            is_primary=True
        )

    def test_syndrome_serialization(self):
        """Test syndrome can be serialized with symptom weights."""
        serializer = SyndromeSerializer(self.syndrome)
        data = serializer.data

        self.assertEqual(data['code'], 'SYN001')
        self.assertEqual(data['name_cn'], '气虚证')
        self.assertEqual(len(data['symptom_weights']), 1)
        self.assertEqual(data['symptom_weights'][0]['symptom']['code'], 'SYM001')
        self.assertEqual(data['symptom_weights'][0]['weight'], 2.0)
        self.assertTrue(data['symptom_weights'][0]['is_primary'])


class DiagnosisSessionSerializerTest(TestCase):
    """Test DiagnosisSessionSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testpractitioner',
            email='practitioner@test.com',
            password='testpass123',
            role='practitioner',
            first_name='Dr.',
            last_name='Smith'
        )

        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            chinese_name='约翰·多',
            ic_number='123456-78-9012',
            phone='0123456789',
            gender='male',
            date_of_birth='1990-01-01'
        )

        self.session = DiagnosisSession.objects.create(
            patient=self.patient,
            practitioner=self.user,
            chief_complaint='Persistent cough',
            selected_symptoms=['SYM001', 'SYM002']
        )

    def test_diagnosis_session_serialization(self):
        """Test diagnosis session can be serialized."""
        serializer = DiagnosisSessionSerializer(self.session)
        data = serializer.data

        self.assertEqual(data['patient'], self.patient.id)
        self.assertIn('John Doe', data['patient_name'])
        self.assertIn('Smith', data['practitioner_name'])
        self.assertEqual(data['chief_complaint'], 'Persistent cough')
        self.assertEqual(data['selected_symptoms'], ['SYM001', 'SYM002'])


class DiagnosisSessionCreateSerializerTest(TestCase):
    """Test DiagnosisSessionCreateSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testpractitioner',
            email='practitioner@test.com',
            password='testpass123',
            role='practitioner'
        )

        self.patient = Patient.objects.create(
            first_name='Jane',
            last_name='Doe',
            chinese_name='简·多',
            ic_number='123456-78-9013',
            phone='0123456790',
            gender='female',
            date_of_birth='1992-05-15'
        )

    def test_create_diagnosis_session(self):
        """Test creating diagnosis session via serializer."""
        data = {
            'patient': self.patient.id,
            'chief_complaint': 'Lower back pain',
            'selected_symptoms': ['SYM003', 'SYM004'],
            'symptom_details': 'Pain for 2 weeks'
        }

        serializer = DiagnosisSessionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        session = serializer.save(practitioner=self.user)
        self.assertEqual(session.patient, self.patient)
        self.assertEqual(session.practitioner, self.user)
        self.assertEqual(session.chief_complaint, 'Lower back pain')
