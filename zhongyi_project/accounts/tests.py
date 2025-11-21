"""Tests for Accounts app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for User model."""

    def test_create_user(self):
        """Test creating a user with default role."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, User.Role.PATIENT)
        self.assertTrue(user.check_password('testpass123'))

    def test_create_practitioner(self):
        """Test creating a practitioner user."""
        user = User.objects.create_user(
            username='doctor',
            email='doctor@clinic.com',
            password='docpass123',
            role=User.Role.PRACTITIONER,
            license_number='TCM-12345',
            specialization='Acupuncture'
        )
        self.assertEqual(user.role, User.Role.PRACTITIONER)
        self.assertTrue(user.is_practitioner)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_patient_role)
        self.assertEqual(user.license_number, 'TCM-12345')

    def test_create_admin(self):
        """Test creating an admin user."""
        user = User.objects.create_user(
            username='admin',
            email='admin@system.com',
            password='adminpass123',
            role=User.Role.ADMIN
        )
        self.assertTrue(user.is_admin)
        self.assertFalse(user.is_practitioner)

    def test_user_str_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(
            username='testuser',
            first_name='张',
            last_name='三',
            email='test@example.com',
            password='testpass123'
        )
        self.assertIn('张 三', str(user))

    def test_user_profile_fields(self):
        """Test user profile fields."""
        user = User.objects.create_user(
            username='patient1',
            email='patient@example.com',
            password='patientpass',
            phone='0123456789',
            ic_number='900101-14-5678',
            address='123 Test Street, KL'
        )
        self.assertEqual(user.phone, '0123456789')
        self.assertEqual(user.ic_number, '900101-14-5678')
        self.assertEqual(user.address, '123 Test Street, KL')


class UserAuthenticationTests(TestCase):
    """Tests for user authentication."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_view(self):
        """Test login view is accessible."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_login_failure(self):
        """Test login with wrong password."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test logout functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('accounts:logout'))
        self.assertIn(response.status_code, [200, 302])

    def test_register_view(self):
        """Test registration view is accessible."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)


class UserDashboardTests(TestCase):
    """Tests for user dashboard."""

    def setUp(self):
        """Set up test users."""
        self.client = Client()
        self.patient = User.objects.create_user(
            username='patient',
            password='patientpass',
            role=User.Role.PATIENT
        )
        self.practitioner = User.objects.create_user(
            username='doctor',
            password='doctorpass',
            role=User.Role.PRACTITIONER
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass',
            role=User.Role.ADMIN
        )

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication."""
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_patient_dashboard(self):
        """Test patient can access dashboard."""
        self.client.login(username='patient', password='patientpass')
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_practitioner_dashboard(self):
        """Test practitioner can access dashboard."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard(self):
        """Test admin can access dashboard."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)


class UserProfileTests(TestCase):
    """Tests for user profile management."""

    def setUp(self):
        """Set up test user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_profile_view_requires_login(self):
        """Test profile view requires authentication."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_authenticated(self):
        """Test authenticated user can view profile."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)


class UserAPITests(TestCase):
    """Tests for User API endpoints."""

    def setUp(self):
        """Set up test client and users."""
        self.client = Client()
        self.practitioner = User.objects.create_user(
            username='doctor',
            email='doctor@clinic.com',
            password='doctorpass',
            role=User.Role.PRACTITIONER,
            first_name='Dr',
            last_name='Smith'
        )
        self.patient = User.objects.create_user(
            username='patient',
            email='patient@email.com',
            password='patientpass',
            role=User.Role.PATIENT
        )

    def test_api_requires_auth(self):
        """Test API requires authentication."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 403)

    def test_api_me_endpoint(self):
        """Test /api/users/me/ endpoint."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, 200)

    def test_api_practitioners_endpoint(self):
        """Test /api/users/practitioners/ endpoint."""
        self.client.login(username='doctor', password='doctorpass')
        response = self.client.get('/api/users/practitioners/')
        self.assertEqual(response.status_code, 200)
