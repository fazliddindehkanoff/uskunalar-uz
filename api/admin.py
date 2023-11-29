from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Blog,
    CustomUser,
    Category,
    SubCategory,
    Product,
    Tag,
    ProductFeature,
)

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
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


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name_uz", "name_en", "name_ru")
    inlines = [
        ProductFeatureAdmin,
    ]


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("title",)
