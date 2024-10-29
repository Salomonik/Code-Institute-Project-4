from django.core.mail import send_mail
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.conf import settings
from .models import Order, OrderItem
from cart.models import CartItem
from .forms import CheckoutForm
import stripe
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    print("Start of checkout view")  # Debug start point

    if not request.user.is_authenticated:
        print("User not authenticated")  # Debug
        return render(request, 'checkout/checkout.html', {'show_login_prompt': True})

    # Calculate subtotal for items in cart
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    print(f"Cart subtotal calculated: {total}")  # Debug

    if not cart_items.exists():
        print("Cart is empty")  # Debug
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    # Set default shipping cost
    shipping_cost = 0
    print("Initial shipping cost set to zero")  # Debug

    # Handle POST request for payment processing
    if request.method == 'POST':
        print("Received POST request for payment")  # Debug

        try:
            data = json.loads(request.body)
            form_data = data.get('order_data', {})
            print(f"Form data received: {form_data}")  # Debug

            # Determine shipping cost based on country
            country = form_data.get('country')
            if country == 'PL':
                shipping_cost = 5  # Shipping cost for Poland
            print(f"Shipping cost determined: {shipping_cost}")  # Debug

            # Calculate total with shipping
            total_with_shipping = total + shipping_cost
            print(f"Total with shipping: {total_with_shipping}")  # Debug

            # Ustawienie customer_email - debug jeśli brak emaila
            customer_email = form_data.get('email', '') if form_data.get('email') else request.user.email
            if not customer_email:
                print("Error: No email provided in form data or user profile.")  # Debug
                return JsonResponse({'error': 'Email is required for processing the payment.'}, status=400)

            with transaction.atomic():
                # Create the order
                order = Order.objects.create(user=request.user, total=total_with_shipping)
                print(f"Order created with ID: {order.id}")  # Debug

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity
                    )
                    print(f"OrderItem created for product {cart_item.product.name} with quantity {cart_item.quantity}")  # Debug

                cart_items.delete()
                print("Cart items deleted after creating order.")  # Debug

                print("Stripe Secret Key:", settings.STRIPE_SECRET_KEY)  # Debug for Stripe key check
                print("Stripe Publishable Key:", settings.STRIPE_PUBLISHABLE_KEY)  # Debug for Stripe publishable key check

                # Debug: check data sent to Stripe
                print("Stripe session data:", {
                    'payment_method_types': ['card'],
                    'line_items': [{
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': 'Your Shop Order',
                                'description': f'Order #{order.id}',
                            },
                            'unit_amount': int(total_with_shipping * 100),
                        },
                        'quantity': 1,
                    }],
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri('/checkout/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    'cancel_url': request.build_absolute_uri('/checkout/cancel/'),
                    'customer_email': customer_email
                })

                # Create the Stripe session with total including shipping
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': 'Your Shop Order',
                                'description': f'Order #{order.id}',
                            },
                            'unit_amount': int(total_with_shipping * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/checkout/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/checkout/cancel/'),
                    customer_email=customer_email
                )
                print(f"Stripe session created with ID: {session.id}")  # Debug

                # Prepare order details for email
                order_items = OrderItem.objects.filter(order=order)
                items_description = "\n".join([
                    f"{item.product.name} (Quantity: {item.quantity}) - £{item.product.price * item.quantity}"
                    for item in order_items
                ])
                print("Order items for email prepared.")  # Debug

                # Create email message with shipping details
                email_message = (
                    f"Thank you for your order!\n\n"
                    f"Your order number is #{order.id}.\n\n"
                    f"Order details:\n"
                    f"{items_description}\n\n"
                    f"Shipping Cost: £{shipping_cost:.2f}\n"
                    f"Total Amount (including shipping): £{total_with_shipping:.2f}\n\n"
                    f"We hope you enjoy your purchase!"
                )
                print("Email message prepared.")  # Debug

                # Send confirmation email with order details
                send_mail(
                    subject=f'Order Confirmation - Order #{order.id}',
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[customer_email],
                    fail_silently=False,
                )
                print("Confirmation email sent.")  # Debug

                return JsonResponse({'id': session.id})

        except json.JSONDecodeError as e:
            print("JSON decoding error:", str(e))  # Debug JSON error
            return JsonResponse({'error': 'Invalid JSON data provided.'}, status=400)
        except stripe.error.StripeError as e:
            print("Stripe error:", str(e))  # Debug Stripe error
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            print("Unexpected error:", str(e))  # Debug any other exception
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

    # Render checkout page for GET requests
    form = CheckoutForm()
    print("Rendering checkout page for GET request")  # Debug
    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'shipping_cost': shipping_cost,
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

def checkout_success(request):
    return render(request, 'checkout/success.html')

def checkout_cancel(request):
    return render(request, 'checkout/cancel.html')
