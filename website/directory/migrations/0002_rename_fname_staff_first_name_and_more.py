# Generated by Django 4.2.3 on 2023-08-02 14:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("directory", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="staff",
            old_name="fname",
            new_name="first_name",
        ),
        migrations.RenameField(
            model_name="staff",
            old_name="lname",
            new_name="last_name",
        ),
    ]
