# Generated by Django 3.2 on 2022-05-19 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_cart_applied_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='applied_coupon',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='grand_total',
        ),
    ]