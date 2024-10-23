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
                    'quantity': quantity
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
                'quantity': quantity
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
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 0))
        
        if quantity <= 0:
            return remove_from_cart(request, product_id)
        
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_item = cart.cartitem_set.filter(product_id=product_id).first()
            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] = quantity
                request.session['cart'] = cart

        # Zwracanie zaktualizowanej zawartości koszyka
        return get_cart_items(request)



def get_cart_items(request):
    """Pobierz aktualną zawartość koszyka w formacie JSON"""
    if request.user.is_authenticated:
        # Dla zalogowanego użytkownika
        cart = Cart.objects.get(user=request.user)
        items = []
        total = Decimal('0.00')
        
        for item in cart.cartitem_set.select_related('product').all():
            items.append({
                'product_id': item.product.id,
                'name': item.product.name,
                'price': str(item.product.price),
                'quantity': item.quantity,
                'total': str(item.product.price * item.quantity)
            })
            total += item.product.price * item.quantity
    else:
        # Dla niezalogowanego użytkownika (koszyk w sesji)
        cart = request.session.get('cart', {})
        items = []
        total = Decimal('0.00')
        
        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            item_total = price * quantity
            
            items.append({
                'product_id': product_id,
                'name': item_data['name'],
                'price': str(price),
                'quantity': quantity,
                'total': str(item_total)
            })
            total += item_total

    return JsonResponse({
        'items': items,
        'total': str(total)
    })
    
 
 def remove_from_cart(request, product_id):
    if request.method == 'POST':
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

        # Zwracanie zaktualizowanej zawartości koszyka
        return get_cart_items(request)  