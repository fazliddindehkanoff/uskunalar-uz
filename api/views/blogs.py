from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import list_blog_posts, blog_post_detail


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


class BlogDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(
            blog_post_detail(
                lang_code=lang_code,
                blog_post_id=pk,
                request=request,
            )
        )
