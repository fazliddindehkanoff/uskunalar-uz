# Generated by Django 4.2.7 on 2024-01-09 20:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0034_alter_supplier_cooperational_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description_en",
            field=ckeditor.fields.RichTextField(blank=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_ru",
            field=ckeditor.fields.RichTextField(blank=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_uz",
            field=ckeditor.fields.RichTextField(blank=True, verbose_name="description"),
        ),
    ]
