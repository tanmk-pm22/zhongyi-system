"""Apps configuration for Tuina module."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TuinaConfig(AppConfig):
    """Tuina app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tuina'
    verbose_name = _('推拿治疗 | Tuina Therapy')
