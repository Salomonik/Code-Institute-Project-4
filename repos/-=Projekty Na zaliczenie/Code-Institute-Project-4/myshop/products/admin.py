from django.contrib import admin
from .models import Product, Category

# Register the Category model in the Django admin interface
admin.site.register(Category)

# Optionally, customize the admin for Product to include category selection
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')

admin.site.register(Product, ProductAdmin)
