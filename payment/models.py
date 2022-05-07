from django.db import models

from orders.models import Order
from customers.models import User

PAYMENT_STATUS = (
    ('PAID', 'Paid'),
    ('FAIL', 'Failed'),
    ('REFUND', 'Refund'),
)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)

    def __str__(self):
        return f'{self.id}'
