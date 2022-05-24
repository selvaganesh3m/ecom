from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    activated_date = models.DateField()
    expiry_date = models.DateField()
    max_discount_price = models.DecimalField(max_digits=6, decimal_places=2)
    price_boundary = models.PositiveIntegerField(null=True, blank=True)
    percentage = models.PositiveIntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])

    def __str__(self):
        return self.code


class CouponUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} -> {self.coupon.code}'
