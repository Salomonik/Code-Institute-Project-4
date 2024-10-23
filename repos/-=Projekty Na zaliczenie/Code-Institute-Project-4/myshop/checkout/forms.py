from django import forms
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Full Name',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control'
    }))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control'
    }))
    street_address1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Street Address 1',
        'class': 'form-control'
    }))
    street_address2 = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Street Address 2',
        'class': 'form-control'
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Town or City',
        'class': 'form-control'
    }))
    county = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'County',
        'class': 'form-control'
    }))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Postal Code',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=forms.Select(attrs={
        'class': 'form-control'
    }))
