"""URL patterns for prescriptions app."""
from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    # Prescription management
    path('', views.PrescriptionListView.as_view(), name='list'),
    path('<int:pk>/', views.PrescriptionDetailView.as_view(), name='detail'),
    path('create/', views.select_patient_for_prescription, name='select_patient'),
    path('create/<int:patient_pk>/', views.create_prescription, name='create'),
    path('<int:pk>/edit/', views.edit_prescription, name='edit'),
    path('<int:pk>/delete/', views.delete_prescription, name='delete'),
    path('<int:pk>/print/', views.print_prescription, name='print'),

    # Herb database
    path('herbs/', views.HerbListView.as_view(), name='herb_list'),
    path('herbs/<int:pk>/', views.HerbDetailView.as_view(), name='herb_detail'),

    # Classic formulas
    path('formulas/', views.FormulaListView.as_view(), name='formula_list'),
    path('formulas/<int:pk>/', views.FormulaDetailView.as_view(), name='formula_detail'),

    # API for AJAX
    path('api/herbs/search/', views.api_herb_search, name='api_herb_search'),
]
