from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages  # For displaying messages to the user
from accounts.forms import UserRegisterForm  # Import the form from forms.py
from django import forms
from django.contrib.auth.backends import ModelBackend

# Home page view
def home(request):
    return render(request, 'home.html')

# About page view
def about(request):
    return render(request, 'about.html')

# Contact page view
def contact(request):
    return render(request, 'contact.html')

# Register page view

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Explicite określamy backend
            backend = ModelBackend()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'error': 'GET method not allowed'}, status=405)
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')