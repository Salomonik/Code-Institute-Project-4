from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# View to list all products on the main page
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request):
    sort_by = request.GET.get('sort', 'name')
    category_slug = request.GET.get('category')

    # Filter products by category if the slug is present
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Exclude "Uncategorised" category in menu categories
    categories = Category.objects.exclude(name="Uncategorized")

    # Apply sorting
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'date':
        products = products.order_by('id')
    else:
        products = products.order_by('name')

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
    
    # Get all products that belong to this category using related name (if defined)
    products = Product.objects.filter(category=category)

    # Render the products within the selected category
    return render(request, 'products/category_products.html', {'category': category, 'products': products})


from .models import Category

def category_list(request):
    categories = Category.objects.all()
    return {'categories': categories}
