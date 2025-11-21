"""Tests for Diagnosis app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from patients.models import Patient
from .models import Symptom, Syndrome, DiagnosisSession, SyndromeSysmptomWeight
from .analysis import analyze_symptoms

User = get_user_model()


class SymptomModelTests(TestCase):
    """Tests for Symptom model."""

    def test_create_symptom(self):
        """Test creating a symptom."""
        symptom = Symptom.objects.create(
            code='S001',
            name_en='Fatigue',
            name_cn='疲劳乏力',
            category='general'
        )
        self.assertEqual(symptom.code, 'S001')
        self.assertEqual(symptom.name_cn, '疲劳乏力')

    def test_symptom_str_representation(self):
        """Test string representation of symptom."""
        symptom = Symptom.objects.create(
            code='S002',
            name_en='Headache',
            name_cn='头痛',
            category='head'
        )
        self.assertIn('Headache', str(symptom))
        self.assertIn('头痛', str(symptom))

    def test_symptom_categories(self):
        """Test symptom category choices."""
        categories = [choice[0] for choice in Symptom.Category.choices]
        self.assertIn('general', categories)
        self.assertIn('head', categories)
        self.assertIn('chest', categories)


class SyndromeModelTests(TestCase):
    """Tests for Syndrome model."""

    def test_create_syndrome(self):
        """Test creating a syndrome."""
        syndrome = Syndrome.objects.create(
            code='SYN001',
            name_en='Qi Deficiency',
            name_cn='气虚证',
            category='qi',
            treatment_principle='补气'
        )
        self.assertEqual(syndrome.code, 'SYN001')
        self.assertEqual(syndrome.name_cn, '气虚证')

    def test_syndrome_with_symptoms(self):
        """Test syndrome with related symptoms."""
        syndrome = Syndrome.objects.create(
            code='SYN002',
            name_en='Blood Stasis',
            name_cn='血瘀证',
            category='blood'
        )
        symptom = Symptom.objects.create(
            code='S003',
            name_en='Pain',
            name_cn='疼痛',
            category='general'
        )
        SyndromeSysmptomWeight.objects.create(
            syndrome=syndrome,
            symptom=symptom,
            weight=2.0,
            is_primary=True
        )
        self.assertEqual(syndrome.symptoms.count(), 1)


class DiagnosisSessionModelTests(TestCase):
    """Tests for DiagnosisSession model."""

    def setUp(self):
        """Set up test data."""
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
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

    def test_create_diagnosis_session(self):
        """Test creating a diagnosis session."""
        session = DiagnosisSession.objects.create(
            patient=self.patient,
            practitioner=self.practitioner,
            chief_complaint='头痛三天，伴有发热'
        )
        self.assertEqual(session.chief_complaint, '头痛三天，伴有发热')
        self.assertFalse(session.is_complete)

    def test_four_examinations_fields(self):
        """Test four examinations documentation."""
        session = DiagnosisSession.objects.create(
            patient=self.patient,
            practitioner=self.practitioner,
            chief_complaint='失眠',
            # Inspection
            spirit_status='Alert',
            complexion='萎黄',
            tongue_body_color='pale',
            tongue_coating_color='white',
            # Auscultation
            voice_quality='低微',
            # Inquiry
            sleep_quality='入睡困难',
            # Palpation
            pulse_overall='细弱'
        )
        self.assertEqual(session.tongue_body_color, 'pale')
        self.assertEqual(session.pulse_overall, '细弱')

    def test_selected_symptoms(self):
        """Test selected symptoms JSON field."""
        session = DiagnosisSession.objects.create(
            patient=self.patient,
            practitioner=self.practitioner,
            chief_complaint='Test',
            selected_symptoms=['S001', 'S002', 'S003']
        )
        self.assertEqual(len(session.selected_symptoms), 3)


class DiagnosisAnalysisTests(TestCase):
    """Tests for diagnosis analysis engine."""

    def setUp(self):
        """Set up test syndromes and symptoms."""
        # Create symptoms
        self.fatigue = Symptom.objects.create(
            code='S001',
            name_en='Fatigue',
            name_cn='疲劳乏力',
            category='general'
        )
        self.spontaneous_sweat = Symptom.objects.create(
            code='S002',
            name_en='Spontaneous sweating',
            name_cn='自汗',
            category='general'
        )
        self.poor_appetite = Symptom.objects.create(
            code='S003',
            name_en='Poor appetite',
            name_cn='食欲不振',
            category='appetite'
        )

        # Create syndrome
        self.qi_deficiency = Syndrome.objects.create(
            code='SYN001',
            name_en='Qi Deficiency',
            name_cn='气虚证',
            category='qi',
            tongue_signs='舌淡苔白',
            pulse_signs='脉虚弱',
            treatment_principle='补气'
        )

        # Link symptoms to syndrome
        SyndromeSysmptomWeight.objects.create(
            syndrome=self.qi_deficiency,
            symptom=self.fatigue,
            weight=2.0,
            is_primary=True
        )
        SyndromeSysmptomWeight.objects.create(
            syndrome=self.qi_deficiency,
            symptom=self.spontaneous_sweat,
            weight=1.5,
            is_primary=False
        )
        SyndromeSysmptomWeight.objects.create(
            syndrome=self.qi_deficiency,
            symptom=self.poor_appetite,
            weight=1.0,
            is_primary=False
        )

    def test_analyze_symptoms_basic(self):
        """Test basic symptom analysis."""
        symptom_codes = ['S001', 'S002', 'S003']
        results = analyze_symptoms(symptom_codes)
        self.assertIsInstance(results, list)

    def test_analyze_symptoms_with_tongue(self):
        """Test analysis with tongue data."""
        symptom_codes = ['S001', 'S002']
        tongue_data = {
            'body_color': 'pale',
            'coating_color': 'white'
        }
        results = analyze_symptoms(symptom_codes, tongue_data=tongue_data)
        self.assertIsInstance(results, list)

    def test_analyze_empty_symptoms(self):
        """Test analysis with empty symptom list."""
        results = analyze_symptoms([])
        self.assertEqual(results, [])


class DiagnosisViewTests(TestCase):
    """Tests for Diagnosis views."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
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

    def test_diagnosis_list_requires_login(self):
        """Test diagnosis list requires authentication."""
        response = self.client.get(reverse('diagnosis:list'))
        self.assertEqual(response.status_code, 302)

    def test_diagnosis_list_view(self):
        """Test diagnosis list view."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('diagnosis:list'))
        self.assertEqual(response.status_code, 200)

    def test_select_patient_view(self):
        """Test patient selection for diagnosis."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('diagnosis:select_patient'))
        self.assertEqual(response.status_code, 200)


