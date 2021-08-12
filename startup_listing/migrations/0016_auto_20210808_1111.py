# Generated by Django 3.2.6 on 2021-08-08 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0015_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dev_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='skill',
            name='profile',
            field=models.ManyToManyField(to='startup_listing.Profile'),
        ),
        migrations.RemoveField(
            model_name='skill',
            name='project',
        ),
        migrations.AddField(
            model_name='skill',
            name='project',
            field=models.ManyToManyField(to='startup_listing.Startup_Project'),
        ),
    ]