from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# View to list all products on the main page
def product_list(request):
   # Get the sorting option from the query parameters (default is "name")
    sort_by = request.GET.get('sort', 'name')
    
    # Return the list of products to be rendered in the template
    return render(request, 'products/product_list.html', {'products': products})

# View to display product details
def product_detail(request, product_id):
    # Fetch the product based on its ID, or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Render the product detail template and pass the product object
    return render(request, 'products/product_detail.html', {'product': product})

# View to list products in a specific category
def category_products(request, category_slug):
    # Get the category based on the slug
    category = get_object_or_404(Category, slug=category_slug)
    
    # Get all products that belong to this category
    products = category.product_set.all()

    
    return render(request, 'products/category_products.html', {'category': category, 'products': products})