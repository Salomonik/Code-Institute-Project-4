from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem, Cart  # Assuming cart models are here
from .forms import CheckoutForm

@login_required
def checkout(request):
    # Get the cart for the logged-in user
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = cart.get_cart_total()

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')  # Redirect to cart page if empty

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(user=request.user, total=total)
                
                # Create order items from cart items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity
                    )

                # Clear the cart after placing the order
                cart_items.delete()

                return redirect('checkout:checkout_success')  # Redirect to success page
    else:
        form = CheckoutForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })
    
def checkout_success(request):
    return render(request, 'checkout/success.html')
