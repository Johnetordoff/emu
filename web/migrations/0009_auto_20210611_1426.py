# Generated by Django 3.1.1 on 2021-06-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_question_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='help',
            field=models.CharField(blank=True, help_text='AKA help_text', max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(blank=True, help_text='AKA Display_text', max_length=5000, null=True),
        ),
    ]
