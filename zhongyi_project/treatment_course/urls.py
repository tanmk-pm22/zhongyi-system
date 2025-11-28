"""URLs for Treatment Course module."""
from django.urls import path
from . import views

app_name = 'treatment_course'

urlpatterns = [
    path('', views.course_list, name='course_list'),
]
