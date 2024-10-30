from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock
from .models import Order, OrderItem
from cart.models import CartItem
from .views import checkout
import json

class CheckoutViewTests(TestCase):

    def setUp(self):
        # Setup method runs before each test, creating a test client, user, and cart item
        
        # Initialize the test client
        self.client = Client()
        
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        
        # Log in the test user
        self.client.login(username="testuser", password="password")

        # Create a sample cart item linked to the user's cart
        self.cart_item = CartItem.objects.create(
            cart=self.user.cart, product_id=1, quantity=2
        )
    
    def tearDown(self):
        # Clean-up method to remove test data after each test to avoid interference between tests
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        CartItem.objects.all().delete()

    def test_checkout_requires_authentication(self):
        """
        Test to ensure that the checkout page requires user authentication.
        If the user is logged out, the checkout view should prompt a login.
        """
        
        # Log out the user
        self.client.logout()
        
        # Attempt to access the checkout page
        response = self.client.get(reverse('checkout'))
        
        # Check that the response status is 200 OK (page is accessible)
        self.assertEqual(response.status_code, 200)
        
        # Verify that the login prompt context variable is included
        self.assertIn('show_login_prompt', response.context)
        
        # Confirm the login prompt is set to True
        self.assertTrue(response.context['show_login_prompt'])

    def test_checkout_empty_cart(self):
        """
        Test to ensure that an empty cart results in an error response when attempting checkout.
        """
        
        # Empty the cart by deleting all cart items
        CartItem.objects.all().delete()

        # Attempt to post to checkout with an empty cart
        response = self.client.post(reverse('checkout'), json.dumps({}), content_type="application/json")
        
        # Check that the response status is 400 Bad Request
        self.assertEqual(response.status_code, 400)
        
        # Verify that the JSON response contains an error indicating the cart is empty
        self.assertJSONEqual(response.content, {'error': 'Your cart is empty.'})
