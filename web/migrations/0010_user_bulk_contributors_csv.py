# Generated by Django 3.1.1 on 2021-07-01 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0009_auto_20210621_1517"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bulk_contributors_csv",
            field=models.FileField(
                blank=True, null=True, upload_to="csv/bulk_contributors/"
            ),
        ),
    ]
