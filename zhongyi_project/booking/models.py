from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from patients.models import Patient


class Appointment(models.Model):
    """预约记录 | Appointment"""

    STATUS_CHOICES = [
        ('pending', _('待确认 | Pending')),
        ('confirmed', _('已确认 | Confirmed')),
        ('completed', _('已完成 | Completed')),
        ('cancelled', _('已取消 | Cancelled')),
        ('no_show', _('未到诊 | No Show')),
    ]

    SERVICE_TYPE_CHOICES = [
        ('internal_medicine', _('中医内科 | Internal Medicine')),
        ('acupuncture', _('针灸治疗 | Acupuncture')),
        ('tuina', _('推拿按摩 | Tuina Massage')),
        ('herbal_consultation', _('中药咨询 | Herbal Consultation')),
        ('health_assessment', _('健康评估 | Health Assessment')),
        ('follow_up', _('复诊 | Follow-up')),
        ('other', _('其他 | Other')),
    ]

    # 基本信息 | Basic Information
    appointment_number = models.CharField(
        _('预约号 | Appointment Number'),
        max_length=50,
        unique=True,
        editable=False
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name=_('患者 | Patient'),
        null=True,
        blank=True
    )

    practitioner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name=_('医师 | Practitioner'),
        limit_choices_to={'role': 'practitioner'}
    )

    # 预约详情 | Appointment Details
    service_type = models.CharField(
        _('服务类型 | Service Type'),
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        default='internal_medicine'
    )

    appointment_date = models.DateField(
        _('预约日期 | Appointment Date')
    )

    appointment_time = models.TimeField(
        _('预约时间 | Appointment Time')
    )

    duration_minutes = models.IntegerField(
        _('预计时长（分钟） | Duration (Minutes)'),
        default=30,
        help_text='30分钟 | 30 minutes'
    )

    # 患者信息（用于未注册患者）| Patient Info (for walk-in patients)
    patient_name = models.CharField(
        _('患者姓名 | Patient Name'),
        max_length=200,
        blank=True,
        help_text='如果患者已注册，此字段可留空 | Leave blank if patient is registered'
    )

    patient_phone = models.CharField(
        _('联系电话 | Contact Phone'),
        max_length=50,
        blank=True
    )

    patient_email = models.EmailField(
        _('邮箱 | Email'),
        blank=True
    )

    # 主诉和备注 | Chief Complaint and Notes
    chief_complaint = models.TextField(
        _('主诉 | Chief Complaint'),
        blank=True,
        help_text='简述主要症状或就诊原因 | Brief description of main symptoms or reason for visit'
    )

    notes = models.TextField(
        _('备注 | Notes'),
        blank=True
    )

    internal_notes = models.TextField(
        _('内部备注 | Internal Notes'),
        blank=True,
        help_text='仅医师和管理员可见 | Visible to practitioners and admins only'
    )

    # 状态管理 | Status Management
    status = models.CharField(
        _('状态 | Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_first_visit = models.BooleanField(
        _('首诊 | First Visit'),
        default=True
    )

    # 提醒和通知 | Reminders and Notifications
    reminder_sent = models.BooleanField(
        _('已发送提醒 | Reminder Sent'),
        default=False
    )

    reminder_sent_at = models.DateTimeField(
        _('提醒发送时间 | Reminder Sent At'),
        null=True,
        blank=True
    )

    confirmation_sent = models.BooleanField(
        _('已发送确认 | Confirmation Sent'),
        default=False
    )

    confirmation_sent_at = models.DateTimeField(
        _('确认发送时间 | Confirmation Sent At'),
        null=True,
        blank=True
    )

    # 取消信息 | Cancellation Information
    cancelled_at = models.DateTimeField(
        _('取消时间 | Cancelled At'),
        null=True,
        blank=True
    )

    cancellation_reason = models.TextField(
        _('取消原因 | Cancellation Reason'),
        blank=True
    )

    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_appointments',
        verbose_name=_('取消人 | Cancelled By')
    )

    # 时间戳 | Timestamps
    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )

    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('预约 | Appointment')
        verbose_name_plural = _('预约 | Appointments')
        ordering = ['-appointment_date', '-appointment_time']
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['practitioner', 'appointment_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        patient_display = self.patient.get_full_name() if self.patient else self.patient_name
        return f"{self.appointment_number} - {patient_display} ({self.appointment_date} {self.appointment_time})"

    def clean(self):
        """验证预约数据 | Validate appointment data"""
        super().clean()

        # 确保有患者信息 | Ensure patient information exists
        if not self.patient and not self.patient_name:
            raise ValidationError({
                'patient_name': _('必须提供患者或患者姓名 | Patient or patient name must be provided')
            })

        # 验证预约时间不能在过去 | Validate appointment time is not in the past
        if self.appointment_date and self.appointment_time:
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(self.appointment_date, self.appointment_time)
            )
            if appointment_datetime < timezone.now() and not self.pk:
                raise ValidationError({
                    'appointment_date': _('预约时间不能在过去 | Appointment time cannot be in the past')
                })

    def save(self, *args, **kwargs):
        # 自动生成预约号 | Auto-generate appointment number
        if not self.appointment_number:
            date_str = self.appointment_date.strftime('%Y%m%d')
            last_appointment = Appointment.objects.filter(
                appointment_number__startswith=f'APT{date_str}'
            ).order_by('-appointment_number').first()

            if last_appointment:
                last_seq = int(last_appointment.appointment_number[-4:])
                new_seq = last_seq + 1
            else:
                new_seq = 1

            self.appointment_number = f'APT{date_str}{new_seq:04d}'

        # 如果患者已注册，使用患者信息 | Use patient info if registered
        if self.patient:
            if not self.patient_name:
                self.patient_name = self.patient.get_full_name()
            if not self.patient_phone:
                self.patient_phone = self.patient.phone
            if not self.patient_email:
                self.patient_email = self.patient.email

        super().save(*args, **kwargs)

    def get_patient_display(self):
        """获取患者显示名称 | Get patient display name"""
        if self.patient:
            return self.patient.get_full_name()
        return self.patient_name

    def get_practitioner_display(self):
        """获取医师显示名称 | Get practitioner display name"""
        if self.practitioner:
            return self.practitioner.get_full_name()
        return _('未指定 | Not assigned')

    def can_cancel(self):
        """检查是否可以取消 | Check if appointment can be cancelled"""
        return self.status in ['pending', 'confirmed']

    def can_reschedule(self):
        """检查是否可以改约 | Check if appointment can be rescheduled"""
        return self.status in ['pending', 'confirmed']

    def cancel(self, user=None, reason=''):
        """取消预约 | Cancel appointment"""
        if not self.can_cancel():
            raise ValueError(_('该预约不能被取消 | This appointment cannot be cancelled'))

        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        if user:
            self.cancelled_by = user
        self.save()

    def confirm(self):
        """确认预约 | Confirm appointment"""
        if self.status == 'pending':
            self.status = 'confirmed'
            self.save()

    def complete(self):
        """完成预约 | Complete appointment"""
        if self.status in ['pending', 'confirmed']:
            self.status = 'completed'
            self.save()

    def mark_no_show(self):
        """标记未到诊 | Mark as no show"""
        if self.status in ['pending', 'confirmed']:
            self.status = 'no_show'
            self.save()

    def is_upcoming(self):
        """检查是否为即将到来的预约 | Check if appointment is upcoming"""
        if self.appointment_date and self.appointment_time:
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(self.appointment_date, self.appointment_time)
            )
            return appointment_datetime > timezone.now()
        return False

    def is_today(self):
        """检查是否为今天的预约 | Check if appointment is today"""
        return self.appointment_date == timezone.now().date()


