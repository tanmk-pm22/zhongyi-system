"""Admin configuration for Appointments module."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AppointmentType, PractitionerSchedule, Appointment


@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
    """Admin for Appointment Types."""

    list_display = ('name_cn', 'name_en', 'code', 'duration_minutes', 'color_code', 'is_active')
    list_filter = ('is_active', 'requires_preparation')
    search_fields = ('name_cn', 'name_en', 'code')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('code', 'name_cn', 'name_en', 'description'),
        }),
        (_('设置 | Settings'), {
            'fields': ('duration_minutes', 'color_code'),
        }),
        (_('准备事项 | Preparation'), {
            'fields': ('requires_preparation', 'preparation_notes'),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(PractitionerSchedule)
class PractitionerScheduleAdmin(admin.ModelAdmin):
    """Admin for Practitioner Schedules."""

    list_display = (
        'practitioner', 'day_of_week', 'start_time', 'end_time',
        'slot_duration_minutes', 'effective_from', 'effective_to', 'is_active'
    )
    list_filter = ('day_of_week', 'practitioner', 'is_active')
    search_fields = ('practitioner__username', 'practitioner__first_name', 'practitioner__last_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('practitioner', 'day_of_week', 'start_time')

    fieldsets = (
        (_('医师 | Practitioner'), {
            'fields': ('practitioner',),
        }),
        (_('工作时间 | Working Hours'), {
            'fields': ('day_of_week', 'start_time', 'end_time'),
        }),
        (_('时间段设置 | Time Slot Settings'), {
            'fields': ('slot_duration_minutes', 'max_appointments_per_slot'),
        }),
        (_('有效期 | Validity Period'), {
            'fields': ('effective_from', 'effective_to'),
        }),
        (_('备注 | Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin for Appointments."""

    list_display = (
        'appointment_number', 'patient', 'practitioner',
        'appointment_date', 'start_time', 'end_time',
        'appointment_type', 'status', 'reminder_sent'
    )
    list_filter = (
        'status', 'appointment_date', 'appointment_type',
        'practitioner', 'is_followup', 'reminder_sent'
    )
    search_fields = (
        'appointment_number',
        'patient__first_name', 'patient__last_name', 'patient__chinese_name',
        'patient__ic_number', 'reason', 'chief_complaint'
    )
    readonly_fields = (
        'appointment_number', 'created_at', 'updated_at',
        'created_by', 'confirmed_at', 'confirmed_by',
        'arrival_time', 'cancelled_at', 'reminder_sent_at',
        'duration_minutes', 'is_past'
    )
    ordering = ('-appointment_date', '-start_time')
    date_hierarchy = 'appointment_date'

    fieldsets = (
        (_('预约信息 | Appointment Information'), {
            'fields': (
                'appointment_number', 'patient', 'practitioner',
                'appointment_type', 'is_followup', 'previous_appointment'
            ),
        }),
        (_('时间 | Time'), {
            'fields': (
                'appointment_date', 'start_time', 'end_time', 'duration_minutes'
            ),
        }),
        (_('就诊信息 | Visit Information'), {
            'fields': ('reason', 'chief_complaint'),
        }),
        (_('状态 | Status'), {
            'fields': ('status', 'is_past'),
        }),
        (_('确认 | Confirmation'), {
            'fields': ('confirmed_at', 'confirmed_by', 'arrival_time'),
            'classes': ('collapse',),
        }),
        (_('取消 | Cancellation'), {
            'fields': ('cancelled_at', 'cancellation_reason', 'cancellation_notes'),
            'classes': ('collapse',),
        }),
        (_('提醒 | Reminders'), {
            'fields': ('reminder_sent', 'reminder_sent_at'),
            'classes': ('collapse',),
        }),
        (_('关联记录 | Linked Records'), {
            'fields': ('diagnosis_session',),
            'classes': ('collapse',),
        }),
        (_('备注 | Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        (_('系统信息 | System Information'), {
            'fields': ('is_active', 'created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set created_by on creation."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
