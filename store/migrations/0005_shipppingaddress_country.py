# Generated by Django 3.1.5 on 2021-02-14 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210214_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipppingaddress',
            name='country',
            field=models.CharField(default='India', max_length=200),
        ),
    ]
