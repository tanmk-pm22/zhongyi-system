"""Patient models for TCM system."""
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Patient(models.Model):
    """Patient model with comprehensive medical information."""

    class Gender(models.TextChoices):
        MALE = 'M', _('Male (男)')
        FEMALE = 'F', _('Female (女)')
        OTHER = 'O', _('Other (其他)')

    class BloodType(models.TextChoices):
        A_POSITIVE = 'A+', 'A+'
        A_NEGATIVE = 'A-', 'A-'
        B_POSITIVE = 'B+', 'B+'
        B_NEGATIVE = 'B-', 'B-'
        AB_POSITIVE = 'AB+', 'AB+'
        AB_NEGATIVE = 'AB-', 'AB-'
        O_POSITIVE = 'O+', 'O+'
        O_NEGATIVE = 'O-', 'O-'
        UNKNOWN = 'UK', _('Unknown')

    # Unique identifier for QR code
    patient_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    # Basic Information
    first_name = models.CharField(
        _('First Name'),
        max_length=100,
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=100,
    )

    chinese_name = models.CharField(
        _('Chinese Name (中文姓名)'),
        max_length=100,
        blank=True,
    )

    ic_number = models.CharField(
        _('IC/Passport Number'),
        max_length=30,
        unique=True,
        help_text=_('Malaysian IC or Passport number'),
    )

    date_of_birth = models.DateField(
        _('Date of Birth'),
    )

    gender = models.CharField(
        _('Gender'),
        max_length=1,
        choices=Gender.choices,
    )

    blood_type = models.CharField(
        _('Blood Type'),
        max_length=3,
        choices=BloodType.choices,
        default=BloodType.UNKNOWN,
    )

    # Contact Information
    phone = models.CharField(
        _('Phone Number'),
        max_length=20,
    )

    email = models.EmailField(
        _('Email'),
        blank=True,
    )

    address = models.TextField(
        _('Address'),
    )

    emergency_contact_name = models.CharField(
        _('Emergency Contact Name'),
        max_length=100,
        blank=True,
    )

    emergency_contact_phone = models.CharField(
        _('Emergency Contact Phone'),
        max_length=20,
        blank=True,
    )

    # Medical Information
    allergies = models.TextField(
        _('Allergies (过敏史)'),
        blank=True,
        help_text=_('List all known allergies to medications, herbs, or substances'),
    )

    chronic_conditions = models.TextField(
        _('Chronic Conditions (慢性疾病)'),
        blank=True,
        help_text=_('e.g., Diabetes, Hypertension, Heart Disease'),
    )

    current_medications = models.TextField(
        _('Current Medications (目前用药)'),
        blank=True,
        help_text=_('List all current Western and TCM medications'),
    )

    medical_history = models.TextField(
        _('Medical History (病史)'),
        blank=True,
        help_text=_('Past surgeries, major illnesses, hospitalizations'),
    )

    family_history = models.TextField(
        _('Family History (家族史)'),
        blank=True,
        help_text=_('Hereditary conditions in family'),
    )

    # TCM Constitution
    tcm_constitution = models.CharField(
        _('TCM Constitution (中医体质)'),
        max_length=100,
        blank=True,
        help_text=_('e.g., 气虚质, 阳虚质, 痰湿质'),
    )

    # Profile
    photo = models.ImageField(
        _('Photo'),
        upload_to='patients/photos/',
        blank=True,
        null=True,
    )

    notes = models.TextField(
        _('Additional Notes'),
        blank=True,
    )

    # Relationships
    assigned_practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients',
        limit_choices_to={'role': 'practitioner'},
        verbose_name=_('Assigned Practitioner'),
    )

    # If patient has a user account
    user_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patient_profile',
        verbose_name=_('User Account'),
    )

    # Privacy and consent
    consent_data_sharing = models.BooleanField(
        _('Consent to Data Sharing'),
        default=False,
        help_text=_('PDPA 2010 compliant consent for data sharing'),
    )

    consent_date = models.DateField(
        _('Consent Date'),
        null=True,
        blank=True,
    )

    # Status
    is_active = models.BooleanField(
        _('Active'),
        default=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')
        ordering = ['-updated_at']

    def __str__(self):
        if self.chinese_name:
            return f"{self.first_name} {self.last_name} ({self.chinese_name})"
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class MedicalRecord(models.Model):
    """Medical record/visit for a patient."""

    class RecordType(models.TextChoices):
        INITIAL = 'initial', _('Initial Visit (初诊)')
        FOLLOWUP = 'followup', _('Follow-up (复诊)')
        EMERGENCY = 'emergency', _('Emergency (急诊)')
        CONSULTATION = 'consultation', _('Consultation (会诊)')

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name=_('Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='medical_records',
        limit_choices_to={'role': 'practitioner'},
        verbose_name=_('Practitioner'),
    )

    record_type = models.CharField(
        _('Record Type'),
        max_length=20,
        choices=RecordType.choices,
        default=RecordType.INITIAL,
    )

    visit_date = models.DateTimeField(
        _('Visit Date'),
    )

    # Chief Complaint (主诉)
    chief_complaint = models.TextField(
        _('Chief Complaint (主诉)'),
    )

    # Four Examinations (四诊)
    # 望诊 - Inspection
    inspection_notes = models.TextField(
        _('Inspection Notes (望诊)'),
        blank=True,
        help_text=_('Spirit, complexion, tongue, body form'),
    )

    tongue_diagnosis = models.TextField(
        _('Tongue Diagnosis (舌诊)'),
        blank=True,
        help_text=_('Tongue body, coating, moisture'),
    )

    # 闻诊 - Auscultation and Olfaction
    auscultation_notes = models.TextField(
        _('Auscultation/Olfaction Notes (闻诊)'),
        blank=True,
        help_text=_('Voice, breath, odors'),
    )

    # 问诊 - Inquiry
    inquiry_notes = models.TextField(
        _('Inquiry Notes (问诊)'),
        blank=True,
        help_text=_('Ten questions, symptoms history'),
    )

    # 切诊 - Palpation
    pulse_diagnosis = models.TextField(
        _('Pulse Diagnosis (脉诊)'),
        blank=True,
        help_text=_('Pulse qualities: rate, rhythm, strength, depth'),
    )

    palpation_notes = models.TextField(
        _('Palpation Notes (切诊)'),
        blank=True,
        help_text=_('Abdominal, point tenderness'),
    )

    # Diagnosis
    tcm_diagnosis = models.TextField(
        _('TCM Diagnosis (中医诊断)'),
        blank=True,
        help_text=_('Pattern/Syndrome identification (辨证)'),
    )

    western_diagnosis = models.TextField(
        _('Western Diagnosis'),
        blank=True,
        help_text=_('ICD-10 codes if applicable'),
    )

    # Treatment
    treatment_principle = models.TextField(
        _('Treatment Principle (治则治法)'),
        blank=True,
    )

    prescription = models.TextField(
        _('Prescription (处方)'),
        blank=True,
        help_text=_('Herbal formula with dosages'),
    )

    acupuncture_points = models.TextField(
        _('Acupuncture Points (针灸穴位)'),
        blank=True,
    )

    other_treatments = models.TextField(
        _('Other Treatments'),
        blank=True,
        help_text=_('Tuina, cupping, moxibustion, etc.'),
    )

    # Recommendations
    lifestyle_advice = models.TextField(
        _('Lifestyle Advice (生活建议)'),
        blank=True,
    )

    dietary_advice = models.TextField(
        _('Dietary Advice (饮食建议)'),
        blank=True,
    )

    follow_up_notes = models.TextField(
        _('Follow-up Notes'),
        blank=True,
    )

    next_appointment = models.DateTimeField(
        _('Next Appointment'),
        null=True,
        blank=True,
    )

    # Attachments
    attachments = models.JSONField(
        _('Attachments'),
        default=list,
        blank=True,
        help_text=_('List of file paths for images, lab results, etc.'),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Medical Record')
        verbose_name_plural = _('Medical Records')
        ordering = ['-visit_date']

    def __str__(self):
        return f"{self.patient} - {self.visit_date.strftime('%Y-%m-%d')} ({self.get_record_type_display()})"
