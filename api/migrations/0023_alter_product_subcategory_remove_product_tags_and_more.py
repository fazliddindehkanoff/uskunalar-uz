# Generated by Django 4.2.7 on 2023-12-05 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0022_alter_product_subcategory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="subcategory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.subcategory"
            ),
        ),
        migrations.RemoveField(
            model_name="product",
            name="tags",
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.CharField(
                help_text=", orqali ajratib yozing!", max_length=500, null=True
            ),
        ),
    ]
