from django.db import models
from mdeditor.fields import MDTextField

from .category import LineCategory
from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class Blog(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        content=MDTextField("Blog Content", config_name="extends"),
    )
    cover = models.ImageField(null=True, blank=True)
    view_count = models.IntegerField(default=0)


class Video(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        description=MDTextField("description", config_name="extends"),
    )
    video_link = models.CharField(max_length=250)


class Line(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        short_description=models.TextField(verbose_name="Short description"),
        long_description=MDTextField("Description", config_name="extends"),
    )
    price = models.IntegerField()
    category = models.ForeignKey(
        LineCategory, on_delete=models.CASCADE, related_name="lines"
    )
    image = models.ImageField()
    banner = models.ImageField()
    view_count = models.IntegerField()


class Work(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        short_description=MDTextField("Short description", config_name="extends"),
        long_description=MDTextField("Description", config_name="extends"),
    )
    image = models.ImageField()
    view_count = models.IntegerField()
