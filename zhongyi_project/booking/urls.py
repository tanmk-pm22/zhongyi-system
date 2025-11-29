from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # 在线预约 | Online Booking
    path('', views.booking_home, name='booking_home'),
    path('step1/', views.booking_step1_service, name='booking_step1'),
    path('step2/', views.booking_step2_practitioner, name='booking_step2'),
    path('step3/', views.booking_step3_datetime, name='booking_step3'),
    path('step4/', views.booking_step4_info, name='booking_step4'),
    path('confirm/', views.booking_confirm, name='booking_confirm'),
    path('success/<str:appointment_number>/', views.booking_success, name='booking_success'),

    # AJAX API endpoints
    path('api/available-slots/', views.api_available_slots, name='api_available_slots'),
    path('api/check-availability/', views.api_check_availability, name='api_check_availability'),
]
