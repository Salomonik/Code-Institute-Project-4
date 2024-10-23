from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem
from products.models import Product
from .forms import CheckoutForm
import stripe
from django.http import JsonResponse
from django.conf import settings

# Set the Stripe secret key for server-side communication
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    # Fetch all items in the user's cart
    cart_items = CartItem.objects.filter(cart__user=request.user)
    # Calculate the total price of all items in the cart
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Check if the cart is empty
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(user=request.user, total=total)
                
                # Process cart items and update product stock
                for cart_item in cart_items:
                    product = cart_item.product
                    
                    # Check if there is enough stock for the product
                    if product.stock < cart_item.quantity:
                        messages.error(request, f"Not enough stock for {product.name}.")
                        return redirect('cart')

                    # Update the product stock after order
                    product.stock -= cart_item.quantity
                    product.save()

                    # Create the order item
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity
                    )

                # Clear the cart after order
                cart_items.delete()

                # ** Stripe Payment Integration **
                # Create a Stripe checkout session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',  # You can change the currency if needed
                            'product_data': {
                                'name': 'Your Shop Order',  # The name of the order
                            },
                            'unit_amount': int(total * 100),  # Stripe requires the amount in cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/checkout/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/checkout/cancel/'),
                )

                # Redirect the user to the Stripe checkout session
                return JsonResponse({'id': session.id})

    else:
        form = CheckoutForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,  # Pass the publishable key to the frontend
    })

# Success view after payment
def checkout_success(request):
    return render(request, 'checkout/success.html')

# Cancel view in case the payment is canceled
def checkout_cancel(request):
    return render(request, 'checkout/cancel.html')
