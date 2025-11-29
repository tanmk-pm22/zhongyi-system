from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # 患者中心 | Patient Dashboard
    path('', views.dashboard, name='dashboard'),

    # 我的档案 | My Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # 就诊记录 | Medical Records
    path('records/', views.records_list, name='records_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),

    # 处方记录 | Prescriptions
    path('prescriptions/', views.prescriptions_list, name='prescriptions_list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescriptions/<int:pk>/print/', views.prescription_print, name='prescription_print'),

    # 预约管理 | Appointments
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),

    # 健康档案 | Health Records
    path('health/', views.health_records, name='health_records'),
    path('health/acupuncture/', views.acupuncture_sessions, name='acupuncture_sessions'),
]
