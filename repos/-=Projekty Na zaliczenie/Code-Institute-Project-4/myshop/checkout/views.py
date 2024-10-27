from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem
from .forms import CheckoutForm
import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem
from .forms import CheckoutForm
import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from cart.models import CartItem
from .forms import CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt  # For testing purposes, remove in production if CSRF protection is required
def checkout(request):
    if not request.user.is_authenticated:
        # Przekaż zmienną do szablonu, aby wyświetlić panel logowania
        return render(request, 'checkout/checkout.html', {
            'show_login_prompt': True
        })
    print("Request method:", request.method)  # Debugging method type

    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if not cart_items.exists():
        print("Error: Cart is empty")
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    if request.method == 'POST':
        print("Processing POST request")  # Debugging POST method
        try:
            # Load JSON data from request
            data = json.loads(request.body)
            print("Received JSON data:", data)  # Debugging JSON data
            
            # Extract 'order_data' from JSON and pass it to the form
            form_data = data.get('order_data', {})
            form = CheckoutForm(form_data)

            if not form.is_valid():
                print("Invalid form data:", form.errors)  # Debugging form errors
                return JsonResponse({
                    'error': 'Invalid form data',
                    'errors': form.errors
                }, status=400)

            # Proceed with transaction creation, order items, and Stripe session
            with transaction.atomic():
                order = Order.objects.create(user=request.user, total=total)
                print("Order created:", order.id)  # Debugging order creation

                # Process each item in the cart
                for cart_item in cart_items:
                    product = cart_item.product
                    if product.stock < cart_item.quantity:
                        print(f"Not enough stock for {product.name}")  # Debugging stock issue
                        return JsonResponse({
                            'error': f'Not enough stock for {product.name}.'
                        }, status=400)

                    product.stock -= cart_item.quantity
                    product.save()
                    print(f"Stock updated for {product.name}: {product.stock}")  # Debugging stock update

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=cart_item.quantity
                    )
                    print(f"OrderItem created for {product.name}")  # Debugging order item creation

                cart_items.delete()
                print("Cart items deleted")  # Debugging cart clear

                # Create Stripe checkout session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': 'Your Shop Order',
                                'description': f'Order #{order.id}',
                                'metadata': {
                                    'order_id': order.id
                                }
                            },
                            'unit_amount': int(total * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/checkout/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/checkout/cancel/'),
                    metadata={
                        'order_id': order.id,
                        'user_id': request.user.id
                    },
                    customer_email=request.user.email
                )
                print("Stripe session created:", session.id)  # Debugging Stripe session

                return JsonResponse({'id': session.id})

        except json.JSONDecodeError:
            print("Invalid JSON data received")  # Debugging JSON decode error
            return JsonResponse({
                'error': 'Invalid JSON data received.'
            }, status=400)

        except stripe.error.StripeError as e:
            print("Stripe error:", e)  # Debugging Stripe error
            return JsonResponse({
                'error': 'Payment processing error. Please try again later.'
            }, status=500)

        except Exception as e:
            import traceback
            print("Unexpected error:", traceback.format_exc())  # Detailed debugging for unexpected errors
            return JsonResponse({
                'error': 'An error occurred. Please try again.'
            }, status=500)

    print("Rendering checkout page")  # Debugging GET method

    form = CheckoutForm()
    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })



def checkout_success(request):
    return render(request, 'checkout/success.html')

def checkout_cancel(request):
    return render(request, 'checkout/cancel.html')
