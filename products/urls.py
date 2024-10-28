from django.urls import path
from . import views


app_name = 'products'
# Defining URL patterns for the products app
urlpatterns = [
    path('', views.product_list, name='product_list'),  # List of products
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),  # Detail page for a product
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),  # Products in category
]
