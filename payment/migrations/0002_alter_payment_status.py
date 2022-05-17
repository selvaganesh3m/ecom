# Generated by Django 3.2 on 2022-05-16 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('FAIL', 'Failed'), ('REFUND', 'Refund'), ('PEND', 'Pending')], default='PEND', max_length=10),
        ),
    ]