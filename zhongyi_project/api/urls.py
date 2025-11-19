"""URL patterns for API app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from diagnosis.api_views import (
    SymptomViewSet,
    SyndromeViewSet,
    DiagnosisSessionViewSet,
    AnalysisViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'records', views.MedicalRecordViewSet)
router.register(r'symptoms', SymptomViewSet)
router.register(r'syndromes', SyndromeViewSet)
router.register(r'diagnosis-sessions', DiagnosisSessionViewSet)
router.register(r'analysis', AnalysisViewSet, basename='analysis')

urlpatterns = [
    path('', include(router.urls)),
]
