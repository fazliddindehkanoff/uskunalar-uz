from django.db import models
from ckeditor.fields import RichTextField

from .category import LineCategory
from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class Blog(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        content=RichTextField(verbose_name="Blog Content"),
    )
    cover = models.ImageField(null=True, blank=True)
    view_count = models.IntegerField(default=0)


class Video(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name="Title",
            null=True,
        ),
        description=RichTextField(
            verbose_name="description",
            null=True,
        ),
    )
    video_link = models.CharField(max_length=250)


class Line(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        short_description=models.TextField(
            verbose_name="Short description",
            null=True,
        ),
        long_description=RichTextField(
            verbose_name="Description",
            null=True,
        ),
    )
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)

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
        short_description=RichTextField(
            verbose_name="Short description",
            null=True,
        ),
        long_description=RichTextField(
            verbose_name="Description",
            null=True,
        ),
    )
    image = models.ImageField()
    view_count = models.IntegerField()


class Gallery(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name="Title",
            blank=True,
        ),
        short_description=models.TextField(
            null=True,
            verbose_name="short description",
        ),
        description=RichTextField(
            verbose_name="Description",
            blank=True,
            null=True,
        ),
    )
    video_url = models.CharField(max_length=255, null=True, blank=True)
    view_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title_uz


class GalleryImage(BaseModel):
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()
