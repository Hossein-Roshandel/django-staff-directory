# Generated by Django 4.2.3 on 2023-07-29 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0004_remove_staff_qrcode_image_staff_qrcode_img_vcard_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='office',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='title',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]