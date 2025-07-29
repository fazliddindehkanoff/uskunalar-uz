from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
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
        COPYWRITER = "COPYWRITER", _("Copywriter")

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
        elif self.role == (self.UserRole.EDITOR or self.UserRole.ADMIN):
            self.is_staff = True
            self.is_active = True
        super().save(*args, **kwargs)

    @hook("after_update")
    def set_user_permissions(self):
        if self.role == self.UserRole.ADMIN:
            self.user_permissions.set(Permission.objects.all())
        elif self.role == self.UserRole.EDITOR:
            group = Group.objects.get(pk=1)  # Assuming group ID 1 exists
            self.groups.set([group])
            print("User permissions set successfully.")
            print("User groups after assignment:", self.groups.all())


class JWTToken(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="token",
    )
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


class OTP(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    @property
    def is_expired(self):
        expiration_time = self.created_at + timezone.timedelta(minutes=5)
        current_time = timezone.now()

        return current_time >= expiration_time
