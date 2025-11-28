"""URL patterns for accounts app."""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Patient portal
    path('patient-portal/', views.patient_portal_dashboard, name='patient_portal'),
    path('patient-portal/prescriptions/', views.patient_prescription_history, name='patient_prescriptions'),
    path('patient-portal/appointments/', views.patient_appointment_history, name='patient_appointments'),
]
