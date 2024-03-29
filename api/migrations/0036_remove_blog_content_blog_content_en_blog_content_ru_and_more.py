# Generated by Django 4.2.7 on 2024-01-09 20:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0035_alter_product_description_en_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blog",
            name="content",
        ),
        migrations.AddField(
            model_name="blog",
            name="content_en",
            field=ckeditor.fields.RichTextField(
                default="test", verbose_name="blog_content"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="blog",
            name="content_ru",
            field=ckeditor.fields.RichTextField(
                default="test", verbose_name="blog_content"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="blog",
            name="content_uz",
            field=ckeditor.fields.RichTextField(
                default="test", verbose_name="blog_content"
            ),
            preserve_default=False,
        ),
    ]
