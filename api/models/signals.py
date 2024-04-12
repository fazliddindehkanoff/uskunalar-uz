from django.db.models.signals import pre_save
from django.dispatch import receiver
from googletrans import Translator

from api.models.product import ProductFeature


@receiver(pre_save, sender=ProductFeature)
def translate_blank_fields(sender, instance, **kwargs):
    if instance._state.adding:
        translator = Translator()
        for field_name in instance.translated_fields:
            try:
                value = getattr(instance, field_name)
                if not value:
                    source_lang = "en"
                    dest_lang = field_name.split("_")[
                        -1
                    ]  # Extract language code from field name
                    filled_field_name = field_name.replace(
                        f"_{dest_lang}", f"_{source_lang}"
                    )
                    filled_value = getattr(instance, filled_field_name)
                    if filled_value:
                        translated_value = translator.translate(
                            filled_value, src=source_lang, dest=dest_lang
                        ).text
                        setattr(instance, field_name, translated_value)
            except Exception:
                pass
