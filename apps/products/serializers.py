from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'base_price', 'product_type']


class ProductPriceQuerySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)