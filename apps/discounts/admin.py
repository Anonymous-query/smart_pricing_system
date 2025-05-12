from django.contrib import admin

from .models import Discount, OrderTieredDiscount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discount_type', 'value', 'priority')
    search_fields = ('name', 'discount_type')
    list_filter = ('discount_type', 'priority')


@admin.register(OrderTieredDiscount)
class OrderTieredDiscountAdmin(admin.ModelAdmin):
    list_display = ('min_total', 'max_total', 'discount_percent')
    search_fields = ('discount_percent',)