# Generated by Django 4.2 on 2023-05-04 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_cashback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='u_sumuzs',
            field=models.FloatField(default=0, null=True),
        ),
    ]