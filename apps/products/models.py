from django.db import models
from apps.common.models import TimeStampedMixin

class Product(TimeStampedMixin):
    PRODUCT_TYPE_CHOICES = [
        ('bulk', 'Bulk'),
        ('premium', 'Premium'),
        ('seasonal', 'Seasonal'),
    ]

    name = models.CharField(max_length=100)
    base_price = models.FloatField()
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)

    def get_price(self, quantity):
        from .services import ProductPricingFactory
        strategy = ProductPricingFactory.get_strategy(self.product_type)
        return strategy.get_price(self.base_price, quantity)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class BulkPricingTier(models.Model):
    min_qty = models.PositiveIntegerField()
    max_qty = models.PositiveIntegerField(null=True, blank=True)
    discount_percent = models.FloatField(help_text="e.g., 5 for 5%")

    def __str__(self):
        return f"{self.min_qty} - {self.max_qty or '∞'}: {self.discount_percent}%"
    
    class Meta:
        verbose_name = "Bulk Pricing Tier"
        verbose_name_plural = "Bulk Pricing Tiers"
    
class PremiumMarkup(models.Model):
    markup_percent = models.FloatField()  # e.g., 15 for 15%

    class Meta:
        verbose_name = "Premium Markup"
        verbose_name_plural = "Premium Markups"

class SeasonalDiscount(models.Model):
    season = models.CharField(max_length=50)
    discount_percent = models.FloatField()  # e.g., 20 for 20%
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.season

    class Meta:
        verbose_name = "Seasonal Discount"
        verbose_name_plural = "Seasonal Discounts"
