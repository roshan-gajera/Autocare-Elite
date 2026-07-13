from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class adminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    shop_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    shop_address = models.TextField(max_length=200, blank=True)
    

    def __str__(self):
        return f"{self.shop_name}"