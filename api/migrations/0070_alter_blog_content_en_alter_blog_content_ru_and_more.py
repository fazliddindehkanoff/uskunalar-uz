# Generated by Django 4.2.7 on 2024-06-30 19:18

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_alter_blog_content_en_alter_blog_content_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content_en',
            field=ckeditor.fields.RichTextField(verbose_name='Blog Content'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content_ru',
            field=ckeditor.fields.RichTextField(verbose_name='Blog Content'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content_uz',
            field=ckeditor.fields.RichTextField(verbose_name='Blog Content'),
        ),
        migrations.AlterField(
            model_name='line',
            name='long_description_en',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='line',
            name='long_description_ru',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='line',
            name='long_description_uz',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_ru',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_uz',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description_en',
            field=ckeditor.fields.RichTextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description_ru',
            field=ckeditor.fields.RichTextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description_uz',
            field=ckeditor.fields.RichTextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='work',
            name='long_description_en',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='work',
            name='long_description_ru',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='work',
            name='long_description_uz',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='work',
            name='short_description_en',
            field=ckeditor.fields.RichTextField(verbose_name='Short description'),
        ),
        migrations.AlterField(
            model_name='work',
            name='short_description_ru',
            field=ckeditor.fields.RichTextField(verbose_name='Short description'),
        ),
        migrations.AlterField(
            model_name='work',
            name='short_description_uz',
            field=ckeditor.fields.RichTextField(verbose_name='Short description'),
        ),
    ]
