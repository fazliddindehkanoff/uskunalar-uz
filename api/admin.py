from collections.abc import Sequence
from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from adminsortable2.admin import SortableAdminMixin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import (
    UserCreationForm,
    UserChangeForm,
    AdminPasswordChangeForm,
)
from unfold.decorators import display

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
    Work,
    Line,
    LineCategory,
    Video,
)


class UnapprovedProduct(Product):
    class Meta:
        proxy = True
        verbose_name = "Unapproved Product"
        verbose_name_plural = "Unapproved Products"


@admin.register(Work)
class WorkAdmin(ModelAdmin):
    list_display = ("id", "title_uz")


@admin.register(Line)
class LineAdmin(ModelAdmin):
    list_display = ("id", "title_uz")


@admin.register(LineCategory)
class LineCategoryAdmin(ModelAdmin):
    list_display = ("id", "title_uz")


@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ("id", "title_uz")


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["user", "product", "status"]


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
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
    search_fields = ["company_name"]
    list_display = ("company_name", "experience")


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ("id", "title_uz", "order")


@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_display = ("id", "category", "title_uz")


@admin.register(ProductFeature)
class ProductFeatureAdmin(ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    pass


class ProductFeatureInlineAdmin(TabularInline):
    model = ProductFeature
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super().get_formset(request, obj, **kwargs)
        if request.user.role == "EDITOR":
            user_language_suffix = f"_{request.user.get_language_display()}"
            formset_class.form.base_fields = {
                field: formset_class.form.base_fields[field]
                for field in formset_class.form.base_fields
                if field.endswith(user_language_suffix)
            }
        return formset_class


class ProductImageInlineAdmin(TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    search_fields = [
        "pk",
        "name_uz",
        "name_en",
        "name_ru",
    ]
    autocomplete_fields = [
        "related_products",
        "supplier",
    ]
    exclude = ("created_by",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if "change" in request.path and request.resolver_match.kwargs.get(
            "object_id",
        ):
            return qs

        if request.user.role == "EDITOR":
            qs = qs.filter(created_by=request.user)

        if (
            request.user.is_superuser
            and request.GET.get(
                "approved__exact",
            )
            is None
        ):
            qs = qs.filter(approved=True)

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
                "supplier",
                "background_image",
            ]
            user_language_suffix = f"_{request.user.get_language_display()}"
            obj = obj if obj else Product
            for field in obj.translated_fields:
                if field.endswith(user_language_suffix):
                    continue

                for lang_suffix in excluded_languages:
                    if field.endswith(lang_suffix):
                        additional_fields_to_exclude.append(field)
            excluded_fields.extend(additional_fields_to_exclude)

        kwargs["exclude"] = excluded_fields
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user

        if not obj.pk and request.user.role == "EDITOR":
            obj.category_id = request.user.category.id
            obj.subcategory_id = request.user.subcategory.pk

        super().save_model(request, obj, form, change)

    list_display = [
        "id",
        "name_uz",
        "category",
        "approved",
    ]

    def get_list_display(self, request: HttpRequest) -> Sequence[str]:
        list_display = super().get_list_display(request)
        if request.user.is_superuser and "created_by" not in list_display:
            list_display.append("created_by")

        return list_display

    inlines = [ProductFeatureInlineAdmin, ProductImageInlineAdmin]


@admin.register(UnapprovedProduct)
class UnapprovedProductAdmin(ModelAdmin):
    search_fields = ["pk", "name_uz", "name_en", "name_ru"]
    autocomplete_fields = [
        "related_products",
    ]
    exclude = ("created_by",)

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(approved=False)
        return qs

    list_display = [
        "id",
        "name_uz",
        "category",
        "approved",
    ]

    def get_list_display(self, request: HttpRequest) -> Sequence[str]:
        list_display = super().get_list_display(request)
        if request.user.is_superuser and "created_by" not in list_display:
            list_display.append("created_by")

        return list_display

    inlines = [ProductFeatureInlineAdmin, ProductImageInlineAdmin]


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ("id", "banner_image_uz")


@admin.register(PartnerLogos)
class PartnerLogoAdmin(ModelAdmin):
    list_display = ("id", "image")


@admin.register(BackgroundBanner)
class BackgroundBannerAdmin(ModelAdmin):
    list_display = ("id", "title", "image")
