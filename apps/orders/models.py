from django.db import models
from apps.common.models import TimeStampedMixin
from django.contrib.auth.models import User
from apps.discounts.models import Discount
from apps.products.models import Product

class Order(TimeStampedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    discounts = models.ManyToManyField(Discount, blank=True)

    def subtotal(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(TimeStampedMixin):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.get_price(self.quantity)