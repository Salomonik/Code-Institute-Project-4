from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Widok strony głównej
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Przekierowanie do logowania po rejestracji
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})