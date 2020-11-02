# Generated by Django 3.1.2 on 2020-10-28 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    # TODO: Add dependencies to make sure the tests can be run
    dependencies = [
        ("cases", "0020_auto_20201027_0846"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bag_id", models.CharField(max_length=255, unique=True)),
                (
                    "street_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("number", models.IntegerField(blank=True, null=True)),
                (
                    "suffix_letter",
                    models.CharField(blank=True, max_length=1, null=True),
                ),
                ("suffix", models.CharField(blank=True, max_length=4, null=True)),
                ("postal_code", models.CharField(blank=True, max_length=7, null=True)),
                ("lat", models.FloatField(blank=True, null=True)),
                ("lng", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.RunSQL(
            """
            INSERT INTO addresses_address (
                id,
                bag_id,
                street_name,
                number,
                suffix_letter,
                suffix,
                postal_code,
                lat,
                lng
            )
            SELECT
                id,
                bag_id,
                street_name,
                number,
                suffix_letter,
                suffix,
                postal_code,
                lat,
                lng
            FROM
                cases_address;
        """,
            reverse_sql="""
            INSERT INTO cases_address (
                id,
                bag_id,
                street_name,
                number,
                suffix_letter,
                suffix,
                postal_code,
                lat,
                lng
            )
            SELECT
                id,
                bag_id,
                street_name,
                number,
                suffix_letter,
                suffix,
                postal_code,
                lat,
                lng
            FROM
                addresses_address;
        """,
        ),
    ]
