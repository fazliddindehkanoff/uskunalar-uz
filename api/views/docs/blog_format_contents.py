from drf_yasg import openapi

list_get_params = [
    openapi.Parameter(
        "page",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description="Page number",
        default=1,
    ),
    openapi.Parameter(
        "page_size",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description="Page size",
        default=10,
    ),
    openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description="Search query",
    ),
]

line_detail_get_response = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "price": openapi.Schema(type=openapi.TYPE_INTEGER),
            "category": openapi.Schema(type=openapi.TYPE_STRING),
            "short_description": openapi.Schema(type=openapi.TYPE_STRING),
            "long_description": openapi.Schema(type=openapi.TYPE_STRING),
            "img_url": openapi.Schema(type=openapi.TYPE_STRING),
            "banner_url": openapi.Schema(type=openapi.TYPE_STRING),
            "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "created_at": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
}


line_list_get_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "line_posts": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "image": openapi.Schema(type=openapi.TYPE_STRING),
                        "banner": openapi.Schema(type=openapi.TYPE_STRING),
                        "category": openapi.Schema(type=openapi.TYPE_STRING),
                        "short_description": openapi.Schema(type=openapi.TYPE_STRING),
                        "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            "total_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page_size": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )
}

blog_detail_get_response = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "cover_url": openapi.Schema(type=openapi.TYPE_STRING),
            "content": openapi.Schema(type=openapi.TYPE_STRING),
            "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "created_at": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
}


blog_list_get_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "blog_posts": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "cover_url": openapi.Schema(type=openapi.TYPE_STRING),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                        "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            "total_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page_size": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )
}
