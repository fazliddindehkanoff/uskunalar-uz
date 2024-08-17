import json
import random

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView


class HomeView(RedirectView):
    pattern_name = "admin:index"


def dashboard_callback(request, context):

    context.update(
        {
            "kpi": [
                {
                    "title": "Number of products",
                    "metric": "12345",
                    "footer": "23 products hasn't been approved yet",
                },
                {
                    "title": "Number of categories",
                    "metric": "452",
                    "footer": "12 categories are hidden",
                },
                {
                    "title": "Number of lines",
                    "metric": "243",
                    "footer": "23 lines are hidden",
                },
            ],
            "model_counts": [
                {
                    "title": "Products",
                    "count": 12345,
                },
                {
                    "title": "Users",
                    "count": 12345,
                },
                {
                    "title": "Orders",
                    "count": 12345,
                },
                {
                    "title": "Categories",
                    "count": 12345,
                },
            ],
            "table_data": {
                "headers": ["col 1", "col 2"],
                "rows": [
                    ["a", "b"],
                    ["c", "d"],
                ],
            },
            "progress": [
                {
                    "title": "Social marketing e-book",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Freelancing tasks",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Development coaching",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Product consulting",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Other income",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
            ],
        },
    )

    return context
