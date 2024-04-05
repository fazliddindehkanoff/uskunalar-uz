from api.models import Category, SubCategory


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


def list_subcategories(lang_code, request):
    subcategories = SubCategory.objects.all()
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
            "product_count": subcategory.category_products_set.count(),
        }
        for subcategory in subcategories
    ]
    return subcategory_data
