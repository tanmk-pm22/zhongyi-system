"""
Models for Cupping Therapy (拔罐治疗).
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class CuppingTechnique(models.Model):
    """
    Cupping technique types (拔罐手法类型).

    Common techniques:
    - 留罐 (Retained cupping)
    - 闪罐 (Flash cupping)
    - 走罐 (Moving cupping)
    - 刺络拔罐 (Bloodletting cupping)
    - 针罐 (Acupuncture with cupping)
    - 药罐 (Herbal cupping)
    - 水罐 (Water cupping)
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

    description = models.TextField(
        _('描述 | Description'),
        blank=True,
    )

    # Technique details
    method = models.TextField(
        _('操作方法 | Method'),
        blank=True,
        help_text=_('详细操作步骤 | Detailed operation steps'),
    )

    indications = models.TextField(
        _('适应症 | Indications'),
        blank=True,
    )

    contraindications = models.TextField(
        _('禁忌症 | Contraindications'),
        blank=True,
    )

    precautions = models.TextField(
        _('注意事项 | Precautions'),
        blank=True,
    )

    typical_duration = models.IntegerField(
        _('典型时长(分钟) | Typical Duration (minutes)'),
        default=10,
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('拔罐手法 | Cupping Technique')
        verbose_name_plural = _('拔罐手法 | Cupping Techniques')
        ordering = ['name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"


class CuppingSession(models.Model):
    """
    Cupping therapy session record (拔罐治疗记录).
    """

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='cupping_sessions',
        verbose_name=_('患者 | Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cupping_sessions',
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

    # Session duration
    duration_minutes = models.IntegerField(
        _('治疗时长(分钟) | Duration (minutes)'),
        default=15,
    )

    # Body diagram/locations
    treatment_locations = models.JSONField(
        _('治疗部位 | Treatment Locations'),
        default=list,
        help_text=_('身体部位列表 | List of body locations treated'),
    )

    # Cupping marks/reactions
    skin_reaction = models.CharField(
        _('皮肤反应 | Skin Reaction'),
        max_length=200,
        blank=True,
        help_text=_('例如：淡红、紫红、黑紫、有水泡等'),
    )

    cup_marks_description = models.TextField(
        _('罐印描述 | Cup Marks Description'),
        blank=True,
    )

    # Patient feedback
    patient_sensation = models.TextField(
        _('患者感受 | Patient Sensation'),
        blank=True,
        help_text=_('治疗过程中和治疗后的感受'),
    )

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

    # Treatment outcome
    immediate_effect = models.TextField(
        _('即时效果 | Immediate Effect'),
        blank=True,
    )

    # Recommendations
    post_treatment_advice = models.TextField(
        _('治疗后建议 | Post-Treatment Advice'),
        blank=True,
    )

    next_session_date = models.DateField(
        _('下次治疗日期 | Next Session Date'),
        null=True,
        blank=True,
    )

    # Attachments (photos of cup marks, etc.)
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
        verbose_name = _('拔罐记录 | Cupping Session')
        verbose_name_plural = _('拔罐记录 | Cupping Sessions')
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.session_date.strftime('%Y-%m-%d')}"


class CuppingSessionTechnique(models.Model):
    """
    Techniques used in a cupping session (治疗中使用的手法).
    """

    session = models.ForeignKey(
        CuppingSession,
        on_delete=models.CASCADE,
        related_name='techniques_used',
        verbose_name=_('治疗记录 | Session'),
    )

    technique = models.ForeignKey(
        CuppingTechnique,
        on_delete=models.CASCADE,
        related_name='session_uses',
        verbose_name=_('手法 | Technique'),
    )

    body_location = models.CharField(
        _('治疗部位 | Body Location'),
        max_length=100,
        help_text=_('例如：背部、肩部、腰部等'),
    )

    duration_minutes = models.IntegerField(
        _('时长(分钟) | Duration (minutes)'),
        default=10,
    )

    number_of_cups = models.IntegerField(
        _('罐数 | Number of Cups'),
        default=1,
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
        return f"{self.technique.name_cn} - {self.body_location}"
