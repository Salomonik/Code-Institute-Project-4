from django.shortcuts import render

# Widok strony głównej
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')