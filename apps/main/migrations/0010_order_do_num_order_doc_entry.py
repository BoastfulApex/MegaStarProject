# Generated by Django 4.1.4 on 2023-04-12 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_subcategory_u_group_subcategory_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='do_num',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='doc_entry',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
