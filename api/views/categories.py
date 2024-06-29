from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import (
    list_categories,
    list_subcategories,
    list_line_categories,
)


class CategoryListApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

        return Response(list_categories(lang_code, request))


class SubCategoryListApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        category_id = request.query_params.get("category_id", None)

        return Response(list_subcategories(lang_code, request, category_id))


class LineCategoryListApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

        return Response(list_line_categories(lang_code, request))
