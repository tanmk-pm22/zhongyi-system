"""
Models for Treatment Course Management (疗程管理).
Track complete treatment courses across multiple sessions and treatment modalities.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class TreatmentCourse(models.Model):
    """
    Treatment course for managing a complete treatment plan (疗程).
    A course may include multiple sessions of different treatment types.
    """

    class Status(models.TextChoices):
        PLANNED = 'planned', _('计划中 | Planned')
        ACTIVE = 'active', _('进行中 | Active')
        PAUSED = 'paused', _('暂停 | Paused')
        COMPLETED = 'completed', _('已完成 | Completed')
        CANCELLED = 'cancelled', _('已取消 | Cancelled')

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='treatment_courses',
        verbose_name=_('患者 | Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='treatment_courses',
        verbose_name=_('主治医师 | Primary Practitioner'),
    )

    # Course identification
    course_number = models.CharField(
        _('疗程编号 | Course Number'),
        max_length=50,
        unique=True,
    )

    course_name = models.CharField(
        _('疗程名称 | Course Name'),
        max_length=200,
        help_text=_('例如：颈椎病综合治疗疗程'),
    )

    # Diagnosis and treatment plan
    primary_diagnosis = models.TextField(
        _('主要诊断 | Primary Diagnosis'),
    )

    treatment_goal = models.TextField(
        _('治疗目标 | Treatment Goal'),
        help_text=_('疗程的预期治疗目标'),
    )

    treatment_plan = models.TextField(
        _('治疗方案 | Treatment Plan'),
        help_text=_('详细的治疗计划和方案'),
    )

    # Course timeline
    start_date = models.DateField(
        _('开始日期 | Start Date'),
    )

    planned_end_date = models.DateField(
        _('计划结束日期 | Planned End Date'),
        null=True,
        blank=True,
    )

    actual_end_date = models.DateField(
        _('实际结束日期 | Actual End Date'),
        null=True,
        blank=True,
    )

    # Planned sessions
    planned_sessions_total = models.IntegerField(
        _('计划总次数 | Planned Total Sessions'),
        default=10,
    )

    planned_frequency = models.CharField(
        _('计划频率 | Planned Frequency'),
        max_length=100,
        blank=True,
        help_text=_('例如：每周2-3次'),
    )

    # Treatment modalities included
    includes_herbal_medicine = models.BooleanField(
        _('包含中药 | Includes Herbal Medicine'),
        default=False,
    )

    includes_acupuncture = models.BooleanField(
        _('包含针灸 | Includes Acupuncture'),
        default=False,
    )

    includes_cupping = models.BooleanField(
        _('包含拔罐 | Includes Cupping'),
        default=False,
    )

    includes_tuina = models.BooleanField(
        _('包含推拿 | Includes Tuina'),
        default=False,
    )

    other_treatments = models.CharField(
        _('其他治疗 | Other Treatments'),
        max_length=200,
        blank=True,
    )

    # Status
    status = models.CharField(
        _('状态 | Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
    )

    # Progress tracking
    progress_notes = models.TextField(
        _('进展备注 | Progress Notes'),
        blank=True,
    )

    # Outcome measurement
    outcome_assessment = models.TextField(
        _('疗效评估 | Outcome Assessment'),
        blank=True,
    )

    patient_satisfaction = models.IntegerField(
        _('患者满意度 | Patient Satisfaction'),
        null=True,
        blank=True,
        help_text=_('1-10分，10分最满意'),
    )

    # Financial
    estimated_cost = models.DecimalField(
        _('预估费用 | Estimated Cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    actual_cost = models.DecimalField(
        _('实际费用 | Actual Cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
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
        verbose_name = _('治疗疗程 | Treatment Course')
        verbose_name_plural = _('治疗疗程 | Treatment Courses')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.course_name} ({self.course_number})"

    def save(self, *args, **kwargs):
        if not self.course_number:
            # Generate course number
            from django.utils import timezone
            import random
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = str(random.randint(1000, 9999))
            self.course_number = f"TC{date_str}{random_str}"
        super().save(*args, **kwargs)

    @property
    def completed_sessions_count(self):
        """Get count of completed sessions."""
        return self.sessions.filter(status='completed').count()

    @property
    def progress_percentage(self):
        """Calculate progress percentage."""
        if self.planned_sessions_total > 0:
            return round((self.completed_sessions_count / self.planned_sessions_total) * 100, 1)
        return 0

    @property
    def remaining_sessions(self):
        """Calculate remaining sessions."""
        return max(0, self.planned_sessions_total - self.completed_sessions_count)


class CourseSession(models.Model):
    """
    Individual session within a treatment course (疗程中的单次治疗).
    Links to specific treatment records (prescriptions, acupuncture, etc.)
    """

    class SessionType(models.TextChoices):
        HERBAL = 'herbal', _('中药 | Herbal Medicine')
        ACUPUNCTURE = 'acupuncture', _('针灸 | Acupuncture')
        CUPPING = 'cupping', _('拔罐 | Cupping')
        TUINA = 'tuina', _('推拿 | Tuina')
        CONSULTATION = 'consultation', _('咨询 | Consultation')
        ASSESSMENT = 'assessment', _('评估 | Assessment')
        OTHER = 'other', _('其他 | Other')

    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', _('已预约 | Scheduled')
        COMPLETED = 'completed', _('已完成 | Completed')
        CANCELLED = 'cancelled', _('已取消 | Cancelled')
        NO_SHOW = 'no_show', _('缺席 | No Show')

    course = models.ForeignKey(
        TreatmentCourse,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('疗程 | Course'),
    )

    session_number = models.IntegerField(
        _('第几次 | Session Number'),
        help_text=_('在疗程中的第几次治疗'),
    )

    session_type = models.CharField(
        _('治疗类型 | Session Type'),
        max_length=20,
        choices=SessionType.choices,
    )

    # Scheduling
    scheduled_date = models.DateTimeField(
        _('预约时间 | Scheduled Date'),
    )

    actual_date = models.DateTimeField(
        _('实际治疗时间 | Actual Date'),
        null=True,
        blank=True,
    )

    # Practitioner
    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='course_sessions',
        verbose_name=_('医师 | Practitioner'),
    )

    # Linked treatment records
    prescription = models.ForeignKey(
        'prescriptions.Prescription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_sessions',
        verbose_name=_('处方 | Prescription'),
    )

    acupuncture_session = models.ForeignKey(
        'acupuncture.AcupunctureSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_sessions',
        verbose_name=_('针灸记录 | Acupuncture Session'),
    )

    cupping_session = models.ForeignKey(
        'cupping.CuppingSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_sessions',
        verbose_name=_('拔罐记录 | Cupping Session'),
    )

    tuina_session = models.ForeignKey(
        'tuina.TuinaSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_sessions',
        verbose_name=_('推拿记录 | Tuina Session'),
    )

    # Session details
    chief_complaint = models.TextField(
        _('主诉 | Chief Complaint'),
        blank=True,
    )

    session_notes = models.TextField(
        _('治疗记录 | Session Notes'),
        blank=True,
    )

    # Outcome for this session
    patient_response = models.TextField(
        _('患者反应 | Patient Response'),
        blank=True,
    )

    effectiveness_rating = models.IntegerField(
        _('疗效评分 | Effectiveness Rating'),
        null=True,
        blank=True,
        help_text=_('1-5分，5分效果最好'),
    )

    # Status
    status = models.CharField(
        _('状态 | Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    # Cost for this session
    session_cost = models.DecimalField(
        _('费用 | Cost'),
        max_digits=10,
        decimal_places=2,
        null=True,
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
        verbose_name = _('疗程治疗记录 | Course Session')
        verbose_name_plural = _('疗程治疗记录 | Course Sessions')
        ordering = ['course', 'session_number']
        unique_together = ['course', 'session_number']

    def __str__(self):
        return f"{self.course.course_name} - 第{self.session_number}次 ({self.get_session_type_display()})"
