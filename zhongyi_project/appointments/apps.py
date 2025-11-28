"""Apps configuration for Appointments module."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppointmentsConfig(AppConfig):
    """Appointments app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    verbose_name = _('预约管理 | Appointment Management')
