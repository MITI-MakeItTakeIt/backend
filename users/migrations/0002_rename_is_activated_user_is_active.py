# Generated by Django 4.1.5 on 2023-01-26 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_activated",
            new_name="is_active",
        ),
    ]