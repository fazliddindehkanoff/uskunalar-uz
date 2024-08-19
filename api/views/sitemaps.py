from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Product, Line, Work, Video
from api.utils import get_list_of_object_ids


class ProductSitemapApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(get_list_of_object_ids(Product, approved=True))


class LineSitemapApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(get_list_of_object_ids(Line))


class WorkSitemapApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(get_list_of_object_ids(Work))


class VideoSitemapApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(get_list_of_object_ids(Video))
