from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import list_categories, list_subcategories


class CategoryListApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

        return Response(list_categories(lang_code))


class SubCategoryListApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

        return Response(list_subcategories(lang_code))
