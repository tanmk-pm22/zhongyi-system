from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AcupunctureSession, AcupointReference


@admin.register(AcupunctureSession)
class AcupunctureSessionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'session_date', 'treatment_type', 'ai_recommendation_used', 'assigned_practitioner', 'is_active', 'created_at')
    list_filter = ('is_active', 'treatment_type', 'patient_response', 'ai_recommendation_used', 'assigned_practitioner', 'session_date', 'created_at')
    search_fields = ('patient__name', 'chief_complaint', 'tcm_diagnosis', 'acupoints_used', 'ai_suggested_acupoints')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-session_date', '-created_at')
    date_hierarchy = 'session_date'

    fieldsets = (
        (_('患者信息 | Patient Information'), {
            'fields': ('patient', 'session_date', 'treatment_type')
        }),
        (_('诊断 | Diagnosis'), {
            'fields': ('chief_complaint', 'tcm_diagnosis')
        }),
        (_('AI建议 | AI Recommendations'), {
            'fields': (
                'ai_suggested_acupoints',
                'ai_confidence_score',
                'ai_recommendation_used',
                'ai_reasoning',
            ),
            'classes': ('collapse',)
        }),
        (_('治疗详情 | Treatment Details'), {
            'fields': (
                'acupoints_used',
                'needle_retention_time',
                'technique_notes',
                'used_moxibustion',
                'used_cupping',
                'used_tuina',
            )
        }),
        (_('治疗反应 | Treatment Response'), {
            'fields': ('patient_response', 'treatment_notes')
        }),
        (_('后续计划 | Follow-up Plan'), {
            'fields': ('next_session_date', 'treatment_plan')
        }),
        (_('费用 | Fee'), {
            'fields': ('session_fee',)
        }),
        (_('分配 | Assignment'), {
            'fields': ('assigned_practitioner', 'is_active')
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient', 'assigned_practitioner')


@admin.register(AcupointReference)
class AcupointReferenceAdmin(admin.ModelAdmin):
    list_display = ('code', 'chinese_name', 'pinyin_name', 'meridian', 'usage_count', 'effectiveness_rating', 'is_active')
    list_filter = ('meridian', 'is_active')
    search_fields = ('code', 'chinese_name', 'pinyin_name', 'english_name', 'indications')
    readonly_fields = ('usage_count', 'effectiveness_rating', 'created_at', 'updated_at')
    ordering = ('meridian', 'code')

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('code', 'chinese_name', 'pinyin_name', 'english_name', 'meridian')
        }),
        (_('定位 | Location'), {
            'fields': ('location_chinese', 'location_english')
        }),
        (_('图片与视频 | Images & Videos'), {
            'fields': ('image_2d', 'image_3d', 'video_url')
        }),
        (_('临床信息 | Clinical Information'), {
            'fields': ('indications', 'functions', 'techniques', 'precautions')
        }),
        (_('统计数据 | Statistics'), {
            'fields': ('usage_count', 'effectiveness_rating'),
            'classes': ('collapse',)
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
        (_('时间戳 | Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
