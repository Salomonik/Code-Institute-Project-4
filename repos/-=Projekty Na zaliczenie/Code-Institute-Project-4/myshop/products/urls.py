from django.urls import path
from . import views

# Defining URL patterns for the products app
urlpatterns = [
    path('', views.product_list, name='product_list'),  # Default route for listing products
    path('<int:product_id>/', views.product_detail, name='product_detail'), # route for product details
    # URL to filter products by category
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
]
