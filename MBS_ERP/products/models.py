from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    # PRODUCT_TYPES = (
    #     ('stock', 'Stock'),
    #     ('service', 'Service'),
    #     ('bundle', 'Bundle'),
    # )

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    product_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='stock')
    stock = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)

    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    # capital_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    vendors = models.ManyToManyField("vendors.Vendor", through="vendors.VendorProduct", related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_code} - {self.name}"
    
class ProductChangeLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="change_logs")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    change_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_code} ({self.change_date})"