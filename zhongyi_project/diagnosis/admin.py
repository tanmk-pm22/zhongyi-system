"""Admin configuration for Diagnosis models."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Symptom, Syndrome, SyndromeSysmptomWeight, DiagnosisSession


class SyndromeSysmptomWeightInline(admin.TabularInline):
    model = SyndromeSysmptomWeight
    extra = 1
    autocomplete_fields = ['symptom']


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_en', 'name_cn', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('code', 'name_en', 'name_cn')
    ordering = ('category', 'name_en')


@admin.register(Syndrome)
class SyndromeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_en', 'name_cn', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('code', 'name_en', 'name_cn')
    ordering = ('category', 'name_en')
    inlines = [SyndromeSysmptomWeightInline]

    fieldsets = (
        (None, {
            'fields': ('code', 'name_en', 'name_cn', 'category', 'is_active')
        }),
        (_('Description'), {
            'fields': ('description', 'etiology', 'clinical_manifestations')
        }),
        (_('Diagnostic Signs'), {
            'fields': ('tongue_signs', 'pulse_signs')
        }),
        (_('Treatment'), {
            'fields': ('treatment_principle',)
        }),
    )


@admin.register(DiagnosisSession)
class DiagnosisSessionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'practitioner', 'session_date', 'is_complete')
    list_filter = ('is_complete', 'session_date', 'practitioner')
    search_fields = ('patient__first_name', 'patient__last_name', 'chief_complaint')
    date_hierarchy = 'session_date'
    readonly_fields = ('created_at', 'updated_at', 'ai_suggested_syndromes')

    fieldsets = (
        (_('Session Info'), {
            'fields': ('patient', 'practitioner', 'medical_record', 'chief_complaint')
        }),
        (_('Inspection (望诊)'), {
            'fields': (
                'spirit_status', 'complexion',
                'tongue_body_color', 'tongue_body_shape',
                'tongue_coating_color', 'tongue_coating_texture', 'tongue_notes'
            )
        }),
        (_('Auscultation (闻诊)'), {
            'fields': ('voice_quality', 'breath_odor', 'auscultation_notes')
        }),
        (_('Inquiry (问诊)'), {
            'fields': (
                'selected_symptoms', 'symptom_details',
                'sleep_quality', 'appetite', 'thirst',
                'defecation', 'urination', 'perspiration', 'inquiry_notes'
            )
        }),
        (_('Palpation (切诊)'), {
            'fields': (
                'pulse_left_cun', 'pulse_left_guan', 'pulse_left_chi',
                'pulse_right_cun', 'pulse_right_guan', 'pulse_right_chi',
                'pulse_overall', 'palpation_notes'
            )
        }),
        (_('Analysis & Diagnosis'), {
            'fields': (
                'ai_suggested_syndromes', 'final_diagnosis',
                'treatment_principle', 'notes', 'is_complete'
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
