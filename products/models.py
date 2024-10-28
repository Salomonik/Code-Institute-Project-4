from django.db import models

# Category model - stores product categories
class Category(models.Model):
    # Name of the category, e.g., "Electronics", "Clothing"
    name = models.CharField(max_length=255)
    
    # Optional description for the category
    description = models.TextField(blank=True, null=True)
    
    # Slug for URL-friendly representation of the category, e.g., "electronics"
    slug = models.SlugField(unique=True)

    # String representation of the object, returns the category name
    def __str__(self):
        return self.name

# Helper function to get or create a default category
def get_default_category():
    # Create a default category "Uncategorized" if it doesn't exist
    default_category, created = Category.objects.get_or_create(name="Uncategorized", slug="uncategorized")
    
    # Return the ID of the default category, used as the default for products without a category
    return default_category.id

# Product model - stores product information
class Product(models.Model):
    # Name of the product, e.g., "Laptop", "Shirt"
    name = models.CharField(max_length=255)
    
    # Description of the product, shown on the product detail page
    description = models.TextField()
    
    # Price of the product, with up to 10 digits and 2 decimal places
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Quantity of the product available in stock
    stock = models.IntegerField()
    
    # Optional field to store an image of the product, e.g., product photo
    # Images are stored in the 'product_images/' folder inside 'media'
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    # Foreign key linking the product to a category (many-to-one relationship)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=get_default_category)

    # String representation of the object, returns the product name
    def __str__(self):
        return self.name
