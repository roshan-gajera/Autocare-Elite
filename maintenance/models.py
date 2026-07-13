from django.db import models
from django.contrib.auth.models import User
from servicesite.models import adminProfile


class selectShop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    select_shop = models.ForeignKey(adminProfile, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f"{self.select_shop}"