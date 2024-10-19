from django.shortcuts import render
from .models import Product

# View to list all products on the main page
def product_list(request):
    # Query to get all products from the database
    products = Product.objects.all()
    
    # Return the list of products to be rendered in the template
    return render(request, 'products/product_list.html', {'products': products})
