from django.contrib import admin
from .models import Quotation, QuotationItem
# Register your models here.

class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1

class QuotationAdmin(admin.ModelAdmin):
    list_display = ("quote_number", "project", "status", "date")
    search_fields = ("quote_number", "project__name", "project__customer__name")
    inlines = [QuotationItemInline]

admin.site.register(Quotation, QuotationAdmin)