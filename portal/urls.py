from django.urls import path
from . import views

urlpatterns = [
    # General Pages
    path('about/', views.about_us, name='about_us'),
    path('services-info/', views.service_list, name='portal_service_list'),
    path('blog/', views.blog_list, name='blog_list'),
    path('contact/', views.contact_us, name='contact_us'),
    
     
    # Blog CRUD (Admin)
    path('blog/add/', views.blog_add, name='blog_add'),
    path('blog/<int:blog_id>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    
    # Service Booking CRUD (Client)
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:booking_id>/delete/', views.booking_delete, name='booking_delete'),
    path('services/<int:service_id>/book/', views.book_service, name='book_service'),
    path('bookings/<int:booking_id>/verify/', views.verify_otp, name='verify_otp'),
    path('bookings/<int:booking_id>/pay/', views.pay_online, name='pay_online'),
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    
    # Towing Request CRUD (Client)
    path('towing/', views.towing_request, name='towing_request'),
    path('towing/<int:towing_id>/', views.towing_detail, name='towing_detail'),
    path('towing/<int:towing_id>/edit/', views.towing_edit, name='towing_edit'),
    path('towing/<int:towing_id>/delete/', views.towing_delete, name='towing_delete'),
    path('towing/<int:towing_id>/verify/', views.verify_towing_otp, name='verify_towing_otp'),
]
