from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from decimal import Decimal
from django.http import JsonResponse
import json

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Pobieramy dane z JSON request
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity', 1)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        
        # Sprawdzenie dostępności w stocku
        if quantity > product.stock:
            return JsonResponse({'status': 'error', 'message': f'Only {product.stock} items available in stock'}, status=400)
        
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 0}
            )
            cart_item.quantity += quantity
            
            # Sprawdzanie, czy nie przekracza ilości dostępnej w stocku
            if cart_item.quantity > product.stock:
                return JsonResponse({'status': 'error', 'message': f'You can only add {product.stock} items to the cart'}, status=400)
            
            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            product_id_str = str(product_id)
            
            if product_id_str in cart:
                cart[product_id_str]['quantity'] += quantity
                # Sprawdzenie, czy nie przekracza dostępnego stocku
                if cart[product_id_str]['quantity'] > product.stock:
                    return JsonResponse({'status': 'error', 'message': f'Only {product.stock} items available'}, status=400)
            else:
                cart[product_id_str] = {
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': quantity,
                    'image_url': product.image.url if product.image else ''
                }
            request.session['cart'] = cart

        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def cart_detail(request):
    """Wyświetl zawartość koszyka"""
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.select_related('product').all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart = request.session.get('cart', {})
        cart_items = []
        total = 0
        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            quantity = item_data['quantity']
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'image_url': item_data['image_url']  # Ensure image_url is passed to the context
            })
            total += Decimal(item_data['price']) * quantity

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, product_id):
    """Usuń produkt z koszyka"""
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.filter(product_id=product_id).first()
        if cart_item:
            cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
    
    messages.success(request, "Produkt usunięty z koszyka")
    return redirect('cart:cart_detail')

def update_cart(request, product_id):
    """Update quantity in cart"""

    try:
        # Parse the JSON request body to get the quantity
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))  # Default to 1 if not found or invalid
        print(f"Received request to update product {product_id} with quantity {quantity}")
    except (ValueError, json.JSONDecodeError):
        print(f"Invalid quantity or request data for product {product_id}")
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity or request data'}, status=400)

    # Retrieve the product
    product = get_object_or_404(Product, id=product_id)

    # Check if the requested quantity exceeds available stock
    if quantity > product.stock:
        print(f"Requested quantity {quantity} exceeds available stock {product.stock} for product {product_id}")
        return JsonResponse({'status': 'error', 'message': f'Only {product.stock} items available in stock'}, status=400)

    # Ensure the quantity is valid
    if quantity <= 0:
        print(f"Removing product {product_id} because quantity is 0 or less.")
        return remove_from_cart(request, product_id)

    if request.user.is_authenticated:
        # For authenticated users, update cart item quantity
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.filter(product_id=product_id).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            print(f"Updated product {product_id} to quantity {cart_item.quantity} for user {request.user.username}")
        else:
            print(f"Product {product_id} not found in cart for user {request.user.username}")
    else:
        # For session-based cart (unauthenticated users)
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity  # Update the session cart
            request.session['cart'] = cart  # Save the updated session cart
            print(f"Updated product {product_id} in session to quantity {quantity}")
        else:
            print(f"Product {product_id} not found in session-based cart.")

    # Calculate the total quantity and price
    total_quantity = 0
    total_price = Decimal('0.00')

    if request.user.is_authenticated:
        cart_items = cart.cartitem_set.all()
    else:
        cart_items = request.session.get('cart', {}).values()

    # Log each item's quantity and total price for debugging
    for item in cart_items:
        if isinstance(item, CartItem):
            item_quantity = item.quantity
            item_total = item.product.price * item.quantity
        else:
            item_quantity = item['quantity']
            item_total = Decimal(item['price']) * item['quantity']

        total_quantity += item_quantity
        total_price += item_total

        # Log each item's details
        print(f"Product ID {product_id}, Quantity: {item_quantity}, Item Total: {item_total}")

    # Final log showing the cart's total quantity and price
    print(f"Final cart total quantity: {total_quantity}, total price: {total_price}")

    return JsonResponse({'status': 'success', 'message': 'Cart updated', 'total_quantity': total_quantity, 'total_price': str(total_price)})




def get_cart_items(request):
    """Pobierz aktualną zawartość koszyka w formacie JSON"""
    if request.user.is_authenticated:
        # For authenticated users
        cart = Cart.objects.get(user=request.user)
        items = []
        total = Decimal('0.00')

        for item in cart.cartitem_set.select_related('product').all():
            category_name = item.product.category.name if item.product.category else 'Unknown Category'
            items.append({
                'product_id': item.product.id,
                'name': item.product.name,
                'price': str(item.product.price),
                'quantity': item.quantity,
                'category': category_name,  # Include category name
                'image_url': item.product.image.url if item.product.image else '',  # Include image URL
                'total': str(item.product.price * item.quantity),
                'stock': item.product.stock  # Include the stock value
            })
            total += item.product.price * item.quantity
    else:
        # For session-based cart (unauthenticated users)
        cart = request.session.get('cart', {})
        items = []
        total = Decimal('0.00')

        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            category_name = product.category.name if product.category else 'Unknown Category'
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            item_total = price * quantity

            items.append({
                'product_id': product_id,
                'name': item_data['name'],
                'price': str(price),
                'quantity': quantity,
                'category': category_name,  # Include category name
                'image_url': product.image.url if product.image else '',  # Include image URL
                'total': str(item_total),
                'stock': product.stock  # Include the stock value
            })
            total += item_total

    return JsonResponse({
        'items': items,
        'total': str(total)
    })




    
 
def remove_from_cart(request, product_id):
    print(f"Received request to remove product {product_id}")
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_item = cart.cartitem_set.filter(product_id=product_id).first()
            if cart_item:
                cart_item.delete()
                print(f"Removed product {product_id} from cart.")
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart
                print(f"Removed product {product_id} from session-based cart.")

        # Zwracanie zaktualizowanej zawartości koszyka
        return get_cart_items(request)  
    
    
    