class DiagnosisAPITests(TestCase):
    """Tests for Diagnosis API endpoints."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
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
        # Create symptoms
        Symptom.objects.create(
            code='S001',
            name_en='Fatigue',
            name_cn='疲劳乏力',
            category='general'
        )

    def test_api_symptoms_list(self):
        """Test symptoms list API."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get('/api/symptoms/')
        self.assertEqual(response.status_code, 200)

    def test_api_symptoms_by_category(self):
        """Test symptoms filtered by category."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get('/api/symptoms/?category=general')
        self.assertEqual(response.status_code, 200)

    def test_api_requires_auth(self):
        """Test API requires authentication."""
        response = self.client.get('/api/symptoms/')
        self.assertEqual(response.status_code, 403)


class SyndromeSysmptomWeightTests(TestCase):
    """Tests for SyndromeSysmptomWeight model."""

    def test_weight_constraints(self):
        """Test symptom weight constraints."""
        syndrome = Syndrome.objects.create(
            code='SYN001',
            name_en='Test Syndrome',
            name_cn='测试证型',
            category='qi'
        )
        symptom = Symptom.objects.create(
            code='S001',
            name_en='Test Symptom',
            name_cn='测试症状',
            category='general'
        )
        weight = SyndromeSysmptomWeight.objects.create(
            syndrome=syndrome,
            symptom=symptom,
            weight=1.5,
            is_primary=True
        )
        self.assertEqual(weight.weight, 1.5)
        self.assertTrue(weight.is_primary)

    def test_unique_together_constraint(self):
        """Test unique together constraint on syndrome-symptom."""
        syndrome = Syndrome.objects.create(
            code='SYN002',
            name_en='Another Syndrome',
            name_cn='另一证型',
            category='blood'
        )
        symptom = Symptom.objects.create(
            code='S002',
            name_en='Another Symptom',
            name_cn='另一症状',
            category='head'
        )
        SyndromeSysmptomWeight.objects.create(
            syndrome=syndrome,
            symptom=symptom,
            weight=1.0
        )
        # Should raise error on duplicate
        with self.assertRaises(Exception):
            SyndromeSysmptomWeight.objects.create(
                syndrome=syndrome,
                symptom=symptom,
                weight=2.0
            )
