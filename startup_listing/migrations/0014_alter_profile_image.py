# Generated by Django 3.2.6 on 2021-08-07 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0013_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='dp/avatar.png', upload_to='dp'),
        ),
    ]