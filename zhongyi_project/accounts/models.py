"""
Custom User model with role-based access control.
Supports: Admin (系统管理员), Practitioner (中医师), Patient (患者)
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User model with roles for TCM system."""

    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrator (系统管理员)')
        PRACTITIONER = 'practitioner', _('TCM Practitioner (中医师)')
        PATIENT = 'patient', _('Patient (患者)')

    role = models.CharField(
        _('Role'),
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    # Additional profile fields
    phone = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True,
    )

    ic_number = models.CharField(
        _('IC/Passport Number'),
        max_length=30,
        blank=True,
        help_text=_('Malaysian IC or Passport number'),
    )

    date_of_birth = models.DateField(
        _('Date of Birth'),
        null=True,
        blank=True,
    )

    address = models.TextField(
        _('Address'),
        blank=True,
    )

    profile_photo = models.ImageField(
        _('Profile Photo'),
        upload_to='profiles/',
        blank=True,
        null=True,
    )

    # Practitioner-specific fields
    license_number = models.CharField(
        _('T&CM License Number'),
        max_length=50,
        blank=True,
        help_text=_('Traditional & Complementary Medicine practitioner license'),
    )

    specialization = models.CharField(
        _('Specialization'),
        max_length=100,
        blank=True,
        help_text=_('e.g., Acupuncture, Herbal Medicine, Tuina'),
    )

    clinic_name = models.CharField(
        _('Clinic Name'),
        max_length=200,
        blank=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_practitioner(self):
        return self.role == self.Role.PRACTITIONER

    @property
    def is_patient_role(self):
        return self.role == self.Role.PATIENT
