# Generated by Django 4.2.5 on 2023-10-12 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0011_alter_garment_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='garments',
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.UUIDField(default=uuid.uuid4, verbose_name='Référence')),
                ('ordered', models.BooleanField(default=False, verbose_name='Acquitté')),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('garment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.garment', verbose_name='Vêtements')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Commande',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(to='shop.order', verbose_name='Vêtements'),
        ),
    ]
