import pytest
from django.contrib.auth.models import User
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.discounts.models import Discount, OrderTieredDiscount
from apps.orders.services import OrderService

@pytest.mark.django_db
def test_order_subtotal():
    user = User.objects.create(username='john')
    order = Order.objects.create(user=user)

    p1 = Product.objects.create(name='A', base_price=100)
    p2 = Product.objects.create(name='B', base_price=200)

    OrderItem.objects.create(order=order, product=p1, quantity=2)
    OrderItem.objects.create(order=order, product=p2, quantity=1)

    assert order.subtotal() == 100*2 + 200*1  # = 400

@pytest.mark.django_db
def test_order_total_with_multiple_discounts():
    user = User.objects.create(username='alice')
    order = Order.objects.create(user=user)

    p = Product.objects.create(name='X', base_price=500)
    OrderItem.objects.create(order=order, product=p, quantity=1)

    # Create discounts
    d1 = Discount.objects.create(name='10% Off', discount_type='percentage', value=10, priority=2)
    d2 = Discount.objects.create(name='Fixed 50', discount_type='fixed', value=50, priority=1)

    order.discounts.add(d1, d2)
    # Use your OrderService to calculate total
    service = OrderService(order)
    total = service.calculate_total()

    # Subtotal = 500 → apply fixed 50 → 450 → apply 10% → 405
    assert total == 405.0

@pytest.mark.django_db
def test_order_tiered_discount_applies():
    user = User.objects.create(username='bob')
    order = Order.objects.create(user=user)

    # Tier: $500–1000 → 5%
    OrderTieredDiscount.objects.create(min_total=500, max_total=1000, discount_percent=5)

    p = Product.objects.create(name='Y', base_price=200)
    OrderItem.objects.create(order=order, product=p, quantity=3)  # $600 subtotal

    d = Discount.objects.create(name='Tiered', discount_type='tiered', value=0, priority=1)
    order.discounts.add(d)

    # Use your OrderService to calculate total
    service = OrderService(order)
    total = service.calculate_total()

    assert total == 600 * 0.95  # 570
