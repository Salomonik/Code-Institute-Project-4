from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from products.models import Product
from .models import Cart, CartItem
from django.db.models import Sum
from decimal import Decimal
import json

class CartException(Exception):
    pass

def calculate_cart_totals(cart_items):
    """Calculate total price and item count for a collection of cart items."""
    try:
        total_price = sum(item.get_total_price() for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        return total_items, total_price
    except Exception as e:
        raise CartException(f"Error calculating cart totals: {str(e)}")

def validate_quantity(quantity, available_stock):
    """Validate if the requested quantity is valid and within stock limits."""
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValidationError("Quantity must be at least 1")
        if quantity > available_stock:
            raise ValidationError(f"Only {available_stock} items available in stock")
        return quantity
    except ValueError:
        raise ValidationError("Invalid quantity value")

@transaction.atomic
def add_to_cart(request, product_id):
    """Add a product to cart with error handling and stock validation."""
    try:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity against stock
        validate_quantity(quantity, product.stock)

        if request.user.is_authenticated:
            return _add_to_db_cart(request, product, quantity)
        else:
            return _add_to_session_cart(request, product, quantity)

    except ValidationError as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'An unexpected error occurred',
            'status': 'error'
        }, status=500)

def _add_to_db_cart(request, product, quantity):
    """Handle adding items to database cart for authenticated users."""
    with transaction.atomic():
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}
        )
        
        # Check if new quantity exceeds stock
        new_quantity = cart_item.quantity + quantity
        validate_quantity(new_quantity, product.stock)
        
        cart_item.quantity = new_quantity
        cart_item.save()

        # Refresh cart totals
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        total_items, total_price = calculate_cart_totals(cart_items)

        return JsonResponse({
            'status': 'success',
            'cart_total': total_items,
            'cart_total_price': f"{total_price:.2f}",
            'items': [{
                'name': item.product.name,
                'price': str(item.product.price),
                'quantity': item.quantity,
                'subtotal': str(item.get_total_price())
            } for item in cart_items]
        })

def _add_to_session_cart(request, product, quantity):
    """Handle adding items to session cart for anonymous users."""
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        new_quantity = cart[str(product_id)]['quantity'] + quantity
        validate_quantity(new_quantity, product.stock)
        cart[str(product_id)]['quantity'] = new_quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity,
            'subtotal': str(Decimal(product.price) * quantity)
        }
    
    request.session['cart'] = cart
    
    # Calculate totals
    total_price = sum(
        Decimal(item['price']) * item['quantity'] 
        for item in cart.values()
    )
    total_items = sum(item['quantity'] for item in cart.values())

    return JsonResponse({
        'status': 'success',
        'cart_total': total_items,
        'cart_total_price': f"{total_price:.2f}",
        'items': list(cart.values())
    })

def cart_detail(request):
    """Display cart details with error handling."""
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = (cart.cartitem_set
                        .select_related('product')
                        .all())
            total_items, total_price = calculate_cart_totals(cart_items)
        else:
            cart = request.session.get('cart', {})
            cart_items = [{
                'product': get_object_or_404(Product, id=int(k)),
                'quantity': v['quantity'],
                'price': v['price']
            } for k, v in cart.items()]
            total_price = sum(
                Decimal(item['price']) * item['quantity'] 
                for item in cart_items
            )
            total_items = sum(item['quantity'] for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_items': total_items,
            'empty': total_items == 0
        }
        
        return render(request, 'cart/cart_detail.html', context)
        
    except Exception as e:
        messages.error(request, "Error loading cart details")
        return redirect('products:product_list')

@transaction.atomic
def update_cart_item(request, product_id):
    """Update cart item quantity with validation."""
    try:
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, id=product_id)
        
        # Validate new quantity
        validate_quantity(quantity, product.stock)
        
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            
            if quantity == 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
                
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                if quantity == 0:
                    del cart[str(product_id)]
                else:
                    cart[str(product_id)]['quantity'] = quantity
                    cart[str(product_id)]['subtotal'] = str(
                        Decimal(cart[str(product_id)]['price']) * quantity
                    )
                request.session['cart'] = cart
        
        return JsonResponse({'status': 'success'})
        
    except ValidationError as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'An unexpected error occurred',
            'status': 'error'
        }, status=500)

def remove_from_cart(request, product_id):
    """Remove item from cart with error handling."""
    try:
        if request.user.is_authenticated:
            with transaction.atomic():
                cart = Cart.objects.get(user=request.user)
                cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
                cart_item.delete()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart
        
        messages.success(request, "Item removed from cart")
        return redirect('cart:cart_detail')
        
    except Exception as e:
        messages.error(request, "Error removing item from cart")
        return redirect('cart:cart_detail')