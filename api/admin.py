from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin, TabularInline

from api.models.product import ProductImage
from api.forms import CustomUserCreationForm
from .models import (
    Blog,
    CustomUser,
    Category,
    SubCategory,
    Product,
    ProductFeature,
    Banner,
    Partner,
    BackgroundBanner,
)

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    form = CustomUserCreationForm
    list_display = ("username", "first_name", "last_name", "is_staff", "is_active")


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ("title_uz", "title_en", "title_ru")


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("title_uz", "title_en", "title_ru")


@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_display = ("title_uz", "title_en", "title_ru")


class ProductFeatureAdmin(TabularInline):
    model = ProductFeature
    extra = 1


class ProductImageAdmin(TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    change_form_template = "admin/product_change_form.html"
    search_fields = ["pk", "name_uz", "name_en", "name_ru"]
    autocomplete_fields = [
        "related_products",
    ]

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_translate_button"] = True  # You can add conditions here
        return super().changeform_view(request, object_id, form_url, extra_context)

    def render_change_form(self, request, context, *args, **kwargs):
        context.update(
            {
                "show_translate_button": context.get("show_translate_button", False),
            }
        )
        return super().render_change_form(request, context, *args, **kwargs)

    def response_change(self, request, obj):
        if "_auto_translate" in request.POST:
            # Perform your translation logic here
            # Example:
            # for field in obj.translations.fields:
            #     translated_value = translate_field(obj, field)
            #     setattr(obj, f"{field}_en", translated_value)
            # obj.save()

            self.message_user(
                request, "Fields auto-filled with translations. Review before saving."
            )
            change_form_url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
                args=[obj.pk],
            )
            return HttpResponseRedirect(change_form_url)
        return super().response_change(request, obj)

    search_fields = ("name_uz", "name_en", "name_ru")
    list_display = ("name_uz", "name_en", "name_ru")
    inlines = [ProductFeatureAdmin, ProductImageAdmin]


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    pass


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = ("image",)


@admin.register(BackgroundBanner)
class BackgroundBannerAdmin(ModelAdmin):
    list_display = ("image",)
