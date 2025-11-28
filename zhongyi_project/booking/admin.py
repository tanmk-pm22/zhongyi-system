from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Appointment, TimeSlot, BlockedDate


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_number', 'get_patient_name', 'get_practitioner_name', 'service_type', 'appointment_date', 'appointment_time', 'status_badge', 'created_at')
    list_filter = ('status', 'service_type', 'is_first_visit', 'appointment_date', 'created_at')
    search_fields = ('appointment_number', 'patient_name', 'patient_phone', 'patient_email', 'chief_complaint')
    ordering = ('-appointment_date', '-appointment_time')
    date_hierarchy = 'appointment_date'

    fieldsets = (
        (_('预约信息 | Appointment Information'), {
            'fields': ('appointment_number', 'patient', 'practitioner', 'service_type', 'appointment_date', 'appointment_time', 'duration_minutes')
        }),
        (_('患者信息 | Patient Information'), {
            'fields': ('patient_name', 'patient_phone', 'patient_email'),
            'description': _('如果患者已注册，这些字段会自动填充 | These fields will auto-fill if patient is registered')
        }),
        (_('主诉和备注 | Chief Complaint & Notes'), {
            'fields': ('chief_complaint', 'notes', 'internal_notes', 'is_first_visit')
        }),
        (_('状态 | Status'), {
            'fields': ('status',)
        }),
        (_('提醒 | Reminders'), {
            'fields': ('reminder_sent', 'reminder_sent_at', 'confirmation_sent', 'confirmation_sent_at'),
            'classes': ('collapse',)
        }),
        (_('取消信息 | Cancellation Info'), {
            'fields': ('cancelled_at', 'cancellation_reason', 'cancelled_by'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('appointment_number', 'reminder_sent_at', 'confirmation_sent_at', 'cancelled_at', 'cancelled_by')

    actions = ['confirm_appointments', 'complete_appointments', 'cancel_appointments']

    def get_patient_name(self, obj):
        return obj.get_patient_display()
    get_patient_name.short_description = _('患者 | Patient')

    def get_practitioner_name(self, obj):
        return obj.get_practitioner_display()
    get_practitioner_name.short_description = _('医师 | Practitioner')

    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'completed': 'success',
            'cancelled': 'danger',
            'no_show': 'secondary',
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    status_badge.short_description = _('状态 | Status')

    def confirm_appointments(self, request, queryset):
        count = 0
        for appointment in queryset:
            if appointment.can_cancel():  # Use can_cancel as it checks for pending/confirmed
                appointment.confirm()
                count += 1
        self.message_user(request, _(f'{count} 个预约已确认 | {count} appointments confirmed'))
    confirm_appointments.short_description = _('确认选中的预约 | Confirm selected appointments')

    def complete_appointments(self, request, queryset):
        count = 0
        for appointment in queryset:
            if appointment.status in ['pending', 'confirmed']:
                appointment.complete()
                count += 1
        self.message_user(request, _(f'{count} 个预约已完成 | {count} appointments completed'))
    complete_appointments.short_description = _('标记为已完成 | Mark as completed')

    def cancel_appointments(self, request, queryset):
        count = 0
        for appointment in queryset:
            if appointment.can_cancel():
                appointment.cancel(user=request.user, reason='管理员取消 | Cancelled by admin')
                count += 1
        self.message_user(request, _(f'{count} 个预约已取消 | {count} appointments cancelled'))
    cancel_appointments.short_description = _('取消选中的预约 | Cancel selected appointments')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('practitioner', 'day_of_week_display', 'start_time', 'end_time', 'slot_duration', 'max_appointments', 'is_active')
    list_filter = ('day_of_week', 'is_active', 'practitioner')
    search_fields = ('practitioner__first_name', 'practitioner__last_name')
    ordering = ('day_of_week', 'start_time')

    fieldsets = (
        (_('医师 | Practitioner'), {
            'fields': ('practitioner',),
            'description': _('留空表示适用于所有医师 | Leave blank for all practitioners')
        }),
        (_('时间设置 | Time Settings'), {
            'fields': ('day_of_week', 'start_time', 'end_time', 'slot_duration')
        }),
        (_('预约限制 | Booking Limits'), {
            'fields': ('max_appointments',)
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
    )

    def day_of_week_display(self, obj):
        return obj.get_day_of_week_display()
    day_of_week_display.short_description = _('星期 | Day')


@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = ('practitioner', 'blocked_date', 'reason_display', 'is_full_day', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_full_day', 'is_active', 'blocked_date', 'practitioner')
    search_fields = ('reason_cn', 'reason_en')
    ordering = ('-blocked_date',)
    date_hierarchy = 'blocked_date'

    fieldsets = (
        (_('医师 | Practitioner'), {
            'fields': ('practitioner',),
            'description': _('留空表示诊所休息 | Leave blank for clinic closure')
        }),
        (_('日期 | Date'), {
            'fields': ('blocked_date',)
        }),
        (_('原因 | Reason'), {
            'fields': ('reason_cn', 'reason_en')
        }),
        (_('时间设置 | Time Settings'), {
            'fields': ('is_full_day', 'start_time', 'end_time'),
            'description': _('如果不是全天，请填写开始和结束时间 | If not full day, fill in start and end time')
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
    )

    def reason_display(self, obj):
        if obj.reason_cn and obj.reason_en:
            return f"{obj.reason_cn} | {obj.reason_en}"
        elif obj.reason_cn:
            return obj.reason_cn
        elif obj.reason_en:
            return obj.reason_en
        return _('无原因 | No reason')
    reason_display.short_description = _('原因 | Reason')
