"""Apps configuration for Cupping module."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CuppingConfig(AppConfig):
    """Cupping app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cupping'
    verbose_name = _('拔罐治疗 | Cupping Therapy')
