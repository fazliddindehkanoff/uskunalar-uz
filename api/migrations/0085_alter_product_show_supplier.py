# Generated by Django 4.2.7 on 2025-01-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_product_show_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='show_supplier',
            field=models.BooleanField(default=True),
        ),
    ]
