from django.db.models import Q
from .models import BulkPricingTier, PremiumMarkup, SeasonalDiscount

class ProductPricing:
    def get_price(self, base_price, quantity):
        return base_price * quantity

class BulkProduct(ProductPricing):
    def get_price(self, base_price, quantity):
        total = base_price * quantity
        applicable_tier = (
            BulkPricingTier.objects
            .filter(min_qty__lte=quantity)
            .filter(Q(max_qty__gte=quantity) | Q(max_qty__isnull=True))
            .order_by('-min_qty')
            .first()
        )
        if applicable_tier:
            discount = (applicable_tier.discount_percent / 100) * total
            return total - discount
        return total

class PremiumProduct(ProductPricing):
    def get_price(self, base_price, quantity):
        try:
            markup = PremiumMarkup.objects.first().markup_percent
        except AttributeError:
            markup = 0  # fallback
        return base_price * (1 + markup / 100) * quantity
    
class SeasonalProduct(ProductPricing):
    def get_price(self, base_price, quantity):
        active = SeasonalDiscount.objects.filter(is_active=True).first()
        discount = active.discount_percent if active else 0
        return base_price * (1 - discount / 100) * quantity

class ProductPricingFactory:
    strategies = {
        'bulk': BulkProduct(),
        'premium': PremiumProduct(),
        'seasonal': SeasonalProduct(),
    }

    @classmethod
    def get_strategy(cls, product_type):
        return cls.strategies.get(product_type, ProductPricing())