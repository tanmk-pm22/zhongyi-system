"""URLs for Appointments module."""
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('calendar/', views.appointment_calendar, name='calendar'),
]
