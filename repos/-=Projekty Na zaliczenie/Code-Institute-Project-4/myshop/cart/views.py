from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem
from .forms import CartAddProductForm

# View to add an item to the cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        user = request.user if request.user.is_authenticated else None
        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=user, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart:cart_detail')