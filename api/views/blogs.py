from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from .docs import (
    list_get_params,
    line_list_get_responses,
    line_detail_get_response,
    blog_detail_get_response,
    blog_list_get_responses,
    videos_list_get_response,
    videos_list_get_params,
)
from .selectors import (
    list_blog_posts,
    blog_post_detail,
    line_post_detail,
    list_line_posts,
    list_videos,
    video_detail,
)


class BlogListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=list_get_params, responses=blog_list_get_responses
    )
    def get(self, request):
        """
        List blog posts
        """
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

    @swagger_auto_schema(responses=blog_detail_get_response)
    def get(self, request, pk):
        """
        Retrieve a blog post
        """
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(
            blog_post_detail(
                lang_code=lang_code,
                blog_post_id=pk,
                request=request,
            )
        )


class LineListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=list_get_params,
        responses=line_list_get_responses,
    )
    def get(self, request):
        """
        List line posts
        """
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        search_query = request.query_params.get("search")
        data = list_line_posts(
            request,
            lang_code,
            page=page,
            page_size=page_size,
            search_query=search_query,
        )
        return Response(data)


class LineDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses=line_detail_get_response)
    def get(self, request, pk):
        """
        Retrieve a line post
        """
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(
            line_post_detail(
                lang_code=lang_code,
                line_post_id=pk,
                request=request,
            )
        )


class VideoListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=videos_list_get_params,
        responses=videos_list_get_response,
    )
    def get(self, request):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        data = list_videos(
            lang_code=lang_code,
            page=page,
            page_size=page_size,
        )
        return Response(data)


class VideoDetailApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(video_detail(lang_code=lang_code, video_id=pk))
