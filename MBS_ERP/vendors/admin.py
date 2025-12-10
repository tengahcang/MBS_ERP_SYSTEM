from django.contrib import admin
from .models import Vendor, VendorProductPricingLog, VendorProduct
# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "address", "website_url", "created_at", "updated_at")
    search_fields = ("name", "phone", "email")


@admin.register(VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    list_display = ("product", "vendor", "vendor_sku", "capital_price")
    search_fields = ("product__name", "vendor__name", "vendor_sku")

    def save_model(self, request, obj, form, change):
        if change:
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


@admin.register(VendorProductPricingLog)
class VendorProductPricingLogAdmin(admin.ModelAdmin):
    list_display = ("vendor_product", "changed_by", "old_value", "new_value")
    list_filter = ("vendor_product", "changed_by")