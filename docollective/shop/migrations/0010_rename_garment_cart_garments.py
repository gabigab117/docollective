# Generated by Django 4.2.5 on 2023-10-11 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='garment',
            new_name='garments',
        ),
    ]
