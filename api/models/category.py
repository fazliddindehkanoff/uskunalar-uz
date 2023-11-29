from django.db import models

from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class Category(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title")
    )
    icon = models.FileField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title_uz
