# Generated by Django 3.2.6 on 2021-08-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_listing', '0018_alter_startup_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form_field',
            name='email_field',
        ),
        migrations.RemoveField(
            model_name='form_field',
            name='phone_field',
        ),
        migrations.AlterField(
            model_name='type_of_field',
            name='type_of',
            field=models.CharField(choices=[('CF', 'Character Filed'), ('TF', 'Text Field'), ('FF', 'File Field'), ('IF', 'Integer Field')], default='CR', max_length=2),
        ),
    ]
