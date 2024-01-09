from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TranslatedFields:
    def __init__(self, **kwargs):
        self.fields = kwargs

    def contribute_to_class(self, cls, name):
        for field_name, field in self.fields.items():
            for lang_code, lang_name in settings.LANGUAGES:
                translated_field_name = f"{field_name}_{lang_code}"
                translated_field = field.clone()
                translated_field.verbose_name = f"{field.verbose_name} ({lang_name})"
                cls.add_to_class(translated_field_name, translated_field)


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    def get_translated_field(self, field_name, lang_code=None):
        lang_code = lang_code
        translated_field_name = f"{field_name}_{lang_code}"
        value = getattr(self, translated_field_name, None)
        if not value:
            lang_code = settings.DEFAULT_LANGUAGE
            translated_field_name = f"{field_name}_{lang_code}"
            value = getattr(self, translated_field_name, None)

        return value
