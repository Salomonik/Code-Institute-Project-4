from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem
from products.models import Product  # Import produktu
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.product.price * item.quantity for item in cart)

    if not cart.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Użycie transakcji dla bezpieczeństwa
                # Stwórz zamówienie
                order = Order.objects.create(user=request.user, total=total)
                
                # Przetwarzanie elementów koszyka i aktualizacja stocku
                for cart_item in cart:
                    product = cart_item.product
                    
                    # Sprawdź, czy jest wystarczająco produktów w magazynie
                    if product.stock < cart_item.quantity:
                        messages.error(request, f"Not enough stock for {product.name}.")
                        return redirect('cart')  # Przekieruj do koszyka, jeśli brakuje produktu

                    # Zaktualizuj stan magazynowy
                    product.stock -= cart_item.quantity
                    product.save()  # Zapisz zaktualizowany stan magazynowy
                    
                    # Stwórz element zamówienia
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity
                    )

                
                cart.delete()

                return redirect('checkout:checkout_success')
    else:
        form = CheckoutForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart_items': cart,
        'total': total
    })
    
    
def checkout_success(request):
    return render(request, 'checkout/success.html')
