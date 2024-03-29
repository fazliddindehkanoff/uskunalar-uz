# Generated by Django 4.2.7 on 2024-02-09 10:12

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0047_alter_product_description_en_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="content_en",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="content_ru",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="content_uz",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_en",
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_ru",
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_uz",
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
    ]
