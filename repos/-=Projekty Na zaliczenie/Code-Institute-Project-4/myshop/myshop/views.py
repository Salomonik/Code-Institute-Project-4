from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

# Profile page view
def profile(request):
    return render(request, 'profile.html')
