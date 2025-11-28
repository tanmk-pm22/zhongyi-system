"""Admin configuration for Cupping module."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CuppingTechnique, CuppingSession, CuppingSessionTechnique


@admin.register(CuppingTechnique)
class CuppingTechniqueAdmin(admin.ModelAdmin):
    """Admin for Cupping Techniques."""

    list_display = ('name_cn', 'name_en', 'code', 'typical_duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_cn', 'name_en', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('code', 'name_cn', 'name_en', 'description'),
        }),
        (_('技术细节 | Technical Details'), {
            'fields': ('method', 'typical_duration', 'indications', 'contraindications', 'precautions'),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class CuppingSessionTechniqueInline(admin.TabularInline):
    """Inline techniques used in session."""
    model = CuppingSessionTechnique
    extra = 1
    fields = ('technique', 'body_location', 'duration_minutes', 'number_of_cups', 'sequence')


@admin.register(CuppingSession)
class CuppingSessionAdmin(admin.ModelAdmin):
    """Admin for Cupping Sessions."""

    list_display = (
        'patient', 'session_date', 'practitioner',
        'duration_minutes', 'pain_level_before', 'pain_level_after'
    )
    list_filter = ('session_date', 'practitioner', 'is_active')
    search_fields = (
        'patient__first_name', 'patient__last_name',
        'patient__chinese_name', 'chief_complaint', 'tcm_diagnosis'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-session_date',)
    date_hierarchy = 'session_date'

    fieldsets = (
        (_('患者信息 | Patient Information'), {
            'fields': ('patient', 'practitioner', 'session_date'),
        }),
        (_('诊断 | Diagnosis'), {
            'fields': ('chief_complaint', 'tcm_diagnosis', 'treatment_principle'),
        }),
        (_('治疗详情 | Treatment Details'), {
            'fields': ('duration_minutes', 'treatment_locations'),
        }),
        (_('治疗反应 | Treatment Reactions'), {
            'fields': (
                'skin_reaction', 'cup_marks_description',
                'pain_level_before', 'pain_level_after',
                'patient_sensation', 'immediate_effect'
            ),
        }),
        (_('建议 | Recommendations'), {
            'fields': ('post_treatment_advice', 'next_session_date'),
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

    inlines = [CuppingSessionTechniqueInline]


@admin.register(CuppingSessionTechnique)
class CuppingSessionTechniqueAdmin(admin.ModelAdmin):
    """Admin for Session Techniques."""

    list_display = (
        'session', 'technique', 'body_location',
        'duration_minutes', 'number_of_cups', 'sequence'
    )
    list_filter = ('technique', 'body_location')
    search_fields = ('session__patient__first_name', 'session__patient__last_name', 'body_location')
    ordering = ('session', 'sequence')
