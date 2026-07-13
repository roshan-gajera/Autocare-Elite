from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('forget/password/', views.forgetPassword, name='forget-password'),
    
    path('logout/', views.logout_view, name='logout'),
]
