from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type', 'base_price')
    search_fields = ('name', 'product_type')
    list_filter = ('product_type',)