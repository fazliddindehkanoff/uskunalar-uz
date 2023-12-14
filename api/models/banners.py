from django.db import models

from .base import TranslatableModel, TranslatedFields
from config.models import BaseModel


class Banner(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        banner_image=models.ImageField(verbose_name="banner")
    )
    product_url = models.CharField(max_length=500)


class Partner(BaseModel):
    image = models.ImageField(verbose_name="banner")
