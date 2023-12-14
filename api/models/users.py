from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


from config.models import BaseModel


class CustomUser(AbstractUser):
    pass


class JWTToken(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="token")
    access_token = models.TextField()
    is_active = models.BooleanField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}'s JWT Token"

    def is_expired(self):
        return timezone.now() > self.expiration_date
