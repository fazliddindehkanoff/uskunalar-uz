from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.views.selectors import product_detail, list_products


class ProductDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(
            product_detail(
                request=request,
                lang_code=lang_code,
                product_id=pk,
            )
        )


class ProductListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
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
        ],
        responses={200: "Successful response"},
    )
    def get(self, request):
        category_id = int(request.query_params.get("category_id", 0))
        sub_category_id = int(request.query_params.get("subcategory_id", 0))
        random = bool(request.query_params.get("random", False))
        order_by = request.query_params.get("order_by")
        query = request.query_params.get("search")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(
            list_products(
                request=request,
                lang_code=lang_code,
                random=random,
                category_id=category_id,
                sub_category_id=sub_category_id,
                order_by=order_by,
                search_query=query,
                page=page,
                page_size=page_size,
            )
        )
