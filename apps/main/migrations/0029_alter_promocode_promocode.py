# Generated by Django 4.2 on 2023-06-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_promocode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='promocode',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]