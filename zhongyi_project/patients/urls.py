"""URL patterns for patients app."""
from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Patient CRUD
    path('', views.PatientListView.as_view(), name='list'),
    path('create/', views.PatientCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PatientUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PatientDeleteView.as_view(), name='delete'),
    path('<int:pk>/qrcode/', views.patient_qrcode, name='qrcode'),

    # Medical Records
    path('<int:patient_pk>/records/create/', views.MedicalRecordCreateView.as_view(), name='record_create'),
    path('records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='record_detail'),
    path('records/<int:pk>/edit/', views.MedicalRecordUpdateView.as_view(), name='record_update'),
]
