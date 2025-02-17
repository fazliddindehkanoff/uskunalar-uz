from django.db import models
from ckeditor.fields import RichTextField

from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields


class Category(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title")
    )
    meta_title = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True)
    description = RichTextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    icon = models.FileField()
    available = models.BooleanField(default=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title_uz


class SubCategory(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title")
    )
    meta_title = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True)
    description = RichTextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    icon = models.FileField(null=True)
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title_uz

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"


class LineCategory(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title")
    )
    order = models.IntegerField()

    def __str__(self) -> str:
        return self.title_uz

    class Meta:
        verbose_name = "LineCategory"
        verbose_name_plural = "LineCategories"
        ordering = ["order"]
