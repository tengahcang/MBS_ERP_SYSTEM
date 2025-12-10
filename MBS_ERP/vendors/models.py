from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    # is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class VendorProduct(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor_sku = models.CharField(max_length=100, blank=True, null=True)
    capital_price  = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # lead_time_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'vendor')

    def __str__(self):
        return f"{self.vendor.name} → {self.product.name}"
    
    
class VendorProductPricingLog(models.Model):
    vendor_product = models.ForeignKey(VendorProduct, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    old_value = models.DecimalField(max_digits=12, decimal_places=2)
    new_value = models.DecimalField(max_digits=12, decimal_places=2)

    change_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pricing Log: {self.vendor_product}"