from django.contrib.auth import get_user_model
from apps.products.models import Product, BulkPricingTier, SeasonalDiscount, PremiumMarkup
from apps.discounts.models import Discount
from apps.orders.models import Order, OrderItem
from apps.orders.services import OrderService
from apps.discounts.models import OrderTieredDiscount

User = get_user_model()

# 1. Create test user
user, _ = User.objects.get_or_create(username='testuser')
user.set_password('testpass123')
user.save()

# 2. Create Bulk Pricing Tiers
BulkPricingTier.objects.all().delete()
BulkPricingTier.objects.create(min_qty=10, max_qty=20, discount_percent=5)
BulkPricingTier.objects.create(min_qty=21, max_qty=50, discount_percent=10)
BulkPricingTier.objects.create(min_qty=51, max_qty=None, discount_percent=15)

# 3. Create Seasonal Discount (active)
SeasonalDiscount.objects.all().delete()
SeasonalDiscount.objects.create(season='Winter', discount_percent=20, is_active=True)

# 4. Create Premium Markup
PremiumMarkup.objects.all().delete()
PremiumMarkup.objects.create(markup_percent=15)

# 5. Create Order Tiered Discounts
OrderTieredDiscount.objects.all().delete()
OrderTieredDiscount.objects.create(min_total=500, max_total=1000, discount_percent=5)
OrderTieredDiscount.objects.create(min_total=1001, max_total=None, discount_percent=10)

# 6. Create Products
Product.objects.all().delete()
bulk_product = Product.objects.create(name="Bulk T-Shirt", base_price=10.0, product_type="bulk")
seasonal_product = Product.objects.create(name="Winter Jacket", base_price=100.0, product_type="seasonal")
premium_product = Product.objects.create(name="Premium Watch", base_price=200.0, product_type="premium")

# 7. Create Discounts
Discount.objects.all().delete()
percentage_discount = Discount.objects.create(name="10% Off", discount_type="percentage", value=10, priority=1)
fixed_discount = Discount.objects.create(name="$50 Off", discount_type="fixed", value=50, priority=2)
tiered_discount = Discount.objects.create(name="Tiered Order Discount", discount_type="tiered", value=0, priority=3)

# 8. Create Order with Items
order = Order.objects.create(user=user)
OrderItem.objects.create(order=order, product=bulk_product, quantity=25)
OrderItem.objects.create(order=order, product=seasonal_product, quantity=1)
OrderItem.objects.create(order=order, product=premium_product, quantity=1)
order.discounts.add(percentage_discount, fixed_discount, tiered_discount)

# 9. Calculate total
order_service = OrderService(order)
total = order_service.calculate_total()
print(f"Order #{order.id} total after discounts: ${total:.2f}")
