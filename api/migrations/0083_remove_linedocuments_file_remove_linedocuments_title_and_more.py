# Generated by Django 4.2.7 on 2024-11-25 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_linedocuments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linedocuments',
            name='file',
        ),
        migrations.RemoveField(
            model_name='linedocuments',
            name='title',
        ),
        migrations.AddField(
            model_name='linedocuments',
            name='file_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
