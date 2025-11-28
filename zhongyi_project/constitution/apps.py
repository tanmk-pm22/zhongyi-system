"""Apps configuration for Constitution module."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConstitutionConfig(AppConfig):
    """Constitution app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'constitution'
    verbose_name = _('体质辨识 | Constitution Analysis')
