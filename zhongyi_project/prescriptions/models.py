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
        """Calculate total price based on herbs and patent medicines."""
        total = Decimal('0.00')

        # Calculate herb costs
        for item in self.items.all():
            if item.herb.price_per_gram:
                total += item.herb.price_per_gram * item.dosage * self.doses

        # Calculate patent medicine costs
        for patent_item in self.patent_medicine_items.all():
            if patent_item.medicine.price_per_box:
                total += patent_item.medicine.price_per_box * patent_item.quantity

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


class PatentMedicine(models.Model):
    """
    Modern Chinese Patent Medicine (中成药)
    现代中成药 - 丸剂、片剂、颗粒、胶囊等
    """

    class DosageForm(models.TextChoices):
        PILL = 'pill', _('丸剂 | Pills')
        TABLET = 'tablet', _('片剂 | Tablets')
        CAPSULE = 'capsule', _('胶囊 | Capsules')
        GRANULE = 'granule', _('颗粒 | Granules')
        POWDER = 'powder', _('散剂 | Powder')
        ORAL_LIQUID = 'oral_liquid', _('口服液 | Oral Liquid')
        SYRUP = 'syrup', _('糖浆 | Syrup')
        INJECTION = 'injection', _('注射液 | Injection')
        EXTERNAL = 'external', _('外用 | External Use')

    class PrescriptionType(models.TextChoices):
        OTC = 'otc', _('非处方药 | OTC')
        RX = 'rx', _('处方药 | Prescription')

    # Basic Info
    code = models.CharField(_('编码 | Code'), max_length=20, unique=True)
    name_cn = models.CharField(_('中文名 | Chinese Name'), max_length=200)
    name_en = models.CharField(_('英文名 | English Name'), max_length=200, blank=True)

    # Manufacturer
    manufacturer = models.CharField(
        _('生产厂家 | Manufacturer'),
        max_length=200,
        blank=True,
    )

    approval_number = models.CharField(
        _('批准文号 | Approval Number'),
        max_length=100,
        blank=True,
        help_text=_('国药准字号'),
    )

    # Dosage Form
    dosage_form = models.CharField(
        _('剂型 | Dosage Form'),
        max_length=20,
        choices=DosageForm.choices,
        default=DosageForm.TABLET,
    )

    prescription_type = models.CharField(
        _('处方类型 | Prescription Type'),
        max_length=10,
        choices=PrescriptionType.choices,
        default=PrescriptionType.OTC,
    )

    # Composition
    ingredients = models.TextField(
        _('成分 | Ingredients'),
        help_text=_('主要药物成分'),
    )

    # TCM Properties
    functions = models.TextField(
        _('功能主治 | Functions & Indications'),
        help_text=_('功效和适应症'),
    )

    tcm_pattern = models.CharField(
        _('中医证型 | TCM Pattern'),
        max_length=200,
        blank=True,
        help_text=_('适用的中医证型'),
    )

    # Dosage & Administration
    specification = models.CharField(
        _('规格 | Specification'),
        max_length=100,
        help_text=_('例如: 0.3g×12粒×3板'),
    )

    dosage_adult = models.CharField(
        _('成人用量 | Adult Dosage'),
        max_length=200,
        help_text=_('例如: 每次4粒，每日3次'),
    )

    dosage_child = models.CharField(
        _('儿童用量 | Child Dosage'),
        max_length=200,
        blank=True,
    )

    administration_method = models.CharField(
        _('服用方法 | Administration'),
        max_length=200,
        default='温水送服',
        help_text=_('例如: 温水送服、饭前服用等'),
    )

    # Safety Info
    contraindications = models.TextField(
        _('禁忌 | Contraindications'),
        blank=True,
    )

    precautions = models.TextField(
        _('注意事项 | Precautions'),
        blank=True,
    )

    adverse_reactions = models.TextField(
        _('不良反应 | Adverse Reactions'),
        blank=True,
    )

    drug_interactions = models.TextField(
        _('药物相互作用 | Drug Interactions'),
        blank=True,
    )

    # Pricing
    price_per_box = models.DecimalField(
        _('单价 (每盒) | Price per Box'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # Storage
    storage_conditions = models.CharField(
        _('贮藏 | Storage'),
        max_length=200,
        default='密封，置阴凉干燥处',
    )

    shelf_life = models.CharField(
        _('有效期 | Shelf Life'),
        max_length=50,
        default='24个月',
    )

    # Status
    is_active = models.BooleanField(_('启用 | Active'), default=True)
    is_in_stock = models.BooleanField(_('有库存 | In Stock'), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('中成药 | Patent Medicine')
        verbose_name_plural = _('中成药 | Patent Medicines')
        ordering = ['name_cn']

    def __str__(self):
        return f"{self.name_cn} ({self.dosage_form})"


class PrescriptionPatentMedicine(models.Model):
    """
    Patent Medicine items in a prescription
    处方中的中成药项目
    """

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='patent_medicine_items',
        verbose_name=_('处方 | Prescription'),
    )

    medicine = models.ForeignKey(
        PatentMedicine,
        on_delete=models.CASCADE,
        related_name='prescription_items',
        verbose_name=_('中成药 | Patent Medicine'),
    )

    quantity = models.PositiveIntegerField(
        _('数量 | Quantity'),
        default=1,
        help_text=_('盒数或瓶数'),
    )

    dosage_instruction = models.CharField(
        _('用法用量 | Dosage Instruction'),
        max_length=200,
        blank=True,
        help_text=_('可覆盖默认用量'),
    )

    duration_days = models.PositiveIntegerField(
        _('疗程天数 | Duration (days)'),
        default=7,
    )

    notes = models.CharField(
        _('备注 | Notes'),
        max_length=200,
        blank=True,
    )

    sequence = models.PositiveIntegerField(
        _('顺序 | Sequence'),
        default=0,
    )

    class Meta:
        verbose_name = _('处方中成药 | Prescription Patent Medicine')
        verbose_name_plural = _('处方中成药 | Prescription Patent Medicines')
        ordering = ['sequence', 'medicine__name_cn']
        unique_together = ['prescription', 'medicine']

    def __str__(self):
        return f"{self.medicine.name_cn} × {self.quantity}"

    @property
    def subtotal(self):
        """Calculate subtotal for this item."""
        if self.medicine.price_per_box:
            return self.medicine.price_per_box * self.quantity
        return Decimal('0.00')


class DecoctionMethod(models.Model):
    """
    Standard decoction methods for herbal medicine (煎药方法).
    """

    name_cn = models.CharField(
        _('中文名称 | Chinese Name'),
        max_length=100,
    )

    name_en = models.CharField(
        _('英文名称 | English Name'),
        max_length=100,
    )

    code = models.CharField(
        _('编码 | Code'),
        max_length=20,
        unique=True,
    )

    description = models.TextField(
        _('描述 | Description'),
        help_text=_('详细的煎药方法说明'),
    )

    # Detailed instructions
    water_amount = models.CharField(
        _('加水量 | Water Amount'),
        max_length=100,
        blank=True,
        help_text=_('例如：加水至药面上2-3厘米'),
    )

    soaking_time = models.CharField(
        _('浸泡时间 | Soaking Time'),
        max_length=100,
        blank=True,
        help_text=_('例如：浸泡20-30分钟'),
    )

    first_decoction = models.CharField(
        _('头煎 | First Decoction'),
        max_length=200,
        blank=True,
        help_text=_('例如：大火煮沸后转小火煎煮30分钟'),
    )

    second_decoction = models.CharField(
        _('二煎 | Second Decoction'),
        max_length=200,
        blank=True,
        help_text=_('例如：再加水煎煮20分钟'),
    )

    administration = models.CharField(
        _('服用方法 | Administration'),
        max_length=200,
        blank=True,
        help_text=_('例如：混合两次煎液，分早晚两次温服'),
    )

    # Special instructions
    special_handling = models.TextField(
        _('特殊处理 | Special Handling'),
        blank=True,
        help_text=_('需要先煎、后下、包煎等特殊处理的说明'),
    )

    # Storage
    storage_instructions = models.CharField(
        _('储存说明 | Storage Instructions'),
        max_length=200,
        blank=True,
        help_text=_('例如：冷藏保存，24小时内服用'),
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('煎药方法 | Decoction Method')
        verbose_name_plural = _('煎药方法 | Decoction Methods')
        ordering = ['name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"


class PrescriptionTemplate(models.Model):
    """
    Prescription templates for common formulas (处方模板).
    Allows practitioners to quickly create prescriptions from saved templates.
    """

    name_cn = models.CharField(
        _('模板名称(中文) | Template Name (Chinese)'),
        max_length=200,
    )

    name_en = models.CharField(
        _('模板名称(英文) | Template Name (English)'),
        max_length=200,
        blank=True,
    )

    code = models.CharField(
        _('编码 | Code'),
        max_length=20,
        unique=True,
    )

    # Based on classic formula
    based_on_formula = models.ForeignKey(
        ClassicFormula,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='templates',
        verbose_name=_('基于方剂 | Based on Formula'),
    )

    category = models.CharField(
        _('类别 | Category'),
        max_length=100,
        blank=True,
        help_text=_('例如：感冒、咳嗽、失眠等'),
    )

    description = models.TextField(
        _('描述 | Description'),
        blank=True,
    )

    # Clinical use
    indications = models.TextField(
        _('适应症 | Indications'),
        blank=True,
    )

    contraindications = models.TextField(
        _('禁忌症 | Contraindications'),
        blank=True,
    )

    # Default decoction method
    default_decoction_method = models.ForeignKey(
        DecoctionMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='templates',
        verbose_name=_('默认煎药方法 | Default Decoction Method'),
    )

    # Default dosage info
    default_doses = models.IntegerField(
        _('默认剂数 | Default Doses'),
        default=7,
    )

    # Usage notes
    modification_notes = models.TextField(
        _('加减说明 | Modification Notes'),
        blank=True,
        help_text=_('常见的加减变化'),
    )

    usage_notes = models.TextField(
        _('使用说明 | Usage Notes'),
        blank=True,
    )

    # Creator
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescription_templates',
        verbose_name=_('创建者 | Created By'),
    )

    # Visibility
    is_public = models.BooleanField(
        _('公开模板 | Public Template'),
        default=False,
        help_text=_('公开模板可被所有医师使用'),
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('处方模板 | Prescription Template')
        verbose_name_plural = _('处方模板 | Prescription Templates')
        ordering = ['category', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} ({self.code})"


class PrescriptionTemplateItem(models.Model):
    """
    Herbs in a prescription template (模板中的药物).
    """

    template = models.ForeignKey(
        PrescriptionTemplate,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('模板 | Template'),
    )

    herb = models.ForeignKey(
        Herb,
        on_delete=models.CASCADE,
        related_name='template_items',
        verbose_name=_('药材 | Herb'),
    )

    dosage = models.DecimalField(
        _('剂量(克) | Dosage (g)'),
        max_digits=6,
        decimal_places=2,
    )

    preparation = models.CharField(
        _('炮制方法 | Preparation'),
        max_length=100,
        blank=True,
        help_text=_('例如：先煎、后下、包煎'),
    )

    is_optional = models.BooleanField(
        _('可选药物 | Optional'),
        default=False,
        help_text=_('标记为可选的药物可以根据症状选择性添加'),
    )

    notes = models.CharField(
        _('备注 | Notes'),
        max_length=200,
        blank=True,
    )

    sequence = models.IntegerField(
        _('顺序 | Sequence'),
        default=0,
    )

    class Meta:
        verbose_name = _('模板药物 | Template Item')
        verbose_name_plural = _('模板药物 | Template Items')
        ordering = ['sequence', 'herb__name_cn']
        unique_together = ['template', 'herb']

    def __str__(self):
        return f"{self.herb.name_cn} {self.dosage}g"
