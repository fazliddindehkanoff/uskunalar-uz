from django.db import models

from config.models import BaseModel


class Tag(BaseModel):
    title = models.CharField(max_length=250)
    # product = models.ForeignKey(
    #     "Product",
    #     on_delete=models.CASCADE,
    #     related_name="tags",
    #     null=True,
    #     blank=True,
    # )

    def __str__(self) -> str:
        return self.title
