from django.db import models
from ckeditor.fields import RichTextField

from api.models.users import CustomUser
from config.models import BaseModel
from .base import TranslatableModel, TranslatedFields
from .constants import (
    AVAILABILITY_STATUS_TRANSLATIONS,
    CIP_STATUS_CHOISES,
    AVAILABILITY_STATUS_CHOISES,
    COOPERATIONAL_STATUS_CHOICES,
    ORDER_STATUS_CHOISES,
)


class Supplier(TranslatableModel, BaseModel):
    company_name = models.CharField(max_length=255)
    experience = models.IntegerField()
    short_details = RichTextField(
        verbose_name="short details",
        blank=True,
        null=True,
    )
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    logo = models.FileField()
    cooperational_status = models.IntegerField(
        choices=COOPERATIONAL_STATUS_CHOICES,
    )

    def __str__(self) -> str:
        return f"{self.company_name} - cooperational status: {self.cooperational_status}"  # noqa


class Product(BaseModel, TranslatableModel):
    approved = models.BooleanField(default=False)
    show_cost = models.BooleanField(default=True)
    show_cost_in_uzs = models.BooleanField(default=True)
    show_supplier = models.BooleanField(default=True)
    translations = TranslatedFields(
        name=models.CharField(
            max_length=250, verbose_name="Name", blank=True, null=True
        ),
        short_description=models.TextField(
            null=True,
            blank=True,
            verbose_name="short description",
        ),
        description=RichTextField(
            verbose_name="Description",
            blank=True,
            null=True,
        ),
    )
    background_image = models.ForeignKey(
        "BackgroundBanner",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="category_products_set",
    )
    subcategory = models.ForeignKey(
        "SubCategory",
        on_delete=models.CASCADE,
        related_name="subcategory_products_set",
    )
    tags = models.CharField(max_length=500, default="", blank=True)
    min_price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    availability_status = models.IntegerField(
        default=1, choices=AVAILABILITY_STATUS_CHOISES
    )
    discount = models.IntegerField(default=0)
    cip_type = models.IntegerField(default=1, choices=CIP_STATUS_CHOISES)
    view_count = models.IntegerField(default=0)
    related_products = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name="Related Products (for sets or complects)",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        "CustomUser", on_delete=models.SET_NULL, null=True, blank=True
    )
    video_url = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def get_model_fields(cls):
        """
        Return a list of all fields of the Product model.
        """
        return [field.name for field in cls._meta.fields]

    def get_availability_status_display(self, lang_code="uz"):
        """Return the translated availability status."""
        status_translation = AVAILABILITY_STATUS_TRANSLATIONS.get(
            lang_code, AVAILABILITY_STATUS_TRANSLATIONS["uz"]
        )
        return status_translation.get(
            self.availability_status,
            "Unknown Status",
        )

    def __str__(self) -> str:
        return self.name_uz


class ProductFeature(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name="Title",
            null=True,
        ),
        value=models.CharField(
            max_length=250,
            verbose_name="Value",
            null=True,
        ),
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


class ProductPriceBasedOnModel(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
    )
    is_active = models.BooleanField(default=False)
    model = models.CharField(max_length=255)
    price = models.IntegerField()


class Order(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_orders"
    )
    description = models.TextField(null=True)
    notes = models.TextField(null=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOISES, default=1)
