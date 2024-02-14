from api.models import Category


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
