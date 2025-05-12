import pytest
from apps.products.models import Product, SeasonalDiscount
from apps.products.services import SeasonalProduct, BulkProduct, PremiumProduct  # Replace path if different

@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_name, base_price, product_type, quantity, discount, expected_price",
    [
        # Seasonal product: 20% off
        ("Jacket", 100, "seasonal", 1, 20, 80.0),
        ("Jacket", 200, "seasonal", 2, 10, 360.0),  # 10% off
        
        # Bulk product: tiered quantity discount
        ("Pen", 10, "bulk", 5, None, 50.0),         # No discount
        ("Pen", 10, "bulk", 15, None, 142.5),       # 5% off
        ("Pen", 10, "bulk", 25, None, 225.0),       # 10% off
        ("Pen", 10, "bulk", 55, None, 467.5),       # 15% off
        
        # Premium product: 15% markup
        ("Laptop", 1000, "premium", 1, None, 1150.0),
        ("Monitor", 500, "premium", 2, None, 1150.0),
    ]
)
def test_product_dynamic_price(product_name, base_price, product_type, quantity, discount, expected_price):
    # Create product instance
    product = Product.objects.create(name=product_name, base_price=base_price, product_type=product_type)

    # Handle seasonal discount setup if applicable
    if product_type == "seasonal" and discount is not None:
        SeasonalDiscount.objects.create(discount_percent=discount, is_active=True)

    # Price calculation using respective class
    if product_type == "seasonal":
        priced_product = SeasonalProduct()
    elif product_type == "bulk":
        priced_product = BulkProduct()
    elif product_type == "premium":
        priced_product = PremiumProduct()
    else:
        pytest.fail(f"Unknown product type: {product_type}")
