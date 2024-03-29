# Generated by Django 4.2 on 2024-02-06 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_pushtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('index', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='story',
            name='story_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.storycategory'),
        ),
    ]
