"""Apps configuration for Treatment Course module."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TreatmentCourseConfig(AppConfig):
    """Treatment Course app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treatment_course'
    verbose_name = _('疗程管理 | Treatment Course Management')
