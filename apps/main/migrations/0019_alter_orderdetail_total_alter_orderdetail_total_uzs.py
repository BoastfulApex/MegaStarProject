# Generated by Django 4.1.4 on 2023-04-14 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_rename_ordetdetail_orderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='total',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='total_uzs',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
