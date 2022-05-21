from cart.models import Cart
from coupon.models import Coupon


def calculate_grand_total(cart: Cart) -> float:
    grand_total = 0
    for cart_item in cart.cart_items.all():
        grand_total += cart_item.total
    return grand_total
