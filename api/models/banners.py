from django.db import models

from .base import TranslatableModel, TranslatedFields
from config.models import BaseModel


class Banner(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        banner_image=models.ImageField(verbose_name="banner")
    )
    product_url = models.CharField(max_length=500)


class PartnerLogos(BaseModel):
    image = models.ImageField(verbose_name="banner")


class BackgroundBanner(BaseModel):
    title = models.CharField(default="", blank=True)
    image = models.ImageField(verbose_name="banner")
