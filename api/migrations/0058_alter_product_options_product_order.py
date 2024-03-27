# Generated by Django 4.2.7 on 2024-03-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_alter_product_description_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]