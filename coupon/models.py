from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=30)
    activated_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
