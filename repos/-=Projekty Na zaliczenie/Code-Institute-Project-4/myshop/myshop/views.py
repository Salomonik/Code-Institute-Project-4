from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages  # For displaying messages to the user
from accounts.forms import UserRegisterForm
from django import forms
from django.contrib.auth.backends import ModelBackend
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from products.models import Product

# Home page view
def home(request):
    return render(request, 'home.html')

# About page view
def about(request):
    return render(request, 'about.html')

# Contact page view
def contact(request):
    return render(request, 'contact.html')

# Profile page view
def profile(request):
    return render(request, 'profile.html')

def contact_view(request):
    if request.method == 'POST':
        print("Form submission detected (POST request).")
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form is valid. Processing form data...")
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            
            subject = f"New Contact Form Submission from {name}"
            email_message = f"From: {name} <{email}>\n\nMessage:\n{message}"
            recipient_list = ['salomonik@gmail.com']

            # Send email
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            print("Email sent successfully.")

            # Render success page or redirect
            return render(request, 'contact_success.html')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        print("GET request detected. Initializing an empty form.")
        form = ContactForm()

    print("Rendering contact.html template with form.")
    return render(request, 'contact.html', {'form': form})

def search_products(request):
    query = request.GET.get('q')  # Get the query from the search bar
    products = []

    if query:
        # Filter products based on the query (adjust fields as needed)
        products = Product.objects.filter(name__icontains=query)  # Searching by product name

    return render(request, 'search_results.html', {'query': query, 'products': products})

