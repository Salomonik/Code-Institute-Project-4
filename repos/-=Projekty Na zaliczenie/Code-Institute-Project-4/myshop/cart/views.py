from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from products.models import Product  # Import only from products.models
from .models import Cart, CartItem  # Import Cart and CartItem from your cart models
from .forms import CartAddProductForm

# View to add an item to the cart
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import CartItem, Cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Handle authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Handle anonymous user with session cart
        cart = request.session.get('cart', {})
        if not cart:
            cart = {}
        
        # If the product is already in the cart, increase the quantity
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            # If the product is not in the cart, add it
            cart[str(product_id)] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
            }
        
        # Save cart to session
        request.session['cart'] = cart

        # Return the updated cart subtotal and items
        total_price = sum(int(item['quantity']) * float(item['price']) for item in cart.values())
        return JsonResponse({
            'cart_total': len(cart),
            'cart_total_price': total_price,
            'items': list(cart.values()),
        })

    # If user is authenticated, continue with database logic (as per your original implementation)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    # Collect all items in the cart
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    items = []
    for item in cart_items:
        items.append({
            'name': item.product.name,
            'price': str(item.product.price),
            'quantity': item.quantity,
        })

    # Return a JSON response for both session-based and authenticated user carts
    return JsonResponse({
        'cart_total': cart_items.count(),
        'cart_total_price': total_price,
        'items': items,
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
