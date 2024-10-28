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

stripe.api_key = settings.STRIPE_SECRET_KEY



def checkout(request):
    if not request.user.is_authenticated:
        return render(request, 'checkout/checkout.html', {
            'show_login_prompt': True
        })

    # Calculate subtotal for items in cart
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if not cart_items.exists():
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    # Set default shipping cost
    shipping_cost = 0

    # Handle POST request for payment processing
    if request.method == 'POST':
        data = json.loads(request.body)
        form_data = data.get('order_data', {})

        # Determine shipping cost based on country
        country = form_data.get('country')
        if country == 'PL':
            shipping_cost = 5  # Shipping cost for Poland

        # Calculate total with shipping
        total_with_shipping = total + shipping_cost

        with transaction.atomic():
            # Create the order
            order = Order.objects.create(user=request.user, total=total_with_shipping)
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            cart_items.delete()

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
                customer_email=request.user.email
            )

                # Prepare order details for email
            order_items = OrderItem.objects.filter(order=order)
            items_description = "\n".join([
                    f"{item.product.name} (Quantity: {item.quantity}) - £{item.product.price * item.quantity}"
                    for item in order_items
                ])
                
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

                # Send confirmation email with order details
            send_mail(
                    subject=f'Order Confirmation - Order #{order.id}',
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )


            return JsonResponse({'id': session.id})

    # Render checkout page for GET requests
    form = CheckoutForm()
    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'shipping_cost': shipping_cost,  # Pass shipping cost for initial display
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
    })





def checkout_success(request):
    return render(request, 'checkout/success.html')

def checkout_cancel(request):
    return render(request, 'checkout/cancel.html')
