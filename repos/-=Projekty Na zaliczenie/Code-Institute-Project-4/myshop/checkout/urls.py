from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_page, name='checkout_page'),  # Main checkout page
]
