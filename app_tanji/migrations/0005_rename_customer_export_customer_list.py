# Generated by Django 4.2.5 on 2023-10-14 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_tanji', '0004_rename_tanji_customer_export_customer_export'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='customer_export',
            new_name='customer_list',
        ),
    ]
