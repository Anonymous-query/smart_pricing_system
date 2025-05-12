from django.contrib import admin

from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discount_type', 'value', 'priority')
    search_fields = ('name', 'discount_type')
    list_filter = ('discount_type', 'priority')