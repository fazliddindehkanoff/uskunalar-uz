# Generated by Django 4.2.7 on 2025-03-13 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0093_productpricebasedonmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpricebasedonmodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
