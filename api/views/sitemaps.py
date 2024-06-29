from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Product, Line, Work, Video
from api.utils import get_list_of_object_ids


class ProductSitemapApiView(APIView):
    def get(self, request):
        return Response(get_list_of_object_ids(Product, approved=True))


class LineSitemapApiView(APIView):
    def get(self, request):
        return Response(get_list_of_object_ids(Line))


class WorkSitemapApiView(APIView):
    def get(self, request):
        return Response(get_list_of_object_ids(Work))


class VideoSitemapApiView(APIView):
    def get(self, request):
        return Response(get_list_of_object_ids(Video))
