from django.db import models
from django.utils.text import slugify
import random
from django.contrib.auth.models import User
from servicesite.models import adminProfile
from maintenance.models import selectShop

class ServiceOffering(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(adminProfile, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class e.g., 'fas fa-oil-can'")
    price_starts_at = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image_url = models.URLField(blank=True, help_text="Relatable image URL")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, default="Admin")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(adminProfile,on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class TowingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Looking for Driver'),
        ('processing', 'Driver On The Way'),
        ('completed', 'Towed Successfully'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(adminProfile,on_delete=models.CASCADE ,null=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    vehicle_details = models.CharField(max_length=200, help_text="Make, Model, and Color")
    pickup_address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def __str__(self):
        return f"Towing for {self.full_name} - {self.status}"

class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Service In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(ServiceOffering, related_name='bookings')

    shop = models.ForeignKey(adminProfile,on_delete=models.CASCADE ,null=True)

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField()
    vehicle_info = models.CharField(max_length=200)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Payment Fields
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Service / Offline'),
        ('online', 'Pay Now (Stripe / Online)'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    is_paid = models.BooleanField(default=False)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True)
    
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp
    
    def total_estimated_cost(self):
        return sum(service.price_starts_at for service in self.services.all())

    def __str__(self):
        count = self.services.count()
        return f"Booking for {self.customer_name} ({count} services)"
