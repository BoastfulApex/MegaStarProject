# Generated by Django 4.2 on 2023-07-16 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_card_summa'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]