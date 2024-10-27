from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

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
    # Check if the form was submitted via POST
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Validate the form data
        if form.is_valid():
            # Extract cleaned form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Prepare the email content
            subject = f'Message from {name}'
            email_message = f"From: {name} <{email}>\n\n{message}"
            
            # Send the email
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['your_email@example.com'],  # Replace with your email address
            )
            # Render a success page after email is sent
            return render(request, 'contact_success.html')
    else:
        # Render the form if no data was submitted
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})