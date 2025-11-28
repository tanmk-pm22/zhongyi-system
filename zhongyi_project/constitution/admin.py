"""Admin configuration for Constitution module."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    ConstitutionType,
    ConstitutionQuestionnaire,
    ConstitutionAssessment,
    ConstitutionAssessmentAnswer
)


class ConstitutionQuestionnaireInline(admin.TabularInline):
    """Inline questionnaire items."""
    model = ConstitutionQuestionnaire
    extra = 1
    fields = ('question_number', 'question_text', 'is_active')
    ordering = ('question_number',)


@admin.register(ConstitutionType)
class ConstitutionTypeAdmin(admin.ModelAdmin):
    """Admin for Constitution Types."""

    list_display = (
        'name_cn', 'name_en', 'code', 'display_order', 'is_active'
    )
    list_filter = ('is_active',)
    search_fields = ('name_cn', 'name_en', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('display_order', 'name_cn')

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('code', 'name_cn', 'name_en', 'description', 'display_order'),
        }),
        (_('特征 | Characteristics'), {
            'fields': (
                'physical_features',
                'common_symptoms',
                'psychological_features',
                'disease_susceptibility',
                'environmental_adaptation',
            ),
        }),
        (_('健康建议 | Health Recommendations'), {
            'fields': (
                'dietary_recommendations',
                'lifestyle_recommendations',
                'exercise_recommendations',
                'herbal_recommendations',
            ),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    inlines = [ConstitutionQuestionnaireInline]


@admin.register(ConstitutionQuestionnaire)
class ConstitutionQuestionnaireAdmin(admin.ModelAdmin):
    """Admin for Constitution Questionnaire."""

    list_display = (
        'question_number', 'constitution_type', 'question_text_short', 'is_active'
    )
    list_filter = ('constitution_type', 'is_active')
    search_fields = ('question_text',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('constitution_type', 'question_number')

    fieldsets = (
        (_('问题信息 | Question Information'), {
            'fields': ('constitution_type', 'question_number', 'question_text'),
        }),
        (_('评分 | Scoring'), {
            'fields': ('scoring_guide',),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def question_text_short(self, obj):
        return obj.question_text[:60] + '...' if len(obj.question_text) > 60 else obj.question_text
    question_text_short.short_description = _('问题 | Question')


class ConstitutionAssessmentAnswerInline(admin.TabularInline):
    """Inline assessment answers."""
    model = ConstitutionAssessmentAnswer
    extra = 0
    fields = ('question', 'score')
    readonly_fields = ('question',)


@admin.register(ConstitutionAssessment)
class ConstitutionAssessmentAdmin(admin.ModelAdmin):
    """Admin for Constitution Assessments."""

    list_display = (
        'patient', 'primary_constitution', 'primary_score',
        'secondary_constitution', 'assessment_date', 'practitioner'
    )
    list_filter = ('primary_constitution', 'assessment_date', 'practitioner', 'is_active')
    search_fields = (
        'patient__first_name', 'patient__last_name',
        'patient__chinese_name', 'patient__ic_number'
    )
    readonly_fields = ('created_at', 'updated_at', 'assessment_date')
    ordering = ('-assessment_date',)
    date_hierarchy = 'assessment_date'

    fieldsets = (
        (_('患者信息 | Patient Information'), {
            'fields': ('patient', 'practitioner', 'assessment_date'),
        }),
        (_('评估结果 | Assessment Results'), {
            'fields': (
                'primary_constitution', 'primary_score',
                'secondary_constitution', 'secondary_score',
                'scores',
            ),
        }),
        (_('分析与建议 | Analysis & Recommendations'), {
            'fields': ('ai_analysis', 'practitioner_notes', 'health_recommendations'),
        }),
        (_('随访 | Follow-up'), {
            'fields': ('follow_up_date',),
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    inlines = [ConstitutionAssessmentAnswerInline]


@admin.register(ConstitutionAssessmentAnswer)
class ConstitutionAssessmentAnswerAdmin(admin.ModelAdmin):
    """Admin for Assessment Answers."""

    list_display = ('assessment', 'question', 'score', 'created_at')
    list_filter = ('score', 'question__constitution_type', 'created_at')
    search_fields = (
        'assessment__patient__first_name',
        'assessment__patient__last_name',
        'question__question_text'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
