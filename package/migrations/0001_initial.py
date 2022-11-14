# Generated by Django 4.0 on 2022-11-14 22:13

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('weight', models.DecimalField(decimal_places=2, default=0, help_text='weight in kilograms', max_digits=5, verbose_name='weight')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='price')),
            ],
            options={
                'verbose_name': 'furniture',
                'verbose_name_plural': 'furnitures',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('customer_name', models.CharField(max_length=30, verbose_name='customer name')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Ready To Send'), (3, 'Sent')], default=1)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('number', models.CharField(max_length=40, verbose_name='number')),
                ('weight', models.DecimalField(decimal_places=2, default=0, help_text='weight in kilograms', max_digits=5, verbose_name='weight')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='package.furniture')),
            ],
            options={
                'verbose_name': 'package',
                'verbose_name_plural': 'packages',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='package.furniture')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='package.order')),
            ],
            options={
                'verbose_name': 'order item',
                'verbose_name_plural': 'order items',
            },
        ),
    ]
