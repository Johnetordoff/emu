# Generated by Django 3.1.1 on 2021-07-21 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_user_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schema',
            old_name='csv_uploads',
            new_name='csv',
        ),
    ]
