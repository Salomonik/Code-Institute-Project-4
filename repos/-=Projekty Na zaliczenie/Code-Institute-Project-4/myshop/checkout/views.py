from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem
from .forms import CheckoutForm
import stripe
from django.http import JsonResponse
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if not cart_items.exists():
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    if request.method == 'POST':
        try:
            form = CheckoutForm(request.POST)
            if not form.is_valid():
                return JsonResponse({
                    'error': 'Invalid form data',
                    'errors': form.errors
                }, status=400)

            with transaction.atomic():
                order = Order.objects.create(user=request.user, total=total)

                for cart_item in cart_items:
                    product = cart_item.product
                    if product.stock < cart_item.quantity:
                        return JsonResponse({
                            'error': f'Not enough stock for {product.name}.'
                        }, status=400)

                    product.stock -= cart_item.quantity
                    product.save()

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=cart_item.quantity
                    )

                cart_items.delete()

                session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'gbp',
            'product_data': {
                'name': 'Your Shop Order',
                'description': f'Order #{order.id}',  # Dodaj numer zamówienia
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
    customer_email=request.user.email  # Dodaj email klienta
)

                return JsonResponse({'id': session.id})

        except stripe.error.StripeError as e:
            return JsonResponse({
                'error': 'Payment processing error. Please try again later.'
            }, status=500)

        except Exception as e:
            import traceback
            print(traceback.format_exc())  # Dodaj to do debugowania
            return JsonResponse({
                'error': 'An error occurred. Please try again.'
            }, status=500)

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



