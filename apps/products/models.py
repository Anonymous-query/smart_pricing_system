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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"