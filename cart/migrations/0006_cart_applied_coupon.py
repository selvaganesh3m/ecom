# Generated by Django 3.2 on 2022-05-19 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20220519_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='applied_coupon',
            field=models.BooleanField(default=False),
        ),
    ]
