# Generated by Django 3.1.3 on 2020-11-06 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0013_auto_20201103_0415"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="caseevent",
            options={"ordering": ["-date_created"]},
        ),
    ]
