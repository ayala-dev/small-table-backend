from django.contrib import admin
from .models import Package, PackageCategory


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vendor', 'price_per_person', 'is_active', 'created_at')
    list_filter = ('is_active', 'vendor')
    search_fields = ('name', 'vendor__business_name')


@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'package')
    list_filter = ('package',)