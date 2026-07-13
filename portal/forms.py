from django import forms
from .models import ServiceOffering, BlogPost, ContactMessage, TowingRequest, ServiceBooking

class ServiceOfferingForm(forms.ModelForm):
    class Meta:
        model = ServiceOffering
        fields = ['title', 'description', 'icon_class', 'price_starts_at', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'rows': 4}),
            'icon_class': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. fas fa-oil-can'}),
            'price_starts_at': forms.NumberInput(attrs={'class': 'input-field'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field'}),
            'content': forms.Textarea(attrs={'class': 'input-field', 'rows': 6}),
            'image_url': forms.URLInput(attrs={'class': 'input-field', 'placeholder': 'Unsplash image URL...'}),
        }

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message','is_read']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email Address'}),
            'subject': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'input-field', 'rows': 4, 'placeholder': 'Your Message'}),
        }

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)

        if not edit_mode:
            # hide fields in create mode
            for f in ['is_read']:
                self.fields.pop(f)

class TowingRequestForm(forms.ModelForm):
    class Meta:
        model = TowingRequest
        fields = ['full_name','phone_number','vehicle_details','pickup_address','latitude','longitude','status','otp_verified']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Phone Number'}),
            'vehicle_details': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Brand, Model & Color'}),
            'pickup_address': forms.TextInput(attrs={'class': 'input-field', 'id': 'address-input', 'placeholder': 'Click on map or enter address'}),
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }

    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)

        if not edit_mode:
            # hide fields in create mode
            for f in ['status', 'otp_verified']:
                self.fields.pop(f)

class ServiceBookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=ServiceOffering.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Services Required"
    )

    class Meta:
        model = ServiceBooking
        fields = ['services','customer_name','customer_phone','customer_email','vehicle_info','preferred_date','preferred_time','payment_method','additional_notes','status','is_paid','otp_verified']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Full Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Phone Number'}),
            'customer_email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email Address'}),
            'vehicle_info': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Make, Model, Year'}),
            'preferred_date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'class': 'input-field', 'type': 'time'}),
            'payment_method': forms.Select(attrs={'class': 'input-field'}),
            'additional_notes': forms.Textarea(attrs={'class': 'input-field', 'rows': 3, 'placeholder': 'Any specific concerns or requests...'}),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None) 
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)

        if shop:
            self.fields['services'].queryset = ServiceOffering.objects.filter(shop=shop, is_active=True)

        if not edit_mode:
            
            for f in ['status', 'is_paid', 'otp_verified']:
                self.fields.pop(f)
    
    

