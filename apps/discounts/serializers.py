from rest_framework import serializers
from .models import Discount, OrderTieredDiscount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'name', 'discount_type', 'value', 'priority', 'is_active']


class OrderTieredDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTieredDiscount
        fields = ['id', 'min_total', 'max_total', 'discount_percent']
