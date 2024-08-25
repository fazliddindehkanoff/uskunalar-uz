from django.core.cache import cache

from api.models import Category, SubCategory
from api.models.category import LineCategory


def list_categories(lang_code, request):
    cache_key = f"list_categories_{lang_code}"
    categories_data = cache.get(cache_key)

    if not categories_data:
        categories = (
            Category.objects.filter(available=True)
            .prefetch_related("category_products_set")
            .order_by("order")
        )

        categories_data = [
            {
                "id": category.pk,
                "icon": (
                    request.build_absolute_uri(category.icon.url)
                    if category.icon
                    else ""
                ).replace("http://", "https://"),
                "title": category.get_translated_field("title", lang_code),
                "product_count": category.category_products_set.count(),
            }
            for category in categories
        ]

        cache.set(cache_key, categories_data, timeout=60 * 10)

    return categories_data


def list_subcategories(lang_code, request, category_id=None):
    cache_key = f"list_subcategories_{category_id}_{lang_code}"
    subcategories_data = cache.get(cache_key)

    if not subcategories_data:
        subcategories = (
            SubCategory.objects.filter(available=True)
            .select_related("category")
            .prefetch_related("subcategory_products_set")
        )

        if category_id:
            subcategories = subcategories.filter(category_id=category_id)

        subcategories_data = [
            {
                "id": subcategory.pk,
                "category": (
                    subcategory.category.get_translated_field(
                        "title",
                        lang_code,
                    )
                    if subcategory.category
                    else ""
                ),
                "icon": (
                    request.build_absolute_uri(subcategory.icon.url)
                    if subcategory.icon
                    else ""
                ).replace("http://", "https://"),
                "title": subcategory.get_translated_field("title", lang_code),
                "product_count": subcategory.subcategory_products_set.count(),
            }
            for subcategory in subcategories
        ]

        cache.set(cache_key, subcategories_data, timeout=60 * 10)

    return subcategories_data


def list_line_categories(lang_code):
    cache_key = f"list_line_categories_{lang_code}"
    line_categories_data = cache.get(cache_key)

    if not line_categories_data:
        line_categories = LineCategory.objects.prefetch_related("lines")

        line_categories_data = [
            {
                "id": category.pk,
                "title": category.get_translated_field("title", lang_code),
                "line_count": category.lines.count(),
            }
            for category in line_categories
        ]

        cache.set(cache_key, line_categories_data, timeout=60 * 10)

    return line_categories_data
