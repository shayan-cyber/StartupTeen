# Generated by Django 3.2.6 on 2021-08-06 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0005_auto_20210806_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='about',
            field=models.TextField(default=''),
        ),
    ]