# Generated by Django 4.1.4 on 2023-04-11 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_megauser_odata_etag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='megauser',
            name='phone',
            field=models.BigIntegerField(unique=True),
        ),
    ]
