# Generated by Django 4.2.7 on 2025-03-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0091_work_yt_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
