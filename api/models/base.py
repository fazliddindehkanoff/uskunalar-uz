from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Iterate over the available languages and create translated fields
        for lang_code, lang_name in settings.LANGUAGES:
            for field_name in self._translated_fields:
                base_field = getattr(self, field_name)
                translated_field_name = f"{field_name}_{lang_code}"
                translated_field = base_field.clone()
                translated_field.verbose_name = (
                    f"{base_field.verbose_name} ({lang_name})"
                )
                setattr(self, translated_field_name, translated_field)


class TranslatedFields:
    def __init__(self, *args):
        self.fields = args

    def contribute_to_class(self, cls, name):
        # Attach the translated fields to the class
        cls._translated_fields = self.fields
