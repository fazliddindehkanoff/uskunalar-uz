# Generated by Django 4.2.7 on 2024-02-02 21:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0039_customuser_language_alter_product_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="approved",
            field=models.BooleanField(default=False),
        ),
    ]