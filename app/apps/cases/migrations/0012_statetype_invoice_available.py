# Generated by Django 3.0.8 on 2020-08-07 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0011_state_invoice_identification"),
    ]

    operations = [
        migrations.AddField(
            model_name="statetype",
            name="invoice_available",
            field=models.BooleanField(default=False),
        ),
    ]