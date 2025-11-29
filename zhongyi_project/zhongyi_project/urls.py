"""
URL configuration for zhongyi_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

urlpatterns = [
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs that should be translated
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    # Public Website (公共网站)
    path('', include('website.urls')),

    # Online Booking (在线预约)
    path('booking/', include('booking.urls')),

    # Patient Portal (患者门户)
    path('portal/', include('portal.urls')),

    # Backend Management (后台管理)
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('diagnosis/', include('diagnosis.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('acupuncture/', include('acupuncture.urls')),

    # API
    path('api/', include('api.urls')),

    prefix_default_language=False,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
