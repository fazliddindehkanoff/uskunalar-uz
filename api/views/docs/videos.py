from drf_yasg import openapi

videos_list_get_response = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "videos": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                        "video_link": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            "total_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page": openapi.Schema(type=openapi.TYPE_INTEGER),
            "page_size": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )
}


videos_list_get_params = [
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
]
