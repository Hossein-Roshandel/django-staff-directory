# Generated by Django 4.2.3 on 2023-07-30 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0005_alter_staff_office_alter_staff_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='company_url',
            field=models.URLField(blank=True, null=True, verbose_name='Company Website'),
        ),
    ]
