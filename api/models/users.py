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

    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.EDITOR
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

    @hook("before_create")
    def set_initial_values(self):
        self.is_staff = True
        self.is_active = True

    @hook("after_create")
    def set_user_permissions(self):
        if self.role == self.UserRole.ADMIN:
            # Give all permissions for admin panel
            self.user_permissions.set(Permission.objects.all())
        elif self.role == self.UserRole.EDITOR:
            # Give permissions for the Product model
            product_permissions = Permission.objects.filter(
                content_type__app_label="api", content_type__model="product"
            )
            product_image_permissions = Permission.objects.filter(
                content_type__app_label="api", content_type__model="product_image"
            )
            product_feature_permissions = Permission.objects.filter(
                content_type__app_label="api", content_type__model="product_feature"
            )

            # Combine the sets of permissions
            all_permissions = (
                product_permissions
                | product_image_permissions
                | product_feature_permissions
            )

            # Set all combined permissions
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
