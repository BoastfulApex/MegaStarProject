# Generated by Django 4.2 on 2023-06-19 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('summa', models.IntegerField()),
            ],
        ),
    ]
