# Generated by Django 3.2.6 on 2021-08-08 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0017_startup_project_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='startup_listing.profile'),
        ),
    ]