# Generated by Django 3.2 on 2022-05-20 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20220519_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='applied_coupon',
            field=models.BooleanField(default=False),
        ),
    ]
