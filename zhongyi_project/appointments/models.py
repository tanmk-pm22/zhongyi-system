"""
Models for Appointment Management (预约管理系统).
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import time, timedelta


class AppointmentType(models.Model):
    """
    Types of appointments (预约类型).
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
        blank=True,
    )

    # Duration
    duration_minutes = models.IntegerField(
        _('时长(分钟) | Duration (minutes)'),
        default=30,
    )

    # Color for calendar display
    color_code = models.CharField(
        _('颜色代码 | Color Code'),
        max_length=7,
        default='#007bff',
        help_text=_('十六进制颜色代码，如 #007bff'),
    )

    # Requires preparation
    requires_preparation = models.BooleanField(
        _('需要准备 | Requires Preparation'),
        default=False,
    )

    preparation_notes = models.TextField(
        _('准备事项 | Preparation Notes'),
        blank=True,
        help_text=_('患者需要提前准备的事项'),
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('预约类型 | Appointment Type')
        verbose_name_plural = _('预约类型 | Appointment Types')
        ordering = ['name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"


class PractitionerSchedule(models.Model):
    """
    Practitioner working schedule (医师工作时间表).
    """

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, _('星期一 | Monday')
        TUESDAY = 2, _('星期二 | Tuesday')
        WEDNESDAY = 3, _('星期三 | Wednesday')
        THURSDAY = 4, _('星期四 | Thursday')
        FRIDAY = 5, _('星期五 | Friday')
        SATURDAY = 6, _('星期六 | Saturday')
        SUNDAY = 7, _('星期日 | Sunday')

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_schedules',
        verbose_name=_('医师 | Practitioner'),
    )

    day_of_week = models.IntegerField(
        _('星期 | Day of Week'),
        choices=DayOfWeek.choices,
    )

    start_time = models.TimeField(
        _('开始时间 | Start Time'),
    )

    end_time = models.TimeField(
        _('结束时间 | End Time'),
    )

    # Time slot duration
    slot_duration_minutes = models.IntegerField(
        _('时间段时长(分钟) | Slot Duration (minutes)'),
        default=30,
        help_text=_('预约时间段的长度'),
    )

    # Maximum appointments per slot
    max_appointments_per_slot = models.IntegerField(
        _('每时段最大预约数 | Max Appointments per Slot'),
        default=1,
    )

    # Validity period
    effective_from = models.DateField(
        _('生效日期 | Effective From'),
        null=True,
        blank=True,
    )

    effective_to = models.DateField(
        _('失效日期 | Effective To'),
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
        verbose_name = _('医师排班 | Practitioner Schedule')
        verbose_name_plural = _('医师排班 | Practitioner Schedules')
        ordering = ['practitioner', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.practitioner.get_full_name()} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    """
    Patient appointment (患者预约).
    """

    class Status(models.TextChoices):
        PENDING = 'pending', _('待确认 | Pending')
        CONFIRMED = 'confirmed', _('已确认 | Confirmed')
        ARRIVED = 'arrived', _('已到达 | Arrived')
        IN_PROGRESS = 'in_progress', _('进行中 | In Progress')
        COMPLETED = 'completed', _('已完成 | Completed')
        CANCELLED = 'cancelled', _('已取消 | Cancelled')
        NO_SHOW = 'no_show', _('缺席 | No Show')

    class CancellationReason(models.TextChoices):
        PATIENT_REQUEST = 'patient_request', _('患者要求 | Patient Request')
        PRACTITIONER_UNAVAILABLE = 'practitioner_unavailable', _('医师不可用 | Practitioner Unavailable')
        EMERGENCY = 'emergency', _('紧急情况 | Emergency')
        WEATHER = 'weather', _('天气原因 | Weather')
        OTHER = 'other', _('其他 | Other')

    # Identification
    appointment_number = models.CharField(
        _('预约编号 | Appointment Number'),
        max_length=50,
        unique=True,
    )

    # Patient and Practitioner
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('患者 | Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments',
        verbose_name=_('医师 | Practitioner'),
    )

    # Appointment details
    appointment_type = models.ForeignKey(
        AppointmentType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments',
        verbose_name=_('预约类型 | Appointment Type'),
    )

    appointment_date = models.DateField(
        _('预约日期 | Appointment Date'),
    )

    start_time = models.TimeField(
        _('开始时间 | Start Time'),
    )

    end_time = models.TimeField(
        _('结束时间 | End Time'),
    )

    # Reason
    reason = models.TextField(
        _('就诊原因 | Reason for Visit'),
        blank=True,
    )

    chief_complaint = models.TextField(
        _('主诉 | Chief Complaint'),
        blank=True,
    )

    # Status
    status = models.CharField(
        _('状态 | Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Confirmation
    confirmed_at = models.DateTimeField(
        _('确认时间 | Confirmed At'),
        null=True,
        blank=True,
    )

    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_appointments',
        verbose_name=_('确认人 | Confirmed By'),
    )

    # Arrival
    arrival_time = models.DateTimeField(
        _('到达时间 | Arrival Time'),
        null=True,
        blank=True,
    )

    # Cancellation
    cancelled_at = models.DateTimeField(
        _('取消时间 | Cancelled At'),
        null=True,
        blank=True,
    )

    cancellation_reason = models.CharField(
        _('取消原因 | Cancellation Reason'),
        max_length=30,
        choices=CancellationReason.choices,
        blank=True,
    )

    cancellation_notes = models.TextField(
        _('取消备注 | Cancellation Notes'),
        blank=True,
    )

    # Reminders
    reminder_sent = models.BooleanField(
        _('已发送提醒 | Reminder Sent'),
        default=False,
    )

    reminder_sent_at = models.DateTimeField(
        _('提醒发送时间 | Reminder Sent At'),
        null=True,
        blank=True,
    )

    # Follow-up from previous visit
    is_followup = models.BooleanField(
        _('复诊 | Is Follow-up'),
        default=False,
    )

    previous_appointment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='followup_appointments',
        verbose_name=_('上次预约 | Previous Appointment'),
    )

    # Linked treatment records
    diagnosis_session = models.ForeignKey(
        'diagnosis.DiagnosisSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name=_('诊断记录 | Diagnosis Session'),
    )

    notes = models.TextField(
        _('备注 | Notes'),
        blank=True,
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_appointments',
        verbose_name=_('创建人 | Created By'),
    )

    class Meta:
        verbose_name = _('预约 | Appointment')
        verbose_name_plural = _('预约 | Appointments')
        ordering = ['-appointment_date', '-start_time']

    def __str__(self):
        return f"{self.appointment_number} - {self.patient.full_name} ({self.appointment_date} {self.start_time})"

    def save(self, *args, **kwargs):
        if not self.appointment_number:
            # Generate appointment number
            from django.utils import timezone
            import random
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = str(random.randint(1000, 9999))
            self.appointment_number = f"APT{date_str}{random_str}"
        super().save(*args, **kwargs)

    @property
    def duration_minutes(self):
        """Calculate appointment duration in minutes."""
        if self.start_time and self.end_time:
            from datetime import datetime
            start = datetime.combine(datetime.today(), self.start_time)
            end = datetime.combine(datetime.today(), self.end_time)
            return int((end - start).total_seconds() / 60)
        return 0

    @property
    def is_past(self):
        """Check if appointment is in the past."""
        from django.utils import timezone
        from datetime import datetime
        appointment_datetime = datetime.combine(self.appointment_date, self.start_time)
        return timezone.make_aware(appointment_datetime) < timezone.now()
