# Generated by Django 4.2 on 2023-09-14 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_sale_description_sale_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='top',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]