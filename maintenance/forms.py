from django.contrib.auth.models import User
from django import forms
from .models import selectShop


class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input form-hint'}),
            'email': forms.EmailInput(attrs={'class': 'form-input form-hint'}),
        }

class selectShopForm(forms.ModelForm):
    class Meta:
        model = selectShop
        fields = ['select_shop']

        widgets = {
            'select_shop' : forms.Select(attrs={'class': 'shop-select', 'id':'shopSelect'})
        }


