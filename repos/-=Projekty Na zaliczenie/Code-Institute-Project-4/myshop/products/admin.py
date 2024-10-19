from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product

# Registering the Product model in the Django admin interface
admin.site.register(Product)
