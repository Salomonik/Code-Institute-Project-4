from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from products.models import Product  # Import only from products.models
from .models import Cart, CartItem  # Import Cart and CartItem from your cart models
from .forms import CartAddProductForm

# View to add an item to the cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Get or create a cart for the user

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1  # Increment quantity
    cart_item.save()

    # Calculate cart total price
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    # Return JSON response (for asynchronous requests)
    return JsonResponse({
        'cart_total': cart_items.count(),
        'cart_total_price': total_price,
        'item': {
            'name': product.name,
            'price': str(product.price),
            'quantity': cart_item.quantity,
        }
    })

# View to display cart
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)  # Get the user's cart
    cart_items = cart.cartitem_set.all()  # Get all items in the cart
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

# View to remove an item from the cart
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)  # Use cart and product_id to get the item
    cart_item.delete()
    return redirect('cart:cart_detail')
