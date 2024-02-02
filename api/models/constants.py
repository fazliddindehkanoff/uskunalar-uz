from django.db import models
from django.utils.translation import gettext_lazy as _


CIP_STATUS_CHOISES = [
    (1, "DAF"),
    (2, "EXW"),
    (3, "FCA"),
]

EDITOR_LANG_CHOICES = [
    (1, "Uzb"),
    (2, "Eng"),
    (3, "Rus"),
]

AVAILABILITY_STATUS_CHOISES = [
    (1, "Omborda mavjud"),
    (2, "Buyurtma orqali"),
]


AVAILABILITY_STATUS_TRANSLATIONS = {
    "en": {
        1: "In Stock",
        2: "By Order",
    },
    "ru": {
        1: "В наличии",
        2: "Под заказ",
    },
    "uz": {
        1: "Omborda mavjud",
        2: "Buyurtma orqali",
    },
}

COOPERATIONAL_STATUS_CHOICES = [
    (1, "Resume"),
    (2, "Pause"),
    (3, "Stop"),
]


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    EDITOR = "EDITOR", _("Editor")
