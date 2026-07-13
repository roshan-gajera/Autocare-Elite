from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    #main page url
    
    path('home/', views.home, name='servicesite-home'),
    path('dashboard/', views.dashboard, name='servicesite-dashboard'),
    path('serviceorder/', views.serviceorder, name='servicesite-serviceorder'),

    # crud opration message
    path('message/', views.message, name='servicesite-message'),
    path('message/<int:message_id>/show', views.message_show, name='servicesite-message-show'),
    path('message/<int:message_id>/edit', views.message_edit, name='servicesite-message-edit'),

    # crud opration towing
    path('towingorder', views.towingorder, name='servicesite-towingorder'),
    path('towingorder/<towing_id>/show', views.towing_order_show, name='servicesite-towingorder-show'),
    path('towingorder/<towing_id>/edit', views.towing_order_edit, name='servicesite-towingorder-edit'),

    # crud opration profile
    path('profile/', views.profile, name='servicesite-profile'),
    path('profile/service/add', views.service_add, name='servicesite-service-add'),
    path('profile/<int:service_id>/edit', views.service_edit, name='servicesite-service-edit'),
    path('profile/<int:service_id>/delete', views.service_delete, name='servicesite-service-delete'),

    # crud opration service order details
    path('serviceorder/<int:order_id>/show', views.serviceorder_show, name='servicesite-serviceorder-show'),
    path('serviceorder/<int:order_id>/edit', views.serviceorder_edit, name='servicesite-serviceorder-edit'),


    #login and logout
    
    path('logout/', views.logout_view, name='servicesite-logout'),


]