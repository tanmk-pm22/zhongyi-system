"""URLs for Constitution module."""
from django.urls import path
from . import views

app_name = 'constitution'

urlpatterns = [
    path('', views.constitution_list, name='assessment_list'),
    path('types/', views.constitution_list, name='list'),
    path('assessment/new/', views.assessment_create, name='assessment_create'),
    path('assessment/new/<int:patient_id>/', views.assessment_create, name='assessment_create_patient'),
]
