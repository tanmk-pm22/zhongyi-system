"""Admin configuration for Tuina module."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import TuinaTechnique, TuinaSession, TuinaSessionTechnique


@admin.register(TuinaTechnique)
class TuinaTechniqueAdmin(admin.ModelAdmin):
    """Admin for Tuina Techniques."""

    list_display = ('name_cn', 'name_en', 'code', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name_cn', 'name_en', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('code', 'name_cn', 'name_en', 'category', 'description'),
        }),
        (_('技术细节 | Technical Details'), {
            'fields': ('method', 'key_points', 'functions', 'common_areas'),
        }),
        (_('适应症与禁忌 | Indications & Contraindications'), {
            'fields': ('indications', 'contraindications'),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class TuinaSessionTechniqueInline(admin.TabularInline):
    """Inline techniques used in session."""
    model = TuinaSessionTechnique
    extra = 1
    fields = ('technique', 'body_area', 'duration_minutes', 'intensity', 'repetitions', 'sequence')


@admin.register(TuinaSession)
class TuinaSessionAdmin(admin.ModelAdmin):
    """Admin for Tuina Sessions."""

    list_display = (
        'patient', 'session_date', 'practitioner',
        'primary_focus', 'duration_minutes',
        'pain_level_before', 'pain_level_after'
    )
    list_filter = ('session_date', 'practitioner', 'is_active')
    search_fields = (
        'patient__first_name', 'patient__last_name',
        'patient__chinese_name', 'chief_complaint',
        'tcm_diagnosis', 'primary_focus'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-session_date',)
    date_hierarchy = 'session_date'

    fieldsets = (
        (_('患者信息 | Patient Information'), {
            'fields': ('patient', 'practitioner', 'session_date'),
        }),
        (_('诊断 | Diagnosis'), {
            'fields': ('chief_complaint', 'tcm_diagnosis', 'treatment_principle', 'primary_focus'),
        }),
        (_('治疗详情 | Treatment Details'), {
            'fields': ('duration_minutes', 'treatment_areas'),
        }),
        (_('治疗效果评估 | Treatment Assessment'), {
            'fields': (
                'pain_level_before', 'pain_level_after',
                'mobility_before', 'mobility_after',
                'patient_sensation', 'immediate_effect'
            ),
        }),
        (_('建议 | Recommendations'), {
            'fields': ('home_exercises', 'lifestyle_advice', 'next_session_date'),
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

    inlines = [TuinaSessionTechniqueInline]


@admin.register(TuinaSessionTechnique)
class TuinaSessionTechniqueAdmin(admin.ModelAdmin):
    """Admin for Session Techniques."""

    list_display = (
        'session', 'technique', 'body_area',
        'duration_minutes', 'intensity', 'sequence'
    )
    list_filter = ('technique', 'body_area', 'intensity')
    search_fields = ('session__patient__first_name', 'session__patient__last_name', 'body_area')
    ordering = ('session', 'sequence')
