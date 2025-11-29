from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # 首页 | Homepage
    path('', views.home, name='home'),

    # 关于我们 | About Us
    path('about/', views.about, name='about'),

    # 服务项目 | Services
    path('services/', views.services_list, name='services_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    # 医师团队 | Practitioners
    path('practitioners/', views.practitioners_list, name='practitioners_list'),
    path('practitioners/<int:pk>/', views.practitioner_detail, name='practitioner_detail'),

    # 知识库 | Knowledge Base
    path('knowledge/', views.knowledge_home, name='knowledge_home'),

    # 穴位图谱 | Acupoint Atlas
    path('knowledge/acupoints/', views.acupoints_list, name='acupoints_list'),
    path('knowledge/acupoints/<str:code>/', views.acupoint_detail, name='acupoint_detail'),

    # 中药库 | Herb Library
    path('knowledge/herbs/', views.herbs_list, name='herbs_list'),
    path('knowledge/herbs/<int:pk>/', views.herb_detail, name='herb_detail'),

    # 经典方剂 | Classic Formulas
    path('knowledge/formulas/', views.formulas_list, name='formulas_list'),
    path('knowledge/formulas/<int:pk>/', views.formula_detail, name='formula_detail'),

    # 健康文章 | Articles
    path('knowledge/articles/', views.articles_list, name='articles_list'),
    path('knowledge/articles/<slug:slug>/', views.article_detail, name='article_detail'),

    # 联系我们 | Contact Us
    path('contact/', views.contact, name='contact'),
]
