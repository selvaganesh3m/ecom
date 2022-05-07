from django.db import models
from customers.models import User, UserAddress
from products.models import Product
from django.conf import settings


# 2 Models
# Cart, CartItem


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.ForeignKey(UserAddress,
                                         on_delete=models.CASCADE,
                                         related_name='cart_shipping_address',
                                         null=True,
                                         blank=True)
    billing_address = models.ForeignKey(UserAddress,
                                        on_delete=models.CASCADE,
                                        related_name='cart_billing_address',
                                        null=True,
                                        blank=True)

    def __str__(self):
        return f'{self.id}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Cart Item {self.id}'
