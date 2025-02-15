# Generated by Django 5.1.6 on 2025-02-15 20:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_sucursal', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_dueño', models.CharField(max_length=100)),
                ('modelo_telefono', models.CharField(max_length=100)),
                ('fono', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='^9\\s\\d{8}$')])),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telefonos', to='app.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.PositiveIntegerField(default=0)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='app.sucursal')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='app.tipo')),
            ],
        ),
    ]
