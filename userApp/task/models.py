from django.db import models
from django.contrib.auth.models import User


# Store the product data managed by the application.
class product(models.Model):
    # Basic product details displayed and edited through the product pages.
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_price = models.PositiveIntegerField()

    # Link each product to its owner; deleting that user also deletes their products.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_products")
    # Record when the row is first created and most recently saved.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)