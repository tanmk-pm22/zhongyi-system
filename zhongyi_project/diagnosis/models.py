"""Models for TCM Diagnosis System."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Symptom(models.Model):
    """TCM Symptom database."""

    class Category(models.TextChoices):
        GENERAL = 'general', _('General (全身)')
        HEAD = 'head', _('Head & Face (头面)')
        CHEST = 'chest', _('Chest & Abdomen (胸腹)')
        LIMBS = 'limbs', _('Limbs (四肢)')
        SKIN = 'skin', _('Skin (皮肤)')
        SLEEP = 'sleep', _('Sleep (睡眠)')
        APPETITE = 'appetite', _('Appetite & Digestion (食欲消化)')
        URINATION = 'urination', _('Urination & Defecation (二便)')
        EMOTION = 'emotion', _('Emotion (情志)')
        GYNECOLOGY = 'gynecology', _('Gynecology (妇科)')

    code = models.CharField(
        _('Symptom Code'),
        max_length=20,
        unique=True,
    )

    name_en = models.CharField(
        _('Name (English)'),
        max_length=200,
    )

    name_cn = models.CharField(
        _('Name (Chinese)'),
        max_length=200,
    )

    category = models.CharField(
        _('Category'),
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Symptom')
        verbose_name_plural = _('Symptoms')
        ordering = ['category', 'name_en']

    def __str__(self):
        return f"{self.name_en} ({self.name_cn})"


class Syndrome(models.Model):
    """TCM Syndrome (证型) database."""

    class Category(models.TextChoices):
        QI = 'qi', _('Qi Patterns (气病证)')
        BLOOD = 'blood', _('Blood Patterns (血病证)')
        YIN_YANG = 'yin_yang', _('Yin-Yang Patterns (阴阳病证)')
        FLUID = 'fluid', _('Fluid Patterns (津液病证)')
        ORGAN = 'organ', _('Organ Patterns (脏腑病证)')
        EXTERIOR = 'exterior', _('Exterior Patterns (表证)')
        INTERIOR = 'interior', _('Interior Patterns (里证)')

    code = models.CharField(
        _('Syndrome Code'),
        max_length=20,
        unique=True,
    )

    name_en = models.CharField(
        _('Name (English)'),
        max_length=200,
    )

    name_cn = models.CharField(
        _('Name (Chinese)'),
        max_length=200,
    )

    category = models.CharField(
        _('Category'),
        max_length=20,
        choices=Category.choices,
        default=Category.QI,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
    )

    etiology = models.TextField(
        _('Etiology (病因病机)'),
        blank=True,
        help_text=_('Cause and pathogenesis'),
    )

    clinical_manifestations = models.TextField(
        _('Clinical Manifestations (临床表现)'),
        blank=True,
    )

    tongue_signs = models.CharField(
        _('Tongue Signs (舌象)'),
        max_length=200,
        blank=True,
    )

    pulse_signs = models.CharField(
        _('Pulse Signs (脉象)'),
        max_length=200,
        blank=True,
    )

    treatment_principle = models.TextField(
        _('Treatment Principle (治则治法)'),
        blank=True,
    )

    # Symptoms associated with this syndrome
    symptoms = models.ManyToManyField(
        Symptom,
        through='SyndromeSysmptomWeight',
        related_name='syndromes',
        verbose_name=_('Associated Symptoms'),
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Syndrome')
        verbose_name_plural = _('Syndromes')
        ordering = ['category', 'name_en']

    def __str__(self):
        return f"{self.name_en} ({self.name_cn})"


class SyndromeSysmptomWeight(models.Model):
    """Weight/importance of symptom for syndrome identification."""

    syndrome = models.ForeignKey(
        Syndrome,
        on_delete=models.CASCADE,
    )

    symptom = models.ForeignKey(
        Symptom,
        on_delete=models.CASCADE,
    )

    weight = models.FloatField(
        _('Weight'),
        default=1.0,
        help_text=_('Importance of this symptom for syndrome identification (0.1-3.0)'),
    )

    is_primary = models.BooleanField(
        _('Primary Symptom'),
        default=False,
        help_text=_('Is this a primary/key symptom for this syndrome?'),
    )

    class Meta:
        verbose_name = _('Syndrome-Symptom Weight')
        verbose_name_plural = _('Syndrome-Symptom Weights')
        unique_together = ['syndrome', 'symptom']

    def __str__(self):
        return f"{self.syndrome.name_cn} - {self.symptom.name_cn} ({self.weight})"


class TongueAppearance(models.Model):
    """Tongue diagnosis options."""

    class BodyColor(models.TextChoices):
        PALE = 'pale', _('Pale (淡白)')
        LIGHT_RED = 'light_red', _('Light Red (淡红)')
        RED = 'red', _('Red (红)')
        DEEP_RED = 'deep_red', _('Deep Red (绛红)')
        PURPLE = 'purple', _('Purple (紫)')
        BLUE = 'blue', _('Blue (青)')

    class CoatingColor(models.TextChoices):
        WHITE = 'white', _('White (白)')
        YELLOW = 'yellow', _('Yellow (黄)')
        GRAY = 'gray', _('Gray (灰)')
        BLACK = 'black', _('Black (黑)')

    class CoatingTexture(models.TextChoices):
        THIN = 'thin', _('Thin (薄)')
        THICK = 'thick', _('Thick (厚)')
        GREASY = 'greasy', _('Greasy (腻)')
        PEELED = 'peeled', _('Peeled (剥)')
        NONE = 'none', _('None (无苔)')

    class BodyShape(models.TextChoices):
        NORMAL = 'normal', _('Normal (正常)')
        THIN = 'thin', _('Thin (瘦薄)')
        SWOLLEN = 'swollen', _('Swollen (胖大)')
        TEETH_MARKED = 'teeth_marked', _('Teeth-marked (齿痕)')
        CRACKED = 'cracked', _('Cracked (裂纹)')
        THORNY = 'thorny', _('Thorny (芒刺)')


class PulseQuality(models.Model):
    """Pulse diagnosis options."""

    class PulseType(models.TextChoices):
        FLOATING = 'floating', _('Floating (浮)')
        DEEP = 'deep', _('Deep (沉)')
        SLOW = 'slow', _('Slow (迟)')
        RAPID = 'rapid', _('Rapid (数)')
        DEFICIENT = 'deficient', _('Deficient (虚)')
        EXCESS = 'excess', _('Excess (实)')
        SLIPPERY = 'slippery', _('Slippery (滑)')
        CHOPPY = 'choppy', _('Choppy (涩)')
        WIRY = 'wiry', _('Wiry (弦)')
        TIGHT = 'tight', _('Tight (紧)')
        THREADY = 'thready', _('Thready (细)')
        LARGE = 'large', _('Large (大)')
        MINUTE = 'minute', _('Minute (微)')
        SOGGY = 'soggy', _('Soggy (濡)')
        WEAK = 'weak', _('Weak (弱)')
        SCATTERED = 'scattered', _('Scattered (散)')
        HOLLOW = 'hollow', _('Hollow (芤)')
        LEATHER = 'leather', _('Leather (革)')
        FIRM = 'firm', _('Firm (牢)')
        HIDDEN = 'hidden', _('Hidden (伏)')
        MOVING = 'moving', _('Moving (动)')
        HASTY = 'hasty', _('Hasty (促)')
        KNOTTED = 'knotted', _('Knotted (结)')
        INTERMITTENT = 'intermittent', _('Intermittent (代)')
        LONG = 'long', _('Long (长)')
        SHORT = 'short', _('Short (短)')
        SURGING = 'surging', _('Surging (洪)')
        MODERATE = 'moderate', _('Moderate (缓)')


class DiagnosisSession(models.Model):
    """A diagnosis session for a patient."""

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='diagnosis_sessions',
        verbose_name=_('Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='diagnosis_sessions',
        verbose_name=_('Practitioner'),
    )

    medical_record = models.ForeignKey(
        'patients.MedicalRecord',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='diagnosis_sessions',
        verbose_name=_('Medical Record'),
    )

    session_date = models.DateTimeField(
        _('Session Date'),
        auto_now_add=True,
    )

    # Chief Complaint
    chief_complaint = models.TextField(
        _('Chief Complaint (主诉)'),
    )

    # Inspection (望诊)
    spirit_status = models.CharField(
        _('Spirit Status (神)'),
        max_length=100,
        blank=True,
        help_text=_('e.g., Alert, Listless, Agitated'),
    )

    complexion = models.CharField(
        _('Complexion (面色)'),
        max_length=100,
        blank=True,
    )

    tongue_body_color = models.CharField(
        _('Tongue Body Color'),
        max_length=20,
        choices=TongueAppearance.BodyColor.choices,
        blank=True,
    )

    tongue_body_shape = models.CharField(
        _('Tongue Body Shape'),
        max_length=20,
        choices=TongueAppearance.BodyShape.choices,
        blank=True,
    )

    tongue_coating_color = models.CharField(
        _('Tongue Coating Color'),
        max_length=20,
        choices=TongueAppearance.CoatingColor.choices,
        blank=True,
    )

    tongue_coating_texture = models.CharField(
        _('Tongue Coating Texture'),
        max_length=20,
        choices=TongueAppearance.CoatingTexture.choices,
        blank=True,
    )

    tongue_notes = models.TextField(
        _('Additional Tongue Notes'),
        blank=True,
    )

    # Auscultation & Olfaction (闻诊)
    voice_quality = models.CharField(
        _('Voice Quality'),
        max_length=100,
        blank=True,
    )

    breath_odor = models.CharField(
        _('Breath Odor'),
        max_length=100,
        blank=True,
    )

    auscultation_notes = models.TextField(
        _('Auscultation Notes'),
        blank=True,
    )

    # Inquiry (问诊)
    # Using JSON field for flexible symptom storage
    selected_symptoms = models.JSONField(
        _('Selected Symptoms'),
        default=list,
        help_text=_('List of symptom codes selected during inquiry'),
    )

    symptom_details = models.TextField(
        _('Symptom Details'),
        blank=True,
        help_text=_('Duration, severity, triggering factors'),
    )

    sleep_quality = models.CharField(
        _('Sleep Quality'),
        max_length=100,
        blank=True,
    )

    appetite = models.CharField(
        _('Appetite'),
        max_length=100,
        blank=True,
    )

    thirst = models.CharField(
        _('Thirst'),
        max_length=100,
        blank=True,
    )

    defecation = models.CharField(
        _('Defecation'),
        max_length=100,
        blank=True,
    )

    urination = models.CharField(
        _('Urination'),
        max_length=100,
        blank=True,
    )

    perspiration = models.CharField(
        _('Perspiration'),
        max_length=100,
        blank=True,
    )

    inquiry_notes = models.TextField(
        _('Additional Inquiry Notes'),
        blank=True,
    )

    # Palpation (切诊)
    pulse_left_cun = models.CharField(
        _('Left Cun Pulse'),
        max_length=50,
        blank=True,
    )

    pulse_left_guan = models.CharField(
        _('Left Guan Pulse'),
        max_length=50,
        blank=True,
    )

    pulse_left_chi = models.CharField(
        _('Left Chi Pulse'),
        max_length=50,
        blank=True,
    )

    pulse_right_cun = models.CharField(
        _('Right Cun Pulse'),
        max_length=50,
        blank=True,
    )

    pulse_right_guan = models.CharField(
        _('Right Guan Pulse'),
        max_length=50,
        blank=True,
    )

    pulse_right_chi = models.CharField(
        _('Right Chi Pulse'),
        max_length=50,
        blank=True,
    )

    pulse_overall = models.CharField(
        _('Overall Pulse Quality'),
        max_length=100,
        blank=True,
    )

    palpation_notes = models.TextField(
        _('Palpation Notes'),
        blank=True,
    )

    # AI Analysis Results
    ai_suggested_syndromes = models.JSONField(
        _('AI Suggested Syndromes'),
        default=list,
        help_text=_('List of syndrome codes with confidence scores'),
    )

    # Practitioner's Final Diagnosis
    final_diagnosis = models.TextField(
        _('Final Diagnosis (辨证结论)'),
        blank=True,
    )

    treatment_principle = models.TextField(
        _('Treatment Principle (治则治法)'),
        blank=True,
    )

    notes = models.TextField(
        _('Additional Notes'),
        blank=True,
    )

    # Status
    is_complete = models.BooleanField(
        _('Complete'),
        default=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Diagnosis Session')
        verbose_name_plural = _('Diagnosis Sessions')
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.patient} - {self.session_date.strftime('%Y-%m-%d')}"
