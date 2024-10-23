from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('get-items/', views.get_cart_items, name='get_cart_items'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  
]