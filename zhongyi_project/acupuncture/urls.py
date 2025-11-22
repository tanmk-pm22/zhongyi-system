from django.urls import path
from . import views

app_name = 'acupuncture'

urlpatterns = [
    # Acupuncture Sessions
    path('', views.AcupunctureSessionListView.as_view(), name='list'),
    path('create/', views.AcupunctureSessionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AcupunctureSessionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AcupunctureSessionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AcupunctureSessionDeleteView.as_view(), name='delete'),

    # Acupoint Library (穴位图库)
    path('library/', views.AcupointLibraryView.as_view(), name='library'),
    path('library/<str:code>/', views.AcupointDetailView.as_view(), name='acupoint_detail'),
]
