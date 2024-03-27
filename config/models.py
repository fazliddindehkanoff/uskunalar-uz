from django.db import models


class BaseModel(models.Model):
    translated_fields = []
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
