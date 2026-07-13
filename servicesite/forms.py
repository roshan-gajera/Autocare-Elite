from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import adminProfile
from django import forms

class registerform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2','is_staff']


class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
    
class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = adminProfile
        fields = ['full_name','shop_name', 'phone_number','city', 'shop_address']
       
