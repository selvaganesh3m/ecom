# Generated by Django 3.2 on 2022-05-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0003_coupon_price_boundary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='price_boundary',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
