# Generated by Django 4.2.7 on 2024-06-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_alter_backgroundbanner_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
