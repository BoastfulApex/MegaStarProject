# Generated by Django 4.2 on 2023-09-26 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_megauser_sale_cashback'),
    ]

    operations = [
        migrations.AddField(
            model_name='megauser',
            name='sale_cashback_summa',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
