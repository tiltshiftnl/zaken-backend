# Generated by Django 3.1.2 on 2020-10-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debriefings", "0005_auto_20201027_1016"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debriefing",
            name="violation",
            field=models.CharField(
                choices=[
                    ("NO", "No"),
                    ("YES", "Yes"),
                    ("ADDITIONAL_RESEARCH_REQUIRED", "Additional research required"),
                ],
                default="NO",
                max_length=28,
            ),
        ),
    ]
