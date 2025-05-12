from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'discounts', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()