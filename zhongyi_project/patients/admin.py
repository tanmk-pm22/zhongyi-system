"""Admin configuration for Patient models."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Patient, MedicalRecord, MedicalHistoryTimeline


class MedicalRecordInline(admin.TabularInline):
    """Inline medical records in patient admin."""
    model = MedicalRecord
    extra = 0
    fields = ('visit_date', 'record_type', 'chief_complaint', 'tcm_diagnosis')
    readonly_fields = ('created_at',)
    ordering = ('-visit_date',)


class MedicalHistoryTimelineInline(admin.TabularInline):
    """Inline timeline events in patient admin."""
    model = MedicalHistoryTimeline
    extra = 0
    fields = ('event_date', 'event_type', 'title', 'is_important')
    readonly_fields = ('created_at',)
    ordering = ('-event_date',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin for Patient model."""

    list_display = (
        'full_name', 'chinese_name', 'ic_number', 'phone',
        'gender', 'age', 'assigned_practitioner', 'is_active', 'updated_at'
    )
    list_filter = ('gender', 'blood_type', 'is_active', 'assigned_practitioner', 'created_at')
    search_fields = ('first_name', 'last_name', 'chinese_name', 'ic_number', 'phone', 'email')
    readonly_fields = ('patient_id', 'created_at', 'updated_at')
    ordering = ('-updated_at',)

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'patient_id', 'first_name', 'last_name', 'chinese_name',
                'ic_number', 'date_of_birth', 'gender', 'blood_type', 'photo'
            ),
        }),
        (_('Contact Information'), {
            'fields': (
                'phone', 'email', 'address',
                'emergency_contact_name', 'emergency_contact_phone'
            ),
        }),
        (_('Medical Information'), {
            'fields': (
                'allergies', 'chronic_conditions', 'current_medications',
                'medical_history', 'family_history', 'tcm_constitution'
            ),
        }),
        (_('System'), {
            'fields': (
                'assigned_practitioner', 'user_account',
                'consent_data_sharing', 'consent_date',
                'is_active', 'notes'
            ),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    inlines = [MedicalRecordInline, MedicalHistoryTimelineInline]

    def age(self, obj):
        return obj.age
    age.short_description = _('Age')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    """Admin for MedicalRecord model."""

    list_display = (
        'patient', 'visit_date', 'record_type',
        'practitioner', 'tcm_diagnosis', 'created_at'
    )
    list_filter = ('record_type', 'practitioner', 'visit_date', 'created_at')
    search_fields = (
        'patient__first_name', 'patient__last_name', 'patient__ic_number',
        'chief_complaint', 'tcm_diagnosis', 'western_diagnosis'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-visit_date',)
    date_hierarchy = 'visit_date'

    fieldsets = (
        (_('Visit Information'), {
            'fields': ('patient', 'practitioner', 'record_type', 'visit_date'),
        }),
        (_('Chief Complaint'), {
            'fields': ('chief_complaint',),
        }),
        (_('Four Examinations (四诊)'), {
            'fields': (
                'inspection_notes', 'tongue_diagnosis',
                'auscultation_notes', 'inquiry_notes',
                'pulse_diagnosis', 'palpation_notes'
            ),
        }),
        (_('Diagnosis'), {
            'fields': ('tcm_diagnosis', 'western_diagnosis'),
        }),
        (_('Treatment'), {
            'fields': (
                'treatment_principle', 'prescription',
                'acupuncture_points', 'other_treatments'
            ),
        }),
        (_('Recommendations'), {
            'fields': (
                'lifestyle_advice', 'dietary_advice',
                'follow_up_notes', 'next_appointment'
            ),
        }),
        (_('Attachments'), {
            'fields': ('attachments',),
            'classes': ('collapse',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(MedicalHistoryTimeline)
class MedicalHistoryTimelineAdmin(admin.ModelAdmin):
    """Admin for MedicalHistoryTimeline model."""

    list_display = (
        'patient', 'event_date', 'event_type', 'title',
        'is_important', 'practitioner', 'created_at'
    )
    list_filter = ('event_type', 'is_important', 'event_date', 'practitioner')
    search_fields = ('patient__first_name', 'patient__last_name', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-event_date',)
    date_hierarchy = 'event_date'

    fieldsets = (
        (_('事件信息 | Event Information'), {
            'fields': ('patient', 'event_type', 'event_date', 'title', 'is_important'),
        }),
        (_('详情 | Details'), {
            'fields': ('description', 'practitioner', 'medical_record'),
        }),
        (_('关联 | Related Objects'), {
            'fields': ('related_object_type', 'related_object_id'),
            'classes': ('collapse',),
        }),
        (_('附件和备注 | Attachments & Notes'), {
            'fields': ('attachments', 'notes'),
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
