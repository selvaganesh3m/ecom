from django.db import models
from customers.models import UserAddress
from products.models import Product
from django.conf import settings
from cart.models import Cart

# 2 Models
# Order OrderItem


STATUS_CHOICES = (
    ('PAYMENT_PENDING', 'Payment Pending'),
    ('PROCESSING', 'Processing'),
    ('SHIPPED', 'Shipped'),
    ('OUT_FOR_DELIVERY', 'Out for Delivery'),
    ('DELIVERED', 'Delivered'),
    ('REFUND', 'Refund'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField(default=0)  # in percentage validation
    shipping_address = models.ForeignKey(UserAddress,
                                         on_delete=models.CASCADE,
                                         related_name='order_shipping_address')
    billing_address = models.ForeignKey(UserAddress,
                                        on_delete=models.CASCADE,
                                        related_name='order_billing_address')
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='PAYMENT_PENDING')
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Order ID {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f' OrderItem ID {self.id}'
