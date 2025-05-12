from django.contrib import admin
from .models import Product, BulkPricingTier, PremiumMarkup, SeasonalDiscount

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type', 'base_price')
    search_fields = ('name', 'product_type')
    list_filter = ('product_type',)

@admin.register(BulkPricingTier)
class BulkPricingTierAdmin(admin.ModelAdmin):
    list_display = ('min_qty', 'max_qty', 'discount_percent')

@admin.register(PremiumMarkup)
class PremiumMarkupAdmin(admin.ModelAdmin):
    list_display = ('markup_percent',)

@admin.register(SeasonalDiscount)
class SeasonalDiscountAdmin(admin.ModelAdmin):
    list_display = ('season', 'discount_percent', 'is_active')