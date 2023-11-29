from django.db import models

from config.models import BaseModel


class Tag(BaseModel):
    title = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.title
