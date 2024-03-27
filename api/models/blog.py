from django.db import models
from mdeditor.fields import MDTextField

from .category import LineCategory
from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class Blog(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        content=MDTextField("Text", config_name="extends"),
    )
    cover = models.ImageField(null=True, blank=True)
    view_count = models.IntegerField(default=0)


class Video(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        description=models.TextField(),
    )
    video_link = models.CharField(max_length=250)


class Line(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        short_description=models.TextField(),
        long_description=MDTextField("Text", config_name="extends"),
    )
    price = models.IntegerField()
    category = models.ForeignKey(LineCategory, on_delete=models.CASCADE)
    image = models.ImageField()
    banner = models.ImageField()
    views = models.IntegerField()


class Work(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        short_description=MDTextField("Text", config_name="extends"),
        long_description=MDTextField("Text", config_name="extends"),
    )
    image = models.ImageField()
    views = models.IntegerField()
