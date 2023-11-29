# Generated by Django 4.2.7 on 2023-11-12 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_subcategory"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("title", models.CharField(max_length=250)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("min_price", models.IntegerField()),
                ("max_price", models.IntegerField()),
                ("name_en", models.CharField(max_length=250, verbose_name="Name")),
                ("name_uz", models.CharField(max_length=250, verbose_name="Name")),
                ("name_ru", models.CharField(max_length=250, verbose_name="Name")),
                (
                    "subcategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.subcategory",
                    ),
                ),
                ("tags", models.ManyToManyField(to="api.tag")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
