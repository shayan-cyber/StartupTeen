# Generated by Django 3.2.6 on 2021-08-06 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0004_form_field_type_of_field'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Community',
        ),
        migrations.RenameField(
            model_name='startup_project',
            old_name='category',
            new_name='community',
        ),
    ]