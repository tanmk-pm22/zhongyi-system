"""URLs for Tuina module."""
from django.urls import path
from . import views

app_name = 'tuina'

urlpatterns = [
    path('', views.tuina_session_list, name='session_list'),
    path('new/', views.tuina_session_create, name='session_create'),
    path('new/<int:patient_id>/', views.tuina_session_create, name='session_create_patient'),
    path('<int:pk>/', views.tuina_session_detail, name='session_detail'),
    path('<int:pk>/edit/', views.tuina_session_edit, name='session_edit'),
    path('<int:pk>/delete/', views.tuina_session_delete, name='session_delete'),
]
