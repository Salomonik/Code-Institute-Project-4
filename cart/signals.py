from django.contrib.auth.signals import user_logged_in
from .models import Cart

def create_cart(sender, user, request, **kwargs):
    # Create a cart for the user if it doesn't exist
    Cart.objects.get_or_create(user=user)

# Connect the signal to the login process
user_logged_in.connect(create_cart)
