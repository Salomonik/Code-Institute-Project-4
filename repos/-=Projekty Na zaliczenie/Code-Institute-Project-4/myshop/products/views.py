from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# View to list all products on the main page
def product_list(request):
    # Get the selected sorting option from the query parameters
    sort_by = request.GET.get('sort', 'name')

    # Get the selected category from the query parameters
    category_slug = request.GET.get('category')

    # Filter products by category if category_slug is present
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Apply sorting
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'date':
        products = products.order_by('id')
    else:
        products = products.order_by('name')

    categories = Category.objects.all()  # Get all categories for the filter menu
    return render(request, 'products/product_list.html', {'products': products, 'categories': categories})

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