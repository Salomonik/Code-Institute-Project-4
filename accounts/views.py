from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from checkout.models import Order, OrderItem

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find the user by email
            user = User.objects.get(email=email)
            # Authenticate the user using the username and password
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Logged in successfully!'})
            else:
                return JsonResponse({'success': False, 'errors': {'password': ['Invalid credentials.']}})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'errors': {'email': ['Email does not exist.']}})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/'})
            return redirect('/')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': '/'})
        return redirect('/')
    return JsonResponse({'error': 'GET method not allowed'}, status=405)

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Dla każdego zamówienia obliczamy całkowitą cenę dla elementów
    for order in orders:
        order.items_with_total = [
            {
                'item': item,
                'total_price': item.product.price * item.quantity
            }
            for item in order.items.all()  # użycie 'items' zamiast 'orderitem_set'
        ]

    return render(request, 'accounts/profile.html', {
        'orders': orders
    })
