# Generated by Django 3.2 on 2022-05-20 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0006_remove_coupon_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UsedCoupon',
        ),
    ]