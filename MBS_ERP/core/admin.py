from django.contrib import admin

# Register your models here.
from .models import Brand, Category, Vendor, Product, ProductVendor, ProductChangeLog



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("vendor_name", "phone", "email", "is_active")
    search_fields = ("vendor_name", "phone", "email")
    list_filter = ("is_active",)


class ProductVendorInline(admin.TabularInline):
    model = ProductVendor
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_code", "name", "brand", "category", "selling_price", "is_active")
    list_filter = ("brand", "category", "is_active", "product_type")
    search_fields = ("product_code", "name")

    inlines = [ProductVendorInline]


@admin.register(ProductVendor)
class ProductVendorAdmin(admin.ModelAdmin):
    list_display = ("product", "vendor", "vendor_sku", "vendor_price", "lead_time_days")
    search_fields = ("product__name", "vendor__vendor_name", "vendor_sku")


@admin.register(ProductChangeLog)
class ProductChangeLogAdmin(admin.ModelAdmin):
    list_display = ("product", "field_name", "changed_by", "changed_at")
    list_filter = ("field_name", "changed_at")
    search_fields = ("product__name", "field_name", "old_value", "new_value")