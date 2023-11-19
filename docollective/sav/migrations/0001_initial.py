# Generated by Django 4.2.5 on 2023-11-19 17:47

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(default=uuid.uuid4, max_length=36)),
                ('subject', models.CharField(max_length=200, verbose_name='Objet')),
                ('closed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', ckeditor.fields.RichTextField(verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Publication')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sav.ticket', verbose_name='Ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]
