# Generated by Django 3.2 on 2022-05-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_alter_user_jti'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='jti',
            field=models.CharField(default='127d3266eb71cced0a0d7306a12b1b374bde189fcefcd266f1d5a76f55a3414c', editable=False, max_length=64),
        ),
    ]