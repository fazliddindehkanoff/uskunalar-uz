from django.db import models

from config.models import BaseModel


class Partner(BaseModel):
    image = models.ImageField(verbose_name="banner")
