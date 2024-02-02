# Generated by Django 4.2.7 on 2024-01-11 00:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0037_customuser_category_customuser_role_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
