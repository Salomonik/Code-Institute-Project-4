from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Order, OrderItem
from cart.models import CartItem  # Assuming cart items are stored in CartItem model
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    total=total
                )
                
                # Create order items from cart items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity
                    )

                # Clear the cart after the order is placed
                cart_items.delete()

                # Redirect to a success page or payment gateway
                return redirect('checkout_success') 
    else:
        form = CheckoutForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })
    
def checkout_success(request):
    return render(request, 'checkout/success.html')
