# Generated by Django 4.2 on 2023-07-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_megauser_all_cashback_megauser_is_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='megauser',
            name='all_cashback',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='megauser',
            name='is_sale',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
