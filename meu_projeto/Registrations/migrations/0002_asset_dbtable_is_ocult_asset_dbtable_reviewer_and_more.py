# Generated by Django 5.0.2 on 2024-11-22 02:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registrations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_dbtable',
            name='is_ocult',
            field=models.BooleanField(default=False, verbose_name='Ocultar'),
        ),
        migrations.AddField(
            model_name='asset_dbtable',
            name='reviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asset_dbtable',
            name='show_to',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Mostrar para'),
        ),
        migrations.AddField(
            model_name='subitem_dbtable',
            name='is_ocult',
            field=models.BooleanField(default=False, verbose_name='Ocultar'),
        ),
        migrations.AddField(
            model_name='subitem_dbtable',
            name='show_to',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Mostrar para'),
        ),
    ]
