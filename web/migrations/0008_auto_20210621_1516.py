# Generated by Django 3.1.1 on 2021-06-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0007_auto_20210621_1427"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="csv_uploads",
            field=models.FileField(null=True, upload_to="csv_uploads/"),
        ),
    ]
