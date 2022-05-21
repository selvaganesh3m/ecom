# Generated by Django 3.2 on 2022-05-20 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_cart_coupon_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]