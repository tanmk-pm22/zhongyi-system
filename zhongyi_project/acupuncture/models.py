from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AcupunctureSession(models.Model):
    """
    针灸治疗记录 | Acupuncture Treatment Session
    Records acupuncture treatment sessions with acupoints, techniques, and patient response.
    """

    class TreatmentType(models.TextChoices):
        TRADITIONAL = 'traditional', _('传统针灸 | Traditional Acupuncture')
        ELECTRO = 'electro', _('电针 | Electroacupuncture')
        AURICULAR = 'auricular', _('耳针 | Auricular Acupuncture')
        SCALP = 'scalp', _('头针 | Scalp Acupuncture')
        MOXIBUSTION = 'moxibustion', _('艾灸 | Moxibustion')
        CUPPING = 'cupping', _('拔罐 | Cupping Therapy')
        LASER = 'laser', _('激光针灸 | Laser Acupuncture')
        MAGNETIC = 'magnetic', _('磁疗针灸 | Magnetic Acupuncture')
        WARMING = 'warming', _('温针灸 | Warming Needle')
        FIRE_NEEDLE = 'fire_needle', _('火针 | Fire Needling')
        BLOODLETTING = 'bloodletting', _('刺络放血 | Bloodletting Therapy')

    class NeedleRetention(models.TextChoices):
        SHORT = '15min', _('15分钟 | 15 minutes')
        MEDIUM = '20min', _('20分钟 | 20 minutes')
        STANDARD = '30min', _('30分钟 | 30 minutes')
        LONG = '40min', _('40分钟 | 40 minutes')

    class PatientResponse(models.TextChoices):
        EXCELLENT = 'excellent', _('效果显著 | Excellent')
        GOOD = 'good', _('效果良好 | Good')
        FAIR = 'fair', _('效果一般 | Fair')
        POOR = 'poor', _('效果不佳 | Poor')
        NO_CHANGE = 'no_change', _('无明显变化 | No Change')

    # Patient information
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='acupuncture_sessions',
        verbose_name=_('患者 | Patient')
    )

    # Session details
    session_date = models.DateField(_('治疗日期 | Session Date'))
    treatment_type = models.CharField(
        _('治疗类型 | Treatment Type'),
        max_length=20,
        choices=TreatmentType.choices,
        default=TreatmentType.TRADITIONAL
    )

    # Chief complaint and diagnosis
    chief_complaint = models.TextField(
        _('主诉 | Chief Complaint'),
        help_text=_('患者主要不适症状 | Main symptoms patient is experiencing')
    )
    tcm_diagnosis = models.TextField(
        _('中医诊断 | TCM Diagnosis'),
        help_text=_('中医辨证诊断结果 | TCM pattern differentiation diagnosis')
    )

    # Treatment details
    acupoints_used = models.TextField(
        _('使用穴位 | Acupoints Used'),
        help_text=_('例如：合谷(LI4), 太冲(LR3), 足三里(ST36) | e.g., Hegu (LI4), Taichong (LR3), Zusanli (ST36)')
    )
    needle_retention_time = models.CharField(
        _('留针时间 | Needle Retention Time'),
        max_length=10,
        choices=NeedleRetention.choices,
        default=NeedleRetention.STANDARD
    )
    technique_notes = models.TextField(
        _('手法说明 | Technique Notes'),
        blank=True,
        help_text=_('针刺手法、深度、刺激强度等 | Needling technique, depth, stimulation intensity, etc.')
    )

    # Additional treatments
    used_moxibustion = models.BooleanField(
        _('配合艾灸 | Used Moxibustion'),
        default=False
    )
    used_cupping = models.BooleanField(
        _('配合拔罐 | Used Cupping'),
        default=False
    )
    used_tuina = models.BooleanField(
        _('配合推拿 | Used Tuina Massage'),
        default=False
    )

    # Treatment response and notes
    patient_response = models.CharField(
        _('患者反应 | Patient Response'),
        max_length=20,
        choices=PatientResponse.choices,
        blank=True
    )
    treatment_notes = models.TextField(
        _('治疗备注 | Treatment Notes'),
        blank=True,
        help_text=_('患者感受、注意事项、建议等 | Patient feedback, precautions, recommendations, etc.')
    )

    # Next session planning
    next_session_date = models.DateField(
        _('下次复诊日期 | Next Session Date'),
        null=True,
        blank=True
    )
    treatment_plan = models.TextField(
        _('治疗计划 | Treatment Plan'),
        blank=True,
        help_text=_('后续治疗计划和建议 | Follow-up treatment plan and recommendations')
    )

    # Cost information
    session_fee = models.DecimalField(
        _('治疗费用 | Session Fee'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('马币 | MYR')
    )

    # AI Recommendations (Modern Enhancement)
    ai_suggested_acupoints = models.TextField(
        _('AI建议穴位 | AI Suggested Acupoints'),
        blank=True,
        help_text=_('基于症状的AI推荐穴位 | AI-recommended acupoints based on symptoms')
    )
    ai_confidence_score = models.DecimalField(
        _('AI置信度 | AI Confidence Score'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('AI建议的置信度 (0-100) | Confidence level of AI suggestion (0-100)')
    )
    ai_recommendation_used = models.BooleanField(
        _('采用AI建议 | Used AI Recommendation'),
        default=False,
        help_text=_('是否采用了AI建议的穴位 | Whether AI-suggested acupoints were used')
    )
    ai_reasoning = models.TextField(
        _('AI推理依据 | AI Reasoning'),
        blank=True,
        help_text=_('AI推荐的理论依据 | Theoretical basis for AI recommendation')
    )

    # Required: Relationship to practitioner
    assigned_practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acupuncture_sessions',
        verbose_name=_('负责医师 | Assigned Practitioner')
    )

    # Required: Timestamps
    created_at = models.DateTimeField(_('创建时间 | Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间 | Updated At'), auto_now=True)

    # Required: Soft delete support
    is_active = models.BooleanField(_('活跃 | Active'), default=True)

    class Meta:
        verbose_name = _('针灸治疗 | Acupuncture Session')
        verbose_name_plural = _('针灸治疗记录 | Acupuncture Sessions')
        ordering = ['-session_date', '-created_at']
        indexes = [
            models.Index(fields=['-session_date', '-created_at']),
            models.Index(fields=['patient', '-session_date']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.session_date} - {self.get_treatment_type_display()}"

    def get_acupoints_list(self):
        """Return list of acupoints used."""
        return [point.strip() for point in self.acupoints_used.split(',') if point.strip()]

    def get_additional_treatments(self):
        """Return list of additional treatments used."""
        treatments = []
        if self.used_moxibustion:
            treatments.append(_('艾灸 | Moxibustion'))
        if self.used_cupping:
            treatments.append(_('拔罐 | Cupping'))
        if self.used_tuina:
            treatments.append(_('推拿 | Tuina'))
        return treatments


class AcupointReference(models.Model):
    """
    穴位参考资料 | Acupoint Reference Library
    3D acupoint reference with images, locations, and indications.
    """

    class MeridianType(models.TextChoices):
        LUNG = 'LU', _('手太阴肺经 | Lung Meridian')
        LARGE_INTESTINE = 'LI', _('手阳明大肠经 | Large Intestine Meridian')
        STOMACH = 'ST', _('足阳明胃经 | Stomach Meridian')
        SPLEEN = 'SP', _('足太阴脾经 | Spleen Meridian')
        HEART = 'HT', _('手少阴心经 | Heart Meridian')
        SMALL_INTESTINE = 'SI', _('手太阳小肠经 | Small Intestine Meridian')
        BLADDER = 'BL', _('足太阳膀胱经 | Bladder Meridian')
        KIDNEY = 'KI', _('足少阴肾经 | Kidney Meridian')
        PERICARDIUM = 'PC', _('手厥阴心包经 | Pericardium Meridian')
        TRIPLE_BURNER = 'TB', _('手少阳三焦经 | Triple Burner Meridian')
        GALLBLADDER = 'GB', _('足少阳胆经 | Gallbladder Meridian')
        LIVER = 'LR', _('足厥阴肝经 | Liver Meridian')
        GOVERNING_VESSEL = 'GV', _('督脉 | Governing Vessel')
        CONCEPTION_VESSEL = 'CV', _('任脉 | Conception Vessel')
        EXTRA = 'EX', _('经外奇穴 | Extra Points')

    # Basic Information
    code = models.CharField(
        _('穴位编码 | Acupoint Code'),
        max_length=10,
        unique=True,
        help_text=_('例如：LI4, ST36 | e.g., LI4, ST36')
    )
    chinese_name = models.CharField(
        _('中文名称 | Chinese Name'),
        max_length=50,
        help_text=_('例如：合谷 | e.g., Hegu')
    )
    pinyin_name = models.CharField(
        _('拼音名称 | Pinyin Name'),
        max_length=50,
        help_text=_('例如：Hegu | e.g., Hegu')
    )
    english_name = models.CharField(
        _('英文名称 | English Name'),
        max_length=100,
        blank=True,
        help_text=_('例如：Union Valley | e.g., Union Valley')
    )
    meridian = models.CharField(
        _('所属经络 | Meridian'),
        max_length=2,
        choices=MeridianType.choices
    )

    # Location
    location_chinese = models.TextField(
        _('定位（中文）| Location (Chinese)'),
        help_text=_('穴位的精确位置描述 | Precise location description')
    )
    location_english = models.TextField(
        _('定位（英文）| Location (English)'),
        blank=True
    )

    # Images and 3D Data
    image_2d = models.ImageField(
        _('2D图片 | 2D Image'),
        upload_to='acupoints/2d/',
        null=True,
        blank=True,
        help_text=_('穴位2D示意图 | 2D illustration of acupoint')
    )
    image_3d = models.ImageField(
        _('3D图片 | 3D Image'),
        upload_to='acupoints/3d/',
        null=True,
        blank=True,
        help_text=_('穴位3D示意图 | 3D illustration of acupoint')
    )
    video_url = models.URLField(
        _('视频链接 | Video URL'),
        blank=True,
        help_text=_('穴位演示视频URL | Demonstration video URL')
    )

    # Clinical Information
    indications = models.TextField(
        _('主治 | Indications'),
        help_text=_('主治病症 | Main indications for treatment')
    )
    functions = models.TextField(
        _('功效 | Functions'),
        help_text=_('穴位功效 | Therapeutic functions')
    )
    techniques = models.TextField(
        _('针刺方法 | Needling Techniques'),
        blank=True,
        help_text=_('进针深度、角度、手法 | Needle depth, angle, manipulation')
    )
    precautions = models.TextField(
        _('注意事项 | Precautions'),
        blank=True,
        help_text=_('禁忌症和注意事项 | Contraindications and precautions')
    )

    # Popularity and Usage Statistics
    usage_count = models.IntegerField(
        _('使用次数 | Usage Count'),
        default=0,
        help_text=_('在系统中被使用的次数 | Times used in the system')
    )
    effectiveness_rating = models.DecimalField(
        _('有效率 | Effectiveness Rating'),
        max_digits=4,
        decimal_places=2,
        default=0.00,
        help_text=_('基于治疗反馈的有效率 | Effectiveness based on treatment feedback')
    )

    # Metadata
    created_at = models.DateTimeField(_('创建时间 | Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间 | Updated At'), auto_now=True)
    is_active = models.BooleanField(_('活跃 | Active'), default=True)

    class Meta:
        verbose_name = _('穴位参考 | Acupoint Reference')
        verbose_name_plural = _('穴位参考库 | Acupoint Reference Library')
        ordering = ['meridian', 'code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['meridian']),
            models.Index(fields=['-usage_count']),
        ]

    def __str__(self):
        return f"{self.code} - {self.chinese_name} ({self.pinyin_name})"

    def increment_usage(self):
        """Increment usage count when acupoint is used in a session."""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

    def update_effectiveness(self, session_response):
        """Update effectiveness rating based on treatment response."""
        # Simple algorithm: update running average
        weight_map = {
            'excellent': 1.0,
            'good': 0.75,
            'fair': 0.5,
            'poor': 0.25,
            'no_change': 0.0
        }
        if session_response in weight_map and self.usage_count > 0:
            current_total = self.effectiveness_rating * (self.usage_count - 1)
            new_rating = (current_total + weight_map[session_response] * 100) / self.usage_count
            self.effectiveness_rating = round(new_rating, 2)
            self.save(update_fields=['effectiveness_rating'])
