from api.models import Category, SubCategory


def list_categories(lang_code):
    categories = Category.objects.all()
    category_data = [
        {
            "id": category.pk,
            "icon": category.icon.url if category.icon else "",
            "title": category.get_translated_field("title", lang_code),
            "product_count": category.category_products_set.count(),
        }
        for category in categories
    ]
    return category_data


def list_subcategories(lang_code):
    subcategories = SubCategory.objects.all()
    subcategory_data = [
        {
            "id": subcategory.pk,
            "category": (
                subcategory.category.get_translated_field("title", lang_code)
                if subcategory.category
                else ""
            ),
            "title": subcategory.get_translated_field("title", lang_code),
            "product_count": subcategory.category_products_set.count(),
        }
        for subcategory in subcategories
    ]
    return subcategory_data
