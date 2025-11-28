"""Admin configuration for Treatment Course module."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import TreatmentCourse, CourseSession


class CourseSessionInline(admin.TabularInline):
    """Inline course sessions."""
    model = CourseSession
    extra = 0
    fields = ('session_number', 'session_type', 'scheduled_date', 'status', 'effectiveness_rating')
    readonly_fields = ('session_number',)
    ordering = ('session_number',)


@admin.register(TreatmentCourse)
class TreatmentCourseAdmin(admin.ModelAdmin):
    """Admin for Treatment Courses."""

    list_display = (
        'course_number', 'patient', 'course_name', 'practitioner',
        'start_date', 'status', 'progress_percentage', 'completed_sessions_count'
    )
    list_filter = ('status', 'start_date', 'practitioner')
    search_fields = (
        'course_number', 'course_name',
        'patient__first_name', 'patient__last_name', 'patient__chinese_name',
        'primary_diagnosis'
    )
    readonly_fields = (
        'course_number', 'created_at', 'updated_at',
        'completed_sessions_count', 'progress_percentage', 'remaining_sessions'
    )
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('course_number', 'patient', 'practitioner', 'course_name'),
        }),
        (_('诊断与计划 | Diagnosis & Plan'), {
            'fields': ('primary_diagnosis', 'treatment_goal', 'treatment_plan'),
        }),
        (_('疗程安排 | Course Schedule'), {
            'fields': (
                'start_date', 'planned_end_date', 'actual_end_date',
                'planned_sessions_total', 'planned_frequency'
            ),
        }),
        (_('治疗方式 | Treatment Modalities'), {
            'fields': (
                'includes_herbal_medicine', 'includes_acupuncture',
                'includes_cupping', 'includes_tuina', 'other_treatments'
            ),
        }),
        (_('进展与评估 | Progress & Assessment'), {
            'fields': (
                'status', 'completed_sessions_count', 'progress_percentage',
                'remaining_sessions', 'progress_notes', 'outcome_assessment',
                'patient_satisfaction'
            ),
        }),
        (_('费用 | Cost'), {
            'fields': ('estimated_cost', 'actual_cost'),
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

    inlines = [CourseSessionInline]

    def progress_percentage(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage.short_description = _('进度 | Progress')

    def completed_sessions_count(self, obj):
        return f"{obj.completed_sessions_count}/{obj.planned_sessions_total}"
    completed_sessions_count.short_description = _('完成次数 | Completed')


@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    """Admin for Course Sessions."""

    list_display = (
        'course', 'session_number', 'session_type',
        'scheduled_date', 'actual_date', 'status', 'effectiveness_rating'
    )
    list_filter = ('session_type', 'status', 'scheduled_date', 'practitioner')
    search_fields = (
        'course__course_number', 'course__patient__first_name',
        'course__patient__last_name', 'chief_complaint'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('course', 'session_number')
    date_hierarchy = 'scheduled_date'

    fieldsets = (
        (_('疗程信息 | Course Information'), {
            'fields': ('course', 'session_number', 'session_type'),
        }),
        (_('时间安排 | Schedule'), {
            'fields': ('scheduled_date', 'actual_date', 'practitioner'),
        }),
        (_('关联治疗记录 | Linked Treatment Records'), {
            'fields': (
                'prescription', 'acupuncture_session',
                'cupping_session', 'tuina_session'
            ),
        }),
        (_('治疗记录 | Session Record'), {
            'fields': ('chief_complaint', 'session_notes', 'patient_response'),
        }),
        (_('评估 | Assessment'), {
            'fields': ('effectiveness_rating', 'session_cost'),
        }),
        (_('状态 | Status'), {
            'fields': ('status',),
        }),
        (_('备注 | Notes'), {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
