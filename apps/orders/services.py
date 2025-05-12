from apps.discounts.services import PercentageDiscount, FixedDiscount, TieredDiscount, Discount

class OrderService:
    def __init__(self, order):
        self.order = order

    def calculate_total(self):
        subtotal = self.order.subtotal()
        total = subtotal
        for discount in self.order.discounts.order_by('priority'):
            strategy = self.get_strategy(discount)
            total = strategy.apply(total)
        return total

    def get_strategy(self, discount):
        if discount.discount_type == 'percentage':
            return PercentageDiscount(discount.value)
        elif discount.discount_type == 'fixed':
            return FixedDiscount(discount.value)
        elif discount.discount_type == 'tiered':
            return TieredDiscount(self.order.subtotal())
        return Discount()
