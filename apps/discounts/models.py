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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"