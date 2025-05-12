from django.db import models
from apps.common.models import TimeStampedMixin

class Discount(TimeStampedMixin):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
        ('tiered', 'Tiered'),
    ]

    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.FloatField()
    priority = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

class OrderTieredDiscount(models.Model):
    min_total = models.FloatField()
    max_total = models.FloatField(null=True, blank=True)
    discount_percent = models.FloatField()

    class Meta:
        verbose_name = "Order Tiered Discount"
        verbose_name_plural = "Order Tiered Discounts"