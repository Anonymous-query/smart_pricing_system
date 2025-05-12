from .models import OrderTieredDiscount
from django.db.models import Q

class Discount:
    def apply(self, price):
        return price

class PercentageDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent

    def apply(self, price):
        return price * (1 - self.percent / 100)

class FixedDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        return max(0, price - self.amount)
    
class TieredDiscount(Discount):
    def __init__(self, order_total):
        self.order_total = order_total

    def apply(self, price):
        tier = (
            OrderTieredDiscount.objects
            .filter(min_total__lte=self.order_total)
            .filter(Q(max_total__gte=self.order_total) | Q(max_total__isnull=True))
            .order_by('-min_total')
            .first()
        )
        if tier:
            return price * (1 - tier.discount_percent / 100)
        return price
