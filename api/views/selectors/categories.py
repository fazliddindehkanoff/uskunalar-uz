from api.models import Category, SubCategory
from api.models.category import LineCategory


def list_categories(lang_code, request):
    categories = Category.objects.all()
    category_data = [
        {
            "id": category.pk,
            "icon": (
                request.build_absolute_uri(category.icon.url) if category.icon else ""
            ),
            "title": category.get_translated_field("title", lang_code),
            "product_count": category.category_products_set.count(),
        }
        for category in categories
    ]
    return category_data


def list_subcategories(lang_code, request, category_id=None):
    subcategories = SubCategory.objects.all()

    if category_id:
        subcategories = subcategories.filter(category_id=category_id)

    subcategory_data = [
        {
            "id": subcategory.pk,
            "category": (
                subcategory.category.get_translated_field("title", lang_code)
                if subcategory.category
                else ""
            ),
            "icon": (
                request.build_absolute_uri(subcategory.icon.url)
                if subcategory.icon
                else ""
            ),
            "title": subcategory.get_translated_field("title", lang_code),
            "product_count": subcategory.subcategory_products_set.count(),
        }
        for subcategory in subcategories
    ]
    return subcategory_data


def list_line_categories(lang_code):
    line_category = LineCategory.objects.all()
    category_data = [
        {
            "id": category.pk,
            "title": category.get_translated_field("title", lang_code),
            "line_count": category.lines.count(),
        }
        for category in line_category
    ]
    return category_data
