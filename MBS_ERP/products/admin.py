from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Category, Product, ProductChangeLog
from vendors.models import VendorProduct, VendorProductPricingLog
# Register your models here.

class ProductVendorInline(admin.TabularInline):
    model = VendorProduct
    extra = 1


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_preview", "created_at", "updated_at")

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;"/>', obj.logo.url)
        return "-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_code", "name", "brand", "product_img_display", "category", "selling_price_idr", "is_active")
    list_filter = ("brand", "category", "is_active")
    search_fields = ("product_code", "name")
    
    inlines = [ProductVendorInline]
    
    def selling_price_idr(self, obj):
        if obj.selling_price is None:
            return "-"
        return f"Rp {obj.selling_price:,.0f}".replace(",", ".")
    selling_price_idr.short_description = "Selling Price (IDR)"
    
    def product_img_display(self, obj):
        if obj.product_img:
            return format_html('<img src="{}" style="height:40px;"/>', obj.product_img.url)
        return "-"
    product_img_display.short_description = "Image"

    def save_model(self, request, obj, form, change):
        """Log perubahan selling_price."""
        if change:
            old_product = Product.objects.get(pk=obj.pk)
            old_price = old_product.selling_price
            new_price = form.cleaned_data.get("selling_price")

            if old_price != new_price:
                ProductChangeLog.objects.create(
                    product=obj,
                    changed_by=request.user,
                    old_value=str(old_price),
                    new_value=str(new_price)
                )
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Log perubahan capital_price pada inline VendorProduct."""
        for formset in formsets:
            if formset.model == VendorProduct:
                for inline_form in formset.forms:
                    if not inline_form.cleaned_data:
                        continue

                    obj = inline_form.instance
                    if obj.pk:
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


@admin.register(ProductChangeLog)
class ProductChangeLogAdmin(admin.ModelAdmin):
    list_display = ("product", "changed_by", "change_date")
    list_filter = ("product__name", "change_date")
    search_fields = ("product__name", "old_value", "new_value")