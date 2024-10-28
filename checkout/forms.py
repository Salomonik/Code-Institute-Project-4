from django import forms
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField

class CheckoutForm(forms.Form):
   
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control'
    }))
    
   
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control'
    }))
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control'
    }))
    
   
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Street Address',
        'class': 'form-control'
    }))
    
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class': 'form-control'
    }))
    
    
    county = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'County',
        'class': 'form-control'
    }))
    
    postcode = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Postcode',
        'class': 'form-control'
    }))
    
    
    country = CountryField(blank_label='(select country)').formfield(widget=forms.Select(attrs={
        'class': 'form-control'
    }))
