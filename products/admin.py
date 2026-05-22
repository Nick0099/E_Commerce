from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller','category', 'price','stock',  'is_active')
    search_fields = ('name', 'seller__email')
    list_filter = ('category','is_active')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','description']
