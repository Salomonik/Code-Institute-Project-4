from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem
from .forms import CartAddProductForm

# View to add an item to the cart
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    # Return updated cart details
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    return JsonResponse({
        'cart_total': cart_items.count(),
        'cart_total_price': total_price,
        'item': {
            'name': product.name,
            'price': product.price,
            'quantity': cart_item.quantity,
        }
    })

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