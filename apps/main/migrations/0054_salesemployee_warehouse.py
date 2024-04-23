# Generated by Django 4.2 on 2024-04-23 18:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_order_client_name_order_clinet_phone_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('edited_date', models.DateTimeField(blank=True, null=True)),
                ('employee_code', models.IntegerField(null=True)),
                ('employee_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('ware_house', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('edited_date', models.DateTimeField(blank=True, null=True)),
                ('warehouse_code', models.CharField(blank=True, max_length=1000, null=True)),
                ('warehouse_name', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
