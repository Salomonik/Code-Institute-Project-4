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

# View to display cart
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user if request.user.is_authenticated else None)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

# View to remove an item from the cart
def remove_from_cart(request, product_id):
    user = request.user if request.user.is_authenticated else None
    cart_item = get_object_or_404(CartItem, product_id=product_id, user=user)
    cart_item.delete()
    return redirect('cart:cart_detail')