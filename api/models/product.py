from django.db import models
from mdeditor.fields import MDTextField

from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields
from .constants import CIP_STATUS_CHOISES, AVAILABILITY_STATUS_CHOISES


class Product(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=250, verbose_name="Name"),
        description=MDTextField(verbose_name="description"),
    )
    subcategory = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    availability_status = models.IntegerField(
        default=1, choices=AVAILABILITY_STATUS_CHOISES
    )
    discount = models.DecimalField(max_digits=9, decimal_places=0, null=True)
    cip_type = models.IntegerField(default=1, choices=CIP_STATUS_CHOISES)

    def __str__(self) -> str:
        return self.name_uz
