"""
Models for Tuina/Massage Therapy (推拿治疗).
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TuinaTechnique(models.Model):
    """
    Tuina manipulation techniques (推拿手法).

    Common techniques (常用手法):
    - 推法 (Pushing)
    - 拿法 (Grasping)
    - 按法 (Pressing)
    - 摩法 (Rubbing)
    - 揉法 (Kneading)
    - 搓法 (Rolling)
    - 点法 (Pointing)
    - 拨法 (Plucking)
    - 抖法 (Shaking)
    - 扳法 (Pulling)
    - 捏法 (Pinching)
    - 击法 (Tapping)
    - 拍法 (Patting)
    """

    name_cn = models.CharField(
        _('中文名称 | Chinese Name'),
        max_length=50,
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

    category = models.CharField(
        _('类别 | Category'),
        max_length=50,
        blank=True,
        help_text=_('例如：摆动类、摩擦类、挤压类、振动类等'),
    )

    description = models.TextField(
        _('描述 | Description'),
        blank=True,
    )

    # Technique details
    method = models.TextField(
        _('操作方法 | Method'),
        blank=True,
        help_text=_('详细操作步骤和要领 | Detailed operation steps and key points'),
    )

    key_points = models.TextField(
        _('操作要领 | Key Points'),
        blank=True,
    )

    functions = models.TextField(
        _('功效 | Functions'),
        blank=True,
    )

    indications = models.TextField(
        _('适应症 | Indications'),
        blank=True,
    )

    contraindications = models.TextField(
        _('禁忌症 | Contraindications'),
        blank=True,
    )

    # Common application areas
    common_areas = models.TextField(
        _('常用部位 | Common Areas'),
        blank=True,
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('推拿手法 | Tuina Technique')
        verbose_name_plural = _('推拿手法 | Tuina Techniques')
        ordering = ['category', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"


class TuinaSession(models.Model):
    """
    Tuina therapy session record (推拿治疗记录).
    """

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='tuina_sessions',
        verbose_name=_('患者 | Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tuina_sessions',
        verbose_name=_('医师 | Practitioner'),
    )

    session_date = models.DateTimeField(
        _('治疗日期 | Session Date'),
    )

    # Chief complaint and diagnosis
    chief_complaint = models.TextField(
        _('主诉 | Chief Complaint'),
    )

    tcm_diagnosis = models.TextField(
        _('中医诊断 | TCM Diagnosis'),
        blank=True,
    )

    treatment_principle = models.TextField(
        _('治则 | Treatment Principle'),
        blank=True,
    )

    # Session details
    duration_minutes = models.IntegerField(
        _('治疗时长(分钟) | Duration (minutes)'),
        default=30,
    )

    treatment_areas = models.JSONField(
        _('治疗部位 | Treatment Areas'),
        default=list,
        help_text=_('治疗的身体部位列表 | List of body areas treated'),
    )

    # Treatment focus
    primary_focus = models.CharField(
        _('主要治疗重点 | Primary Focus'),
        max_length=200,
        blank=True,
        help_text=_('例如：颈椎病、腰痛、肩周炎等'),
    )

    # Patient condition assessment
    pain_level_before = models.IntegerField(
        _('治疗前疼痛等级 | Pain Level Before'),
        null=True,
        blank=True,
        help_text=_('0-10级，0=无痛，10=剧痛'),
    )

    pain_level_after = models.IntegerField(
        _('治疗后疼痛等级 | Pain Level After'),
        null=True,
        blank=True,
        help_text=_('0-10级'),
    )

    mobility_before = models.CharField(
        _('治疗前活动度 | Mobility Before'),
        max_length=200,
        blank=True,
    )

    mobility_after = models.CharField(
        _('治疗后活动度 | Mobility After'),
        max_length=200,
        blank=True,
    )

    # Patient feedback
    patient_sensation = models.TextField(
        _('患者感受 | Patient Sensation'),
        blank=True,
        help_text=_('治疗过程中和治疗后的感受'),
    )

    # Treatment outcome
    immediate_effect = models.TextField(
        _('即时效果 | Immediate Effect'),
        blank=True,
    )

    # Recommendations
    home_exercises = models.TextField(
        _('家庭练习 | Home Exercises'),
        blank=True,
        help_text=_('建议患者在家进行的练习'),
    )

    lifestyle_advice = models.TextField(
        _('生活建议 | Lifestyle Advice'),
        blank=True,
    )

    next_session_date = models.DateField(
        _('下次治疗日期 | Next Session Date'),
        null=True,
        blank=True,
    )

    # Attachments
    attachments = models.JSONField(
        _('附件 | Attachments'),
        default=list,
        blank=True,
    )

    notes = models.TextField(
        _('备注 | Notes'),
        blank=True,
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('推拿记录 | Tuina Session')
        verbose_name_plural = _('推拿记录 | Tuina Sessions')
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.session_date.strftime('%Y-%m-%d')}"


class TuinaSessionTechnique(models.Model):
    """
    Techniques used in a tuina session (治疗中使用的手法).
    """

    session = models.ForeignKey(
        TuinaSession,
        on_delete=models.CASCADE,
        related_name='techniques_used',
        verbose_name=_('治疗记录 | Session'),
    )

    technique = models.ForeignKey(
        TuinaTechnique,
        on_delete=models.CASCADE,
        related_name='session_uses',
        verbose_name=_('手法 | Technique'),
    )

    body_area = models.CharField(
        _('治疗部位 | Body Area'),
        max_length=100,
        help_text=_('例如：颈部、肩部、腰部、背部等'),
    )

    duration_minutes = models.IntegerField(
        _('时长(分钟) | Duration (minutes)'),
        default=5,
    )

    intensity = models.CharField(
        _('力度 | Intensity'),
        max_length=50,
        blank=True,
        help_text=_('例如：轻、中、重'),
    )

    repetitions = models.IntegerField(
        _('重复次数 | Repetitions'),
        null=True,
        blank=True,
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
        verbose_name = _('治疗手法记录 | Session Technique')
        verbose_name_plural = _('治疗手法记录 | Session Techniques')
        ordering = ['sequence', 'technique']

    def __str__(self):
        return f"{self.technique.name_cn} - {self.body_area}"
