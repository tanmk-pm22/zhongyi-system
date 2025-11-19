"""URL patterns for diagnosis app."""
from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    # List and detail
    path('', views.DiagnosisListView.as_view(), name='list'),
    path('<int:pk>/', views.DiagnosisDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.edit_diagnosis, name='edit'),
    path('<int:pk>/delete/', views.delete_diagnosis, name='delete'),

    # Select patient to start diagnosis
    path('select-patient/', views.select_patient, name='select_patient'),

    # Diagnosis wizard steps
    path('start/<int:patient_pk>/', views.start_diagnosis, name='start'),
    path('<int:pk>/step2/', views.diagnosis_step2, name='step2'),
    path('<int:pk>/step3/', views.diagnosis_step3, name='step3'),
    path('<int:pk>/step4/', views.diagnosis_step4, name='step4'),
    path('<int:pk>/step5/', views.diagnosis_step5, name='step5'),
    path('<int:pk>/analyze/', views.diagnosis_analyze, name='analyze'),

    # API
    path('api/analyze/', views.api_analyze_symptoms, name='api_analyze'),
]
