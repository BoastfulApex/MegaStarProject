# Generated by Django 4.2 on 2024-02-08 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_megauser_sale_cashback_summa'),
    ]

    operations = [
        migrations.AddField(
            model_name='megauser',
            name='is_media_staff',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
