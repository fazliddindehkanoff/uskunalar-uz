from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from googletrans import Translator

from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from unfold.decorators import display

from .models.constants import EDITOR_LANG_CHOICES
from .models import (
    Blog,
    CustomUser,
    Category,
    SubCategory,
    Product,
    ProductFeature,
    Banner,
    PartnerLogos,
    BackgroundBanner,
    Supplier,
    ProductImage,
    Order,
)

admin.site.unregister(Group)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["user", "product", "status"]


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "first_name", "last_name", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("category", "subcategory"),
                    "language",
                    "role",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    readonly_fields = ["last_login", "date_joined"]

    @display(description=_("User"), header=True)
    def display_header(self, instance: CustomUser):
        return instance.full_name, instance.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: CustomUser):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: CustomUser):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: CustomUser):
        return instance.created_at


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ("title_uz", "title_en", "title_ru")


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ("company_name", "experience")


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
    # change_form_template = "admin/product_change_form.html"
    search_fields = ["pk", "name_uz", "name_en", "name_ru"]
    autocomplete_fields = [
        "related_products",
    ]
    exclude = ("created_by",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == "EDITOR":
            qs = qs.filter(created_by=request.user)
        return qs

    def get_form(self, request, obj: Product = None, **kwargs):
        excluded_fields = list(self.exclude) if self.exclude else []

        if request.user.role == "EDITOR":
            excluded_languages = ["_uz", "_ru", "_en"]
            additional_fields_to_exclude = [
                "category",
                "subcategory",
                "approved",
                "view_count",
            ]
            user_language_suffix = f"_{request.user.get_language_display()}"
            obj = obj if obj else Product
            for field in obj.translated_fields:
                for lang_suffix in excluded_languages:
                    if field.endswith(lang_suffix) and not field.endswith(
                        user_language_suffix
                    ):
                        additional_fields_to_exclude.append(field)
            excluded_fields.extend(additional_fields_to_exclude)

        kwargs["exclude"] = excluded_fields
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user

        if not obj.pk and request.user.role == "EDITOR":
            obj.category_id = request.user.category.id
            obj.subcategory_id = request.user.subcategory.pk

        user_language = request.user.language
        translator = Translator()
        for field in obj._meta.fields:
            if field.name != "id":
                field_name = str(field.name)
                for lang_code, lang_name in EDITOR_LANG_CHOICES:
                    if lang_code != user_language and field_name.endswith(lang_name):
                        try:

                            translated_value = translator.translate(
                                getattr(
                                    obj,
                                    field_name[:-2]
                                    + request.user.get_language_display(),
                                ),
                                src=request.user.get_language_display(),
                                dest=lang_name,
                            ).text
                        except Exception as e:
                            print(e)
                            translated_value = "TEST"
                        print(translated_value)
                        setattr(obj, field.name, translated_value)

        # Call the parent save_model method to save the object
        super().save_model(request, obj, form, change)

    search_fields = ("name_uz", "name_en", "name_ru")
    list_display = ("name_uz", "name_en", "name_ru")
    inlines = [ProductFeatureAdmin, ProductImageAdmin]


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    pass


@admin.register(PartnerLogos)
class PartnerLogoAdmin(ModelAdmin):
    list_display = ("image",)


@admin.register(BackgroundBanner)
class BackgroundBannerAdmin(ModelAdmin):
    list_display = ("image",)
