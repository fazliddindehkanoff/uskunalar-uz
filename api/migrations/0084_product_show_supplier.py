# Generated by Django 4.2.7 on 2025-01-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_remove_linedocuments_file_remove_linedocuments_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_supplier',
            field=models.BooleanField(default=False),
        ),
    ]
