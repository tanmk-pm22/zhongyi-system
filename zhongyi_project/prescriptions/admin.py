"""Admin configuration for Prescription System."""
from django.contrib import admin
from .models import (
    HerbCategory, Herb, ClassicFormula, FormulaHerb,
    Prescription, PrescriptionItem, PatentMedicine, PrescriptionPatentMedicine
)


@admin.register(HerbCategory)
class HerbCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_cn', 'name_en']
    search_fields = ['name_cn', 'name_en']


class FormulaHerbInline(admin.TabularInline):
    model = FormulaHerb
    extra = 1
    autocomplete_fields = ['herb']


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1
    autocomplete_fields = ['herb']


class PrescriptionPatentMedicineInline(admin.TabularInline):
    model = PrescriptionPatentMedicine
    extra = 1
    autocomplete_fields = ['medicine']


@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ['name_cn', 'name_en', 'name_pinyin', 'nature', 'category', 'dosage_range', 'is_active']
    list_filter = ['nature', 'category', 'is_active', 'is_toxic']
    search_fields = ['name_cn', 'name_en', 'name_pinyin', 'code']
    ordering = ['name_pinyin', 'name_cn']


@admin.register(ClassicFormula)
class ClassicFormulaAdmin(admin.ModelAdmin):
    list_display = ['name_cn', 'name_en', 'source', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name_cn', 'name_en', 'name_pinyin', 'code']
    inlines = [FormulaHerbInline]


@admin.register(PatentMedicine)
class PatentMedicineAdmin(admin.ModelAdmin):
    list_display = ['name_cn', 'name_en', 'dosage_form', 'manufacturer', 'prescription_type', 'price_per_box', 'is_active', 'is_in_stock']
    list_filter = ['dosage_form', 'prescription_type', 'is_active', 'is_in_stock']
    search_fields = ['name_cn', 'name_en', 'code', 'manufacturer', 'approval_number']
    ordering = ['name_cn']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息 | Basic Info', {
            'fields': ('code', 'name_cn', 'name_en', 'manufacturer', 'approval_number')
        }),
        ('剂型与分类 | Form & Classification', {
            'fields': ('dosage_form', 'prescription_type')
        }),
        ('成分与功效 | Composition & Functions', {
            'fields': ('ingredients', 'functions', 'tcm_pattern')
        }),
        ('用法用量 | Dosage & Administration', {
            'fields': ('specification', 'dosage_adult', 'dosage_child', 'administration_method')
        }),
        ('安全信息 | Safety Info', {
            'fields': ('contraindications', 'precautions', 'adverse_reactions', 'drug_interactions')
        }),
        ('价格与储存 | Pricing & Storage', {
            'fields': ('price_per_box', 'storage_conditions', 'shelf_life')
        }),
        ('状态 | Status', {
            'fields': ('is_active', 'is_in_stock', 'created_at', 'updated_at')
        }),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_number', 'patient', 'practitioner', 'prescription_date', 'doses', 'status']
    list_filter = ['status', 'prescription_date']
    search_fields = ['prescription_number', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'prescription_date'
    inlines = [PrescriptionItemInline, PrescriptionPatentMedicineInline]
    readonly_fields = ['prescription_number', 'prescription_date', 'created_at', 'updated_at']
