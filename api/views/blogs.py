from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import get_blog_posts_list, get_blog_detail, list_blog_posts


class BlogListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        search_query = request.query_params.get("search")
        data = list_blog_posts(
            request,
            lang_code,
            page=page,
            page_size=page_size,
            search_query=search_query,
        )
        return Response(data)
