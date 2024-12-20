# Generated by Django 5.0.2 on 2024-11-01 14:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project_DBTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Criação')),
                ('uptaded_at', models.DateField(auto_now=True, null=True, verbose_name='Modificação')),
                ('projectName', models.CharField(max_length=100)),
                ('projectDescription', models.TextField()),
                ('image', models.ImageField(default='projects_images/default.jpg', upload_to='projects_images/')),
                ('status', models.CharField(choices=[('Arquivado', 'Arquivado'), ('Ativo', 'Ativo')], default='Ativo', max_length=100, verbose_name='Status')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.company_dbtable')),
                ('user_has_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('user_has_modified', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
