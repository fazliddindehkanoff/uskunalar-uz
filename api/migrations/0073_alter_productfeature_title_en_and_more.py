# Generated by Django 4.2.7 on 2024-06-30 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_alter_productfeature_value_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeature',
            name='title_en',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='title_ru',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='title_uz',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
    ]