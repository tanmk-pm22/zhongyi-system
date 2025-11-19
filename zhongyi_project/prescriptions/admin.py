"""Admin configuration for Prescription System."""
from django.contrib import admin
from .models import (
    HerbCategory, Herb, ClassicFormula, FormulaHerb,
    Prescription, PrescriptionItem
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


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_number', 'patient', 'practitioner', 'prescription_date', 'doses', 'status']
    list_filter = ['status', 'prescription_date']
    search_fields = ['prescription_number', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'prescription_date'
    inlines = [PrescriptionItemInline]
    readonly_fields = ['prescription_number', 'prescription_date', 'created_at', 'updated_at']
