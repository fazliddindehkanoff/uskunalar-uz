# Generated by Django 4.2.7 on 2023-11-10 22:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_blog"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("icon", models.FileField(upload_to="")),
                ("title_en", models.CharField(max_length=250, verbose_name="Title")),
                ("title_uz", models.CharField(max_length=250, verbose_name="Title")),
                ("title_ru", models.CharField(max_length=250, verbose_name="Title")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