class TimeSlot(models.Model):
    """可用时间段 | Available Time Slot"""

    DAY_OF_WEEK_CHOICES = [
        (0, _('周一 | Monday')),
        (1, _('周二 | Tuesday')),
        (2, _('周三 | Wednesday')),
        (3, _('周四 | Thursday')),
        (4, _('周五 | Friday')),
        (5, _('周六 | Saturday')),
        (6, _('周日 | Sunday')),
    ]

    practitioner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='time_slots',
        verbose_name=_('医师 | Practitioner'),
        limit_choices_to={'role': 'practitioner'},
        null=True,
        blank=True,
        help_text='留空表示适用于所有医师 | Leave blank for all practitioners'
    )

    day_of_week = models.IntegerField(
        _('星期 | Day of Week'),
        choices=DAY_OF_WEEK_CHOICES
    )

    start_time = models.TimeField(
        _('开始时间 | Start Time')
    )

    end_time = models.TimeField(
        _('结束时间 | End Time')
    )

    slot_duration = models.IntegerField(
        _('时段时长（分钟） | Slot Duration (Minutes)'),
        default=30,
        help_text='每个预约时段的长度 | Length of each appointment slot'
    )

    max_appointments = models.IntegerField(
        _('最大预约数 | Max Appointments'),
        default=1,
        help_text='该时段最多可预约人数 | Maximum number of appointments for this slot'
    )

    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )

    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('可用时间段 | Time Slot')
        verbose_name_plural = _('可用时间段 | Time Slots')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        practitioner_name = self.practitioner.get_full_name() if self.practitioner else _('所有医师 | All Practitioners')
        day_name = dict(self.DAY_OF_WEEK_CHOICES)[self.day_of_week]
        return f"{practitioner_name} - {day_name} {self.start_time}-{self.end_time}"

    def clean(self):
        """验证时间段数据 | Validate time slot data"""
        super().clean()

        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError({
                    'end_time': _('结束时间必须晚于开始时间 | End time must be after start time')
                })


class BlockedDate(models.Model):
    """不可预约日期 | Blocked Date"""

    practitioner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_dates',
        verbose_name=_('医师 | Practitioner'),
        limit_choices_to={'role': 'practitioner'},
        null=True,
        blank=True,
        help_text='留空表示诊所休息 | Leave blank for clinic closure'
    )

    blocked_date = models.DateField(
        _('不可预约日期 | Blocked Date')
    )

    reason_cn = models.CharField(
        _('原因（中文） | Reason (Chinese)'),
        max_length=200,
        blank=True
    )

    reason_en = models.CharField(
        _('原因（英文） | Reason (English)'),
        max_length=200,
        blank=True
    )

    is_full_day = models.BooleanField(
        _('全天 | Full Day'),
        default=True
    )

    start_time = models.TimeField(
        _('开始时间 | Start Time'),
        null=True,
        blank=True,
        help_text='部分时间段不可用时填写 | Fill when partial time block'
    )

    end_time = models.TimeField(
        _('结束时间 | End Time'),
        null=True,
        blank=True,
        help_text='部分时间段不可用时填写 | Fill when partial time block'
    )

    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )

    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('不可预约日期 | Blocked Date')
        verbose_name_plural = _('不可预约日期 | Blocked Dates')
        ordering = ['-blocked_date']

    def __str__(self):
        practitioner_name = self.practitioner.get_full_name() if self.practitioner else _('诊所 | Clinic')
        return f"{practitioner_name} - {self.blocked_date}"
