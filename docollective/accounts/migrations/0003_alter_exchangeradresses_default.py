# Generated by Django 4.2.5 on 2023-10-05 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_exchangeradresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangeradresses',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Défaut'),
        ),
    ]
