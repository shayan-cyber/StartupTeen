# Generated by Django 3.2.6 on 2021-08-08 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0016_auto_20210808_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup_project',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]