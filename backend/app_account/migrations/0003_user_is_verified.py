# Generated by Django 4.2.1 on 2025-03-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_account", "0002_profile_description_profile_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
