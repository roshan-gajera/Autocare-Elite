from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/serviceorder/', views.serviceorder, name='service-order'),
    path('dashboard/towingorder/', views.towingorder, name='towing-order'),
    path('profile/', views.profile, name='user_profile'),  
]
