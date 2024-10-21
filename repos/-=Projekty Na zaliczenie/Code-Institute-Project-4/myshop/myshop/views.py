from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # For displaying messages to the user

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can log in now.')
            return redirect('login')  # Redirect to login after registration
        else:
            messages.error(request, 'Please correct the error below.')  # Error feedback
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
