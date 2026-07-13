from django.contrib import admin
from .models import ServiceOffering, BlogPost, ContactMessage, TowingRequest, ServiceBooking

@admin.register(ServiceOffering)
class ServiceOfferingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_starts_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')

@admin.register(TowingRequest)
class TowingRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'status', 'otp_verified', 'requested_at')
    list_filter = ('status', 'otp_verified', 'requested_at')
    search_fields = ('full_name', 'phone_number', 'vehicle_details')
    readonly_fields = ('otp', 'requested_at')

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'get_services', 'preferred_date', 'status', 'otp_verified')
    list_filter = ('status', 'otp_verified', 'preferred_date')
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    readonly_fields = ('otp', 'created_at')

    def get_services(self, obj):
        return ", ".join([s.title for s in obj.services.all()])
    get_services.short_description = 'Services'
