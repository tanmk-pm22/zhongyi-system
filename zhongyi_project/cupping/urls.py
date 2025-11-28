"""URLs for Cupping module."""
from django.urls import path
from . import views

app_name = 'cupping'

urlpatterns = [
    path('', views.cupping_session_list, name='session_list'),
]
