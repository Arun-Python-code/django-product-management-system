from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_price = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)