# Generated by Django 4.1.4 on 2023-04-13 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_order_total_sum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_sum',
            new_name='u_sumuzs',
        ),
    ]
