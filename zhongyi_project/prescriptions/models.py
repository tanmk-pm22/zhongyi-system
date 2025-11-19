"""Models for TCM Prescription System."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class HerbCategory(models.Model):
    """Category for herbs."""

    name_cn = models.CharField(_('名称 (中文)'), max_length=100)
    name_en = models.CharField(_('Name (English)'), max_length=100)
    description = models.TextField(_('描述'), blank=True)

    class Meta:
        verbose_name = _('药材类别')
        verbose_name_plural = _('药材类别')
        ordering = ['name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"


class Herb(models.Model):
    """TCM Herb/Medicine database."""

    class Nature(models.TextChoices):
        HOT = 'hot', _('热 | Hot')
        WARM = 'warm', _('温 | Warm')
        NEUTRAL = 'neutral', _('平 | Neutral')
        COOL = 'cool', _('凉 | Cool')
        COLD = 'cold', _('寒 | Cold')

    class Taste(models.TextChoices):
        SOUR = 'sour', _('酸 | Sour')
        BITTER = 'bitter', _('苦 | Bitter')
        SWEET = 'sweet', _('甘 | Sweet')
        PUNGENT = 'pungent', _('辛 | Pungent')
        SALTY = 'salty', _('咸 | Salty')
        BLAND = 'bland', _('淡 | Bland')
        ASTRINGENT = 'astringent', _('涩 | Astringent')

    # Basic Info
    code = models.CharField(_('编码'), max_length=20, unique=True)
    name_cn = models.CharField(_('中文名'), max_length=100)
    name_en = models.CharField(_('English Name'), max_length=200)
    name_pinyin = models.CharField(_('拼音'), max_length=200, blank=True)
    name_latin = models.CharField(_('拉丁名'), max_length=200, blank=True)

    category = models.ForeignKey(
        HerbCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='herbs',
        verbose_name=_('类别'),
    )

    # TCM Properties
    nature = models.CharField(
        _('药性'),
        max_length=20,
        choices=Nature.choices,
        default=Nature.NEUTRAL,
    )

    taste = models.JSONField(
        _('药味'),
        default=list,
        help_text=_('List of tastes, e.g., ["sweet", "bitter"]'),
    )

    meridians = models.JSONField(
        _('归经'),
        default=list,
        help_text=_('List of meridians, e.g., ["lung", "spleen"]'),
    )

    # Clinical Info
    functions = models.TextField(
        _('功效'),
        blank=True,
        help_text=_('Main therapeutic functions'),
    )

    indications = models.TextField(
        _('主治'),
        blank=True,
        help_text=_('Clinical indications'),
    )

    contraindications = models.TextField(
        _('禁忌'),
        blank=True,
        help_text=_('Contraindications and cautions'),
    )

    # Dosage
    dosage_min = models.DecimalField(
        _('最小剂量 (克)'),
        max_digits=6,
        decimal_places=2,
        default=Decimal('3.00'),
    )

    dosage_max = models.DecimalField(
        _('最大剂量 (克)'),
        max_digits=6,
        decimal_places=2,
        default=Decimal('15.00'),
    )

    dosage_unit = models.CharField(
        _('剂量单位'),
        max_length=20,
        default='克',
    )

    # Preparation
    preparation_notes = models.TextField(
        _('炮制/煎煮说明'),
        blank=True,
        help_text=_('Special preparation or decoction instructions'),
    )

    # Pricing (optional)
    price_per_gram = models.DecimalField(
        _('单价 (每克)'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # Status
    is_active = models.BooleanField(_('启用'), default=True)
    is_toxic = models.BooleanField(_('有毒'), default=False)
    requires_processing = models.BooleanField(_('需炮制'), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('中药')
        verbose_name_plural = _('中药')
        ordering = ['name_pinyin', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} ({self.name_en})"

    @property
    def dosage_range(self):
        return f"{self.dosage_min}-{self.dosage_max}{self.dosage_unit}"


class ClassicFormula(models.Model):
    """Classic TCM Formulas (经典方剂)."""

    code = models.CharField(_('编码'), max_length=20, unique=True)
    name_cn = models.CharField(_('中文名'), max_length=100)
    name_en = models.CharField(_('English Name'), max_length=200)
    name_pinyin = models.CharField(_('拼音'), max_length=200, blank=True)

    source = models.CharField(
        _('出处'),
        max_length=200,
        blank=True,
        help_text=_('Classical text source'),
    )

    composition = models.TextField(
        _('组成'),
        help_text=_('Original composition description'),
    )

    functions = models.TextField(
        _('功效'),
        blank=True,
    )

    indications = models.TextField(
        _('主治'),
        blank=True,
    )

    contraindications = models.TextField(
        _('禁忌'),
        blank=True,
    )

    modifications = models.TextField(
        _('加减变化'),
        blank=True,
        help_text=_('Common modifications'),
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('经典方剂')
        verbose_name_plural = _('经典方剂')
        ordering = ['name_pinyin', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} ({self.name_en})"


class FormulaHerb(models.Model):
    """Herbs in a classic formula with their roles and dosages."""

    class Role(models.TextChoices):
        MONARCH = 'monarch', _('君药 | Monarch')
        MINISTER = 'minister', _('臣药 | Minister')
        ASSISTANT = 'assistant', _('佐药 | Assistant')
        ENVOY = 'envoy', _('使药 | Envoy')

    formula = models.ForeignKey(
        ClassicFormula,
        on_delete=models.CASCADE,
        related_name='formula_herbs',
    )

    herb = models.ForeignKey(
        Herb,
        on_delete=models.CASCADE,
        related_name='formula_uses',
    )

    role = models.CharField(
        _('药物角色'),
        max_length=20,
        choices=Role.choices,
        default=Role.ASSISTANT,
    )

    dosage = models.DecimalField(
        _('剂量'),
        max_digits=6,
        decimal_places=2,
    )

    notes = models.CharField(
        _('备注'),
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = _('方剂药物')
        verbose_name_plural = _('方剂药物')
        unique_together = ['formula', 'herb']
        ordering = ['role', 'herb__name_cn']

    def __str__(self):
        return f"{self.formula.name_cn} - {self.herb.name_cn}"


class Prescription(models.Model):
    """Patient prescription."""

    class Status(models.TextChoices):
        DRAFT = 'draft', _('草稿')
        CONFIRMED = 'confirmed', _('已确认')
        DISPENSED = 'dispensed', _('已配药')
        COMPLETED = 'completed', _('已完成')
        CANCELLED = 'cancelled', _('已取消')

    # Relations
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('患者'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prescriptions',
        verbose_name=_('医师'),
    )

    diagnosis_session = models.ForeignKey(
        'diagnosis.DiagnosisSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions',
        verbose_name=_('诊断记录'),
    )

    based_on_formula = models.ForeignKey(
        ClassicFormula,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='derived_prescriptions',
        verbose_name=_('基于方剂'),
    )

    # Prescription Info
    prescription_number = models.CharField(
        _('处方编号'),
        max_length=50,
        unique=True,
    )

    prescription_date = models.DateTimeField(
        _('处方日期'),
        auto_now_add=True,
    )

    diagnosis = models.TextField(
        _('诊断'),
        blank=True,
    )

    treatment_principle = models.TextField(
        _('治则治法'),
        blank=True,
    )

    # Dosage Info
    doses = models.PositiveIntegerField(
        _('剂数'),
        default=7,
        help_text=_('Number of doses to prepare'),
    )

    decoction_method = models.TextField(
        _('煎煮方法'),
        default='水煎服，每日一剂，分两次温服。',
        help_text=_('Instructions for decoction'),
    )

    # Additional Instructions
    dietary_advice = models.TextField(
        _('饮食宜忌'),
        blank=True,
    )

    lifestyle_advice = models.TextField(
        _('生活建议'),
        blank=True,
    )

    notes = models.TextField(
        _('备注'),
        blank=True,
    )

    # Status
    status = models.CharField(
        _('状态'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    # Pricing
    total_price = models.DecimalField(
        _('总价'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('处方')
        verbose_name_plural = _('处方')
        ordering = ['-prescription_date']

    def __str__(self):
        return f"{self.prescription_number} - {self.patient.full_name}"

    def save(self, *args, **kwargs):
        if not self.prescription_number:
            # Generate prescription number
            from django.utils import timezone
            import random
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = str(random.randint(1000, 9999))
            self.prescription_number = f"RX{date_str}{random_str}"
        super().save(*args, **kwargs)

    def calculate_total(self):
        """Calculate total price based on herbs."""
        total = Decimal('0.00')
        for item in self.items.all():
            if item.herb.price_per_gram:
                total += item.herb.price_per_gram * item.dosage * self.doses
        self.total_price = total
        return total


class PrescriptionItem(models.Model):
    """Individual herb in a prescription."""

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('处方'),
    )

    herb = models.ForeignKey(
        Herb,
        on_delete=models.CASCADE,
        related_name='prescription_items',
        verbose_name=_('药材'),
    )

    dosage = models.DecimalField(
        _('剂量 (克)'),
        max_digits=6,
        decimal_places=2,
    )

    preparation = models.CharField(
        _('炮制方法'),
        max_length=100,
        blank=True,
        help_text=_('e.g., 先煎, 后下, 包煎'),
    )

    notes = models.CharField(
        _('备注'),
        max_length=200,
        blank=True,
    )

    sequence = models.PositiveIntegerField(
        _('顺序'),
        default=0,
    )

    class Meta:
        verbose_name = _('处方药物')
        verbose_name_plural = _('处方药物')
        ordering = ['sequence', 'herb__name_cn']
        unique_together = ['prescription', 'herb']

    def __str__(self):
        return f"{self.herb.name_cn} {self.dosage}g"

    @property
    def subtotal(self):
        """Calculate subtotal for this item."""
        if self.herb.price_per_gram:
            return self.herb.price_per_gram * self.dosage * self.prescription.doses
        return Decimal('0.00')
