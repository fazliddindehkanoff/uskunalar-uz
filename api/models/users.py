from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel, hook

from api.models.constants import EDITOR_LANG_CHOICES
from config.models import BaseModel


class CustomUser(AbstractUser, LifecycleModel):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        EDITOR = "EDITOR", _("Editor")
        USER = "USER", _("Foydalanuvchi")

    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.USER
    )
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    subcategory = models.ForeignKey(
        "SubCategory", on_delete=models.SET_NULL, null=True, blank=True
    )
    language = models.IntegerField(default=1, choices=EDITOR_LANG_CHOICES)

    def save(self, *args, **kwargs):
        if self.role == self.UserRole.ADMIN:
            self.category = None
            self.subcategory = None
        super().save(*args, **kwargs)

    @hook("after_create")
    def set_user_permissions(self):
        self.is_staff = True
        self.is_active = True
        if self.role == self.UserRole.ADMIN:
            self.user_permissions.set(Permission.objects.all())
        elif self.role == self.UserRole.EDITOR:
            product_permissions = Permission.objects.filter(
                content_type__app_label="api", content_type__model="product"
            )
            product_image_permissions = Permission.objects.filter(
                content_type__app_label="api", content_type__model="product_image"
            )
            product_feature_permissions = Permission.objects.filter(
                content_type__app_label="api", content_type__model="product_feature"
            )
            all_permissions = list(
                product_permissions
                | product_image_permissions
                | product_feature_permissions
            )
            self.user_permissions.set(all_permissions)


class JWTToken(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="token")
    access_token = models.TextField()
    is_active = models.BooleanField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}'s JWT Token"

    def is_expired(self):
        return timezone.now() > self.expiration_date


class SMSCode(BaseModel):
    code = models.IntegerField()
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sms_codes"
    )
