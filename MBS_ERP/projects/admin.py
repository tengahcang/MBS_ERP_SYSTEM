from django.contrib import admin
from .models import Project
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "status")
    search_fields = ("name", "customer__name")
    list_filter = ("status",)
    autocomplete_fields = ["customer"]

admin.site.register(Project, ProjectAdmin)