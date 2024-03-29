# Generated by Django 4.2.7 on 2024-01-10 21:41

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0036_remove_blog_content_blog_content_en_blog_content_ru_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.category",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[("ADMIN", "Admin"), ("EDITOR", "Editor")],
                default="EDITOR",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="subcategory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.subcategory",
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="content_en",
            field=ckeditor.fields.RichTextField(verbose_name="blog Content"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="content_ru",
            field=ckeditor.fields.RichTextField(verbose_name="blog Content"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="content_uz",
            field=ckeditor.fields.RichTextField(verbose_name="blog Content"),
        ),
    ]
