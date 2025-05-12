import pytest
from apps.discounts.models import Discount, OrderTieredDiscount
from apps.discounts.services import PercentageDiscount, FixedDiscount, TieredDiscount

@pytest.mark.django_db
def test_percentage_discount():
    d = PercentageDiscount(10)
    assert d.apply(200) == 180

@pytest.mark.django_db
def test_fixed_discount():
    d = FixedDiscount(50)
    assert d.apply(200) == 150

    d = FixedDiscount(250)
    assert d.apply(200) == 0  # no negative

@pytest.mark.django_db
def test_tiered_discount_application():
    OrderTieredDiscount.objects.create(min_total=500, max_total=1000, discount_percent=5)
    OrderTieredDiscount.objects.create(min_total=1001, max_total=None, discount_percent=10)

    # Between 500–1000
    td = TieredDiscount(750)
    assert td.apply(750) == 712.5

    # Above 1000
    td = TieredDiscount(1500)
    assert td.apply(1500) == 1350

    # Below any tier
    td = TieredDiscount(200)
    assert td.apply(200) == 200
