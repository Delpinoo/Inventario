# Generated by Django 5.1.6 on 2025-02-11 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_producto_sucursal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='sucursal',
        ),
    ]
