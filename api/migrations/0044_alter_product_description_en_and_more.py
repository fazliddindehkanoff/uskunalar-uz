# Generated by Django 4.2.7 on 2024-02-08 18:50

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0043_alter_product_description_en_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description_en",
            field=ckeditor.fields.RichTextField(null=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_ru",
            field=ckeditor.fields.RichTextField(null=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_uz",
            field=ckeditor.fields.RichTextField(null=True, verbose_name="description"),
        ),
    ]
