from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Import model kamu
from .models import Brand, Category, Vendor, Product, VendorProduct, ProductChangeLog, VendorProductPricingLog

# ========================================================
# BAGIAN 1: DEFINISI CLASS (JANGAN ADA @admin.register DI SINI)
# ========================================================

class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "action_buttons")
    search_fields = ("name",)

    def action_buttons(self, obj):
        edit_url = reverse('admin:core_brand_change', args=[obj.id])
        delete_url = reverse('admin:core_brand_delete', args=[obj.id])
        return format_html(
            '''
            <a href="{}" class="btn btn-sm" style="background:#7f8c8d; color:white; padding:5px 10px; border-radius:4px; margin-right:5px;" title="Edit"><i class="fas fa-edit"></i></a>
            <a href="{}" class="btn btn-sm" style="background:#E74C3C; color:white; padding:5px 10px; border-radius:4px;" title="Delete"><i class="fas fa-trash"></i></a>
            ''',
            edit_url, delete_url
        )
    action_buttons.short_description = 'Aksi'
    action_buttons.allow_tags = True

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)

class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "address", "website_url", "created_at", "updated_at")
    search_fields = ("name", "phone", "email")

class ProductVendorInline(admin.TabularInline):
    model = VendorProduct
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_code", "name", "brand", "category", "selling_price", "is_active", "action_buttons")
    list_filter = ("brand", "category", "is_active")
    search_fields = ("product_code", "name")
    inlines = [ProductVendorInline]

    def action_buttons(self, obj):
        edit_url = reverse('admin:core_product_change', args=[obj.id])
        delete_url = reverse('admin:core_product_delete', args=[obj.id])
        return format_html(
            '''
            <a href="{}" class="btn btn-sm" style="background:#7f8c8d; color:white; padding:5px 10px; border-radius:4px; margin-right:5px;" title="Edit"><i class="fas fa-edit"></i></a>
            <a href="{}" class="btn btn-sm" style="background:#E74C3C;   color:white; padding:5px 10px; border-radius:4px;" title="Delete"><i class="fas fa-trash"></i></a>
            ''',
            edit_url, delete_url
        )
    action_buttons.short_description = 'Aksi'
    action_buttons.allow_tags = True

class VendorProductAdmin(admin.ModelAdmin):
    list_display = ("product", "vendor", "vendor_sku", "capital_price")
    search_fields = ("product__name", "vendor__vendor_name", "vendor_sku")

class ProductChangeLogAdmin(admin.ModelAdmin):
    list_display = ("product", "changed_by", "change_date")
    list_filter = ("product__name", "change_date")
    search_fields = ("product__name", "field_name", "old_value", "new_value")

class VendorProductPricingLogAdmin(admin.ModelAdmin):
    list_display = ("vendor_product", "changed_by", "old_value", "new_value")
    list_filter = ("vendor_product", "changed_by")


# ========================================================
# BAGIAN 2: PENDAFTARAN MANUAL (INI YANG MENCEGAH ERROR)
# ========================================================

# Daftar pasangan Model dan Class Admin
registrations = [
    (Brand, BrandAdmin),
    (Category, CategoryAdmin),
    (Vendor, VendorAdmin),
    (Product, ProductAdmin),
    (VendorProduct, VendorProductAdmin),
    (ProductChangeLog, ProductChangeLogAdmin),
    (VendorProductPricingLog, VendorProductPricingLogAdmin),
]

# Loop pendaftaran dengan pengecekan "Apakah sudah terdaftar?"
for model_class, admin_class in registrations:
    try:
        admin.site.register(model_class, admin_class)
    except admin.sites.AlreadyRegistered:
        pass # Kalau sudah terdaftar, diam saja (jangan error)