from django.contrib import admin
from .models import Customer, CustomerContactPerson
from projects.models import Project
# Register your models here.


class CustomerContactPersonInLine(admin.TabularInline):
    model = CustomerContactPerson
    extra = 1
    
class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    fields = ("name", "status", "start_date", "end_date")
    show_change_link = True
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", 'customer_type', 'business_entity_type', 'email', 'phone')
    search_fields = ("name",)
    list_filter = ("customer_type", "business_entity_type")
    inlines = [CustomerContactPersonInLine, ProjectInline]
    class Media:
        js = ("admin/js/customer.js",)