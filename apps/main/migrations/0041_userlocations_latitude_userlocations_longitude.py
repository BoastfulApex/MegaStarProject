# Generated by Django 4.2 on 2023-07-21 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_userlocations'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocations',
            name='latitude',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='userlocations',
            name='longitude',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
