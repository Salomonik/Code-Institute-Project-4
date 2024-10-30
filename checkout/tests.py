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
        # Tworzymy przykładowego użytkownika oraz koszyk
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

        # Tworzymy przykładowe dane do testowania koszyka
        self.cart_item = CartItem.objects.create(
            cart=self.user.cart, product_id=1, quantity=2
        )
    
    def tearDown(self):
        # Czyszczenie danych po każdym teście
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        CartItem.objects.all().delete()


    def test_checkout_requires_authentication(self):
        # Wylogowujemy użytkownika
        self.client.logout()
        
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('show_login_prompt', response.context)
        self.assertTrue(response.context['show_login_prompt'])

    def test_checkout_empty_cart(self):
        # Usuwamy elementy z koszyka, aby był pusty
        CartItem.objects.all().delete()

        response = self.client.post(reverse('checkout'), json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Your cart is empty.'})
