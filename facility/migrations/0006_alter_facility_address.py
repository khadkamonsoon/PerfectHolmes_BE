# Generated by Django 3.2 on 2024-04-21 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("facility", "0005_alter_facility_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facility",
            name="address",
            field=models.CharField(
                blank=True, help_text="주소", max_length=300, null=True
            ),
        ),
    ]
