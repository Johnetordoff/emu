# Generated by Django 3.1.1 on 2021-06-11 12:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, help_text='Enter as comma seperated list', null=True, size=None),
        ),
    ]
