from drf_yasg import openapi

list_works_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "works": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "short_description": openapi.Schema(type=openapi.TYPE_STRING),
                        "image_url": openapi.Schema(type=openapi.TYPE_STRING),
                        "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
            ),
            "total_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page_size": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )
}

work_detail_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "short_description": openapi.Schema(type=openapi.TYPE_STRING),
            "long_description": openapi.Schema(type=openapi.TYPE_STRING),
            "image_url": openapi.Schema(type=openapi.TYPE_STRING),
            "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )
}
