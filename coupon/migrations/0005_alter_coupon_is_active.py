# Generated by Django 3.2 on 2022-05-18 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0004_alter_coupon_price_boundary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(),
        ),
    ]
