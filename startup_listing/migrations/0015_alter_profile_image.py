# Generated by Django 3.2.6 on 2021-08-07 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0014_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='avatar.png', upload_to='dp'),
        ),
    ]
