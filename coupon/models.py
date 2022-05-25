from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings

COUPON_TYPES = (
    ('PBO', 'Product Based'),
    ('CBO', 'Category Based'),
    ('FLO', 'Flat'),
    ('PVO', 'Percentage Based'),
    ('LCO', 'Limited Coupon'),
)


class Coupon(models.Model):
    coupon_type = models.CharField(max_length=3, choices=COUPON_TYPES)
    code = models.CharField(max_length=30, unique=True)
    activated_date = models.DateField()
    expiry_date = models.DateField()
    max_discount_price = models.DecimalField(max_digits=6, decimal_places=2)  # Flat offer
    price_boundary = models.DecimalField(max_digits=6, decimal_places=2)  # minimum order value
    percentage = models.PositiveIntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ], null=True, blank=True)
    coupon_count = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(1000),
        MinValueValidator(1)
    ], null=True, blank=True)
    product_name = models.CharField(max_length=100, null=True, blank=True)
    category_name = models.CharField(max_length=100, null=True, blank=True)

    def clean(self):
        if self.coupon_type == 'PVO':
            if not self.percentage:
                raise ValidationError('Percentage is must for Percentage based offer')
        if self.coupon_type == 'LCO':
            if not self.coupon_count:
                raise ValidationError('Coupon count is Must.')
        if self.coupon_type == 'PBO':
            if not self.product_name:
                raise ValidationError('Product Name is Must.')
        if self.coupon_type == 'CBO':
            if not self.category_name:
                raise ValidationError('Category name is Must')

    def __str__(self):
        return self.code


class CouponUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} -> {self.coupon.code}'
