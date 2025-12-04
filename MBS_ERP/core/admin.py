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
    
    def save_model(self, request, obj, form, change):
        """
        Override penyimpanan product untuk mendeteksi perubahan selling_price
        dan menambah ke ProductChangeLog otomatis.
        """
        if change:  # hanya berjalan saat update, bukan create
            old_product = Product.objects.get(pk=obj.pk)
            old_price = old_product.selling_price
            new_price = form.cleaned_data.get("selling_price")
            if old_price != new_price:
                # Buat log otomatis
                ProductChangeLog.objects.create(
                    product=obj,
                    changed_by=request.user,
                    old_value=str(old_price),
                    new_value=str(new_price)
                )
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """
        Detect perubahan capital_price pada inline VendorProduct
        dan otomatis membuat log VendorProductPricingLog.
        """
        for formset in formsets:
            if formset.model == VendorProduct:
                # loop semua inline VendorProduct
                for inline_form in formset.forms:
                    if not inline_form.cleaned_data:
                        continue
                    obj = inline_form.instance
                    if obj.pk:  # hanya update
                        old = VendorProduct.objects.get(pk=obj.pk)
                        old_price = old.capital_price
                        new_price = inline_form.cleaned_data.get("capital_price")
                        if old_price != new_price:
                            VendorProductPricingLog.objects.create(
                                vendor_product=obj,
                                changed_by=request.user,
                                old_value=old_price,
                                new_value=new_price
                            )

        super().save_related(request, form, formsets, change)

@admin.register(VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    list_display = ("product", "vendor", "vendor_sku", "capital_price")
    search_fields = ("product__name", "vendor__name", "vendor_sku")
    def save_model(self, request, obj, form, change):
        if change:  # hanya update
            old_obj = VendorProduct.objects.get(pk=obj.pk)
            old_price = old_obj.capital_price
            new_price = form.cleaned_data.get("capital_price")
            if old_price != new_price:
                VendorProductPricingLog.objects.create(
                    vendor_product=obj,
                    changed_by=request.user,
                    old_value=old_price,
                    new_value=new_price
                )
        super().save_model(request, obj, form, change)


@admin.register(ProductChangeLog)
class ProductChangeLogAdmin(admin.ModelAdmin):
    list_display = ("product", "changed_by", "change_date")
    list_filter = ("product__name", "change_date")
    search_fields = ("product__name", "field_name", "old_value", "new_value")
    
    
@admin.register(VendorProductPricingLog)
class VendorProductPricingLogAdmin(admin.ModelAdmin):
    list_display = ("vendor_product", "changed_by", "old_value", "new_value")
    list_filter = ("vendor_product", "changed_by")