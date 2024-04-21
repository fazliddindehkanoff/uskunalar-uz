from drf_yasg import openapi

products_list_get_params = [
    openapi.Parameter(
        "category_id",
        openapi.IN_QUERY,
        description="Category ID",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "subcategory_id",
        openapi.IN_QUERY,
        description="Subcategory ID",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "order_by",
        openapi.IN_QUERY,
        description="Order by field default(view_count)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        description="Search query",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "page",
        openapi.IN_QUERY,
        description="Page number",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "page_size",
        openapi.IN_QUERY,
        description="Number of items per page",
        type=openapi.TYPE_INTEGER,
    ),
]
