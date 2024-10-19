from django.urls import path
from . import views

# Defining URL patterns for the products app
urlpatterns = [
    path('', views.product_list, name='product_list'),  # Default route for listing products
]
