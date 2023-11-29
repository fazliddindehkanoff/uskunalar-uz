from django.db import models
from .base import TranslatableModel, TranslatedFields
from config.models import BaseModel


class ProductFeature(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        value=models.CharField(max_length=250, verbose_name="Value"),
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="specifications",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.title_uz} - {self.value_uz}"
