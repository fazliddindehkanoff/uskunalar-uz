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

list_products_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "products": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "price_in_usd": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "price_in_uzs": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "has_discount": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "discount_percentage": openapi.Schema(
                            type=openapi.TYPE_INTEGER
                        ),
                        "price_with_discount_in_usd": openapi.Schema(
                            type=openapi.TYPE_NUMBER
                        ),
                        "price_with_discount_in_uzs": openapi.Schema(
                            type=openapi.TYPE_NUMBER
                        ),
                        "images": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "background_image": openapi.Schema(type=openapi.TYPE_STRING),
                        "cip_type": openapi.Schema(type=openapi.TYPE_STRING),
                        "availability_status_readable": openapi.Schema(
                            type=openapi.TYPE_STRING
                        ),
                        "availability_status": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_new": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "specifications": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                        ),
                    },
                ),
            ),
            "total_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page_size": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )
}


product_detail_response = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "price_in_usd": openapi.Schema(type=openapi.TYPE_NUMBER),
            "price_in_uzs": openapi.Schema(type=openapi.TYPE_NUMBER),
            "has_discount": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "discount_percentage": openapi.Schema(type=openapi.TYPE_INTEGER),
            "price_with_discount_in_usd": openapi.Schema(type=openapi.TYPE_NUMBER),
            "price_with_discount_in_uzs": openapi.Schema(type=openapi.TYPE_NUMBER),
            "images": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
            ),
            "background_image": openapi.Schema(type=openapi.TYPE_STRING),
            "specifications": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "value": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "short_description": openapi.Schema(type=openapi.TYPE_STRING),
            "category": openapi.Schema(type=openapi.TYPE_STRING),
            "subcategory": openapi.Schema(type=openapi.TYPE_STRING),
            "availability_status": openapi.Schema(type=openapi.TYPE_STRING),
            "discount": openapi.Schema(type=openapi.TYPE_INTEGER),
            "cip_type": openapi.Schema(type=openapi.TYPE_STRING),
            "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "related_products": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "price_in_usd": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "price_in_uzs": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "images": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            ),
            "similar_products": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "price_in_usd": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "price_in_uzs": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "images": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                    },
                ),
            ),
            "supplier": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "address": openapi.Schema(type=openapi.TYPE_STRING),
                    "contact_number": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}
