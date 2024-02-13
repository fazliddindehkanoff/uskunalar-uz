from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class Blog(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        content=CKEditor5Field("Text", config_name="extends"),
    )
    cover = models.ImageField(null=True, blank=True)
