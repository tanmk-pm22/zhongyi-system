"""Admin configuration for User model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model with role support."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'ic_number', 'phone')
    ordering = ('-created_at',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Role & Profile'), {
            'fields': ('role', 'phone', 'ic_number', 'date_of_birth', 'address', 'profile_photo'),
        }),
        (_('Practitioner Info'), {
            'fields': ('license_number', 'specialization', 'clinic_name'),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Role & Profile'), {
            'fields': ('role', 'phone', 'ic_number'),
        }),
    )
