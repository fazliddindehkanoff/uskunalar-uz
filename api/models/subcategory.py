from django.db import models

from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class SubCategory(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title")
    )
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title_uz

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
