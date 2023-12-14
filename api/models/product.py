from django.db import models
from mdeditor.fields import MDTextField

from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields
from .constants import CIP_STATUS_CHOISES, AVAILABILITY_STATUS_CHOISES


class Product(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=250, verbose_name="Name", blank=True),
        description=MDTextField(verbose_name="description", blank=True),
    )
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    tags = models.CharField(max_length=500, default="", blank=True)
    min_price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    availability_status = models.IntegerField(
        default=1, choices=AVAILABILITY_STATUS_CHOISES
    )
    discount = models.DecimalField(
        max_digits=9, decimal_places=0, null=True, blank=True
    )
    cip_type = models.IntegerField(default=1, choices=CIP_STATUS_CHOISES)
    view_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name_uz


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


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField()
