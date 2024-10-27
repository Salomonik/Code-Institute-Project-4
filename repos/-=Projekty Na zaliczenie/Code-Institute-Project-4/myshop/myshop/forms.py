from django import forms

class ContactForm(forms.Form):
    # Field for the user's name
    name = forms.CharField(max_length=100, label='Name')
    # Field for the user's email address
    email = forms.EmailField(label='Email')
    # Field for the user's message
    message = forms.CharField(widget=forms.Textarea, label='Message')
