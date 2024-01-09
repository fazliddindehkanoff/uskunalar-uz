from django.db import models
from ckeditor.fields import RichTextField
from .base import TranslatableModel, TranslatedFields


class Blog(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name="Title"),
        content=RichTextField(verbose_name="blog_content"),
    )
    cover = models.ImageField(null=True, blank=True)
