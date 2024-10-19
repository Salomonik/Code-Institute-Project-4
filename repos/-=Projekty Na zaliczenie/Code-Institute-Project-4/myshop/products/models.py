from django.db import models

# Create your models here.

# Product model to store product details
class Product(models.Model):
    # The name of the product, maximum length is 255 characters
    name = models.CharField(max_length=255)
    
    # A brief description of the product
    description = models.TextField()
    
    # Price of the product, defined as a decimal with two decimal places
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
     # Stock represents how many items are available in the store
    stock = models.IntegerField()
    
    # An optional image for the product, images are stored in 'product_images/' directory
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    # Automatically sets the date when the product is added
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Automatically updates the date when the product is updated
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the product
    def __str__(self):
        return self.name
    
class Category(models.Model):
    # The name of the category (e.g., Electronics, Clothing, etc.)
    name = models.CharField(max_length=255)
    
    # A short description for the category (optional)
    description = models.TextField(blank=True, null=True)
    
    # This field will create a URL-friendly version of the category name
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name