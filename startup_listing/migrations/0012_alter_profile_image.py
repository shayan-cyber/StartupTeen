# Generated by Django 3.2.6 on 2021-08-07 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0011_auto_20210807_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='https://via.placeholder.com/150', null=True, upload_to='dp'),
        ),
    ]
