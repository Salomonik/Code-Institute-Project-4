from django.shortcuts import render, get_object_or_404
from .models import Product

# View to list all products on the main page
def product_list(request):
    # Query to get all products from the database
    products = Product.objects.all()
    
    # Return the list of products to be rendered in the template
    return render(request, 'products/product_list.html', {'products': products})

# View to display product details
def product_detail(request, product_id):
    # Fetch the product based on its ID, or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Render the product detail template and pass the product object
    return render(request, 'products/product_detail.html', {'product': product})