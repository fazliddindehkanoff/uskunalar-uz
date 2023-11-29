from django.db import models
from mdeditor.fields import MDTextField
from .base import TranslatableModel, TranslatedFields


class Blog(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title")
    )
    content = MDTextField()
    cover = models.ImageField(null=True, blank=True)
