from django.contrib import admin

# Register your models here.
from .models import Brand, Category, Vendor, Product, VendorProduct, ProductChangeLog, VendorProductPricingLog



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "address", "website_url", "created_at", "updated_at")
    search_fields = ("name", "phone", "email")
    # list_filter = ("is_active",)


class ProductVendorInline(admin.TabularInline):
    model = VendorProduct
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_code", "name", "brand", "category", "description", "selling_price", "is_active")
    list_filter = ("brand", "category", "is_active")
    search_fields = ("product_code", "name")

    inlines = [ProductVendorInline]


@admin.register(VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    list_display = ("product", "vendor", "vendor_sku", "capital_price")
    search_fields = ("product__name", "vendor__vendor_name", "vendor_sku")


@admin.register(ProductChangeLog)
class ProductChangeLogAdmin(admin.ModelAdmin):
    list_display = ("product", "changed_by", "change_date")
    list_filter = ("product__name", "change_date")
    search_fields = ("product__name", "field_name", "old_value", "new_value")
    
    
@admin.register(VendorProductPricingLog)
class VendorProductPricingLogAdmin(admin.ModelAdmin):
    list_display = ("vendor_product", "changed_by", "old_value", "new_value")
    list_filter = ("vendor_product", "changed_by")