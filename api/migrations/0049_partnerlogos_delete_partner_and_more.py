# Generated by Django 4.2.7 on 2024-02-14 07:30

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0048_alter_blog_content_en_alter_blog_content_ru_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnerLogos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("image", models.ImageField(upload_to="", verbose_name="banner")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="Partner",
        ),
        migrations.AlterField(
            model_name="product",
            name="description_en",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, null=True, verbose_name="Text"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_ru",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, null=True, verbose_name="Text"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_uz",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, null=True, verbose_name="Text"
            ),
        ),
    ]
