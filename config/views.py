from django.views.generic import RedirectView
from api.models import Product, Category, SubCategory


class HomeView(RedirectView):
    pattern_name = "admin:index"


def dashboard_callback(request, context):
    products = Product.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    approved_products_count = products.filter(approved=True).count()
    unapproved_products_count = products.filter(approved=False).count()
    available_categories_count = categories.filter(available=True).count()
    unavailable_categories_count = categories.filter(available=False).count()
    available_sub_categories_count = sub_categories.filter(
        available=True,
    ).count()
    unavailable_sub_categories_count = sub_categories.filter(
        available=False,
    ).count()

    context.update(
        {
            "kpi": [
                {
                    "title": "Number of products",
                    "metric": approved_products_count,
                    "footer": f"{unapproved_products_count} products hasn't been approved yet",  # noqa
                },
                {
                    "title": "Number of categories",
                    "metric": available_categories_count,
                    "footer": f"{unavailable_categories_count} categories are hidden",  # noqa
                },
                {
                    "title": "Number of Subcategories",
                    "metric": available_sub_categories_count,
                    "footer": f"{unavailable_sub_categories_count} subcategories are hidden",  # noqa
                },
            ],
            "approved_products": products.filter(
                approved=True,
            ).order_by(
                "-created_at"
            )[:5],
            "unapproved_products": products.filter(approved=False).order_by(
                "-created_at"
            )[:5],
        },
    )

    return context
