from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea, label="Shipping Address")
