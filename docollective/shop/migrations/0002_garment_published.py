# Generated by Django 4.2.5 on 2023-10-10 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='garment',
            name='published',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2023, 10, 10, 21, 24, 15, 919408, tzinfo=datetime.timezone.utc), verbose_name='Date de publication'),
            preserve_default=False,
        ),
    ]