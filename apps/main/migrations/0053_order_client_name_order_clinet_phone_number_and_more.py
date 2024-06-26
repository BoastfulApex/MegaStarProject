# Generated by Django 4.2 on 2024-04-12 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_storycategory_story_story_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='clinet_phone_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='manager_phone_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='moll',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
