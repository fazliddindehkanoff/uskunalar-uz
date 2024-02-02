# Generated by Django 4.2.7 on 2024-01-09 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0032_supplier_product_related_products_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="supplier",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.supplier",
            ),
        ),
    ]