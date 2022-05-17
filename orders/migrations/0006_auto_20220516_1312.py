# Generated by Django 3.2 on 2022-05-16 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PAYMENT_PENDING', 'Payment Pending'), ('PROCESSING', 'Processing'), ('SUCCESS', 'Success'), ('REFUND', 'Refund'), ('FAILED', 'Failed')], default='PAYMENT_PENDING', max_length=120),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
