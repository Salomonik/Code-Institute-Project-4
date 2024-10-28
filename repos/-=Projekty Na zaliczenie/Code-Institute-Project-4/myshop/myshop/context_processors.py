from products.models import Category

def categories_context(request):
    categories = Category.objects.exclude(name="Uncategorized")
    return {
        'categories': categories
    }
