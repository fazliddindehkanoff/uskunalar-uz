# Generated by Django 4.2.7 on 2024-06-28 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_category_available_subcategory_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_type',
            field=models.IntegerField(choices=[(1, 'HTML'), (2, 'Markdown')], default=1),
        ),
    ]
