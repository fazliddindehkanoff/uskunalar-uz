# Generated by Django 4.2.7 on 2024-02-14 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0049_partnerlogos_delete_partner_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description_en",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, null=True, verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_ru",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, null=True, verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description_uz",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True, null=True, verbose_name="Description"
            ),
        ),
        migrations.CreateModel(
            name="Order",
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
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="api.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
