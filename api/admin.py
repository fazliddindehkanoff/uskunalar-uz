from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from unfold.decorators import action, display

from api.models.product import ProductImage
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
    Supplier,
)

admin.site.unregister(Group)


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

    def get_form(self, request, obj=None, **kwargs):
        excluded_fields = list(self.exclude) if self.exclude else []
        if request.user.role == "EDITOR":
            additional_fields_to_exclude = [
                "category",
                "subcategory",
            ]
            excluded_fields.extend(additional_fields_to_exclude)

        kwargs["exclude"] = excluded_fields
        return super().get_form(request, obj, **kwargs)

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

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.category_id = request.user.category.id
            obj.subcategory_id = request.user.subcategory.pk
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

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
