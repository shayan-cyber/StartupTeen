# Generated by Django 3.2.6 on 2021-08-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0027_auto_20210815_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='work_experience',
            field=models.FloatField(default=0),
        ),
    ]
