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
    
    