from django import forms

class ContactForm(forms.Form):
    # Name field with Bootstrap styling
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    # Email field with Bootstrap styling
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    # Message field with Bootstrap styling
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message', 'rows': 4})
    )
