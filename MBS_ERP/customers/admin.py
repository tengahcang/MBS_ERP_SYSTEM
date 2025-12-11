from django.contrib import admin
from .models import Customer, CustomerContactPerson
# Register your models here.


class CustomerContactPersonInLine(admin.TabularInline):
    model = CustomerContactPerson
    extra = 1
    
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", 'customer_type', 'email', 'phone')
    search_fields = ("name",)
    inlines = [CustomerContactPersonInLine]