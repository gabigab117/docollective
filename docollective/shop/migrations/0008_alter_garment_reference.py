# Generated by Django 4.2.5 on 2023-10-11 20:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_garment_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garment',
            name='reference',
            field=models.UUIDField(blank=True, default=uuid.uuid4, verbose_name='Référence'),
        ),
    ]