from django.contrib import admin

from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'category', )
    list_filter = ('category', )
    search_fields = ('name', 'description', )

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_version', 'product',)
    list_filter = ('product',)