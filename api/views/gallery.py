from rest_framework.views import APIView
from rest_framework.response import Response
from api.views.selectors.galleries import (
    get_list_of_galleries,
    get_gallery_detail,
)


class GalleryListView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(
        self,
        request,
        order_by="created_at",
        page=1,
        page_size=10,
    ):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        galleries_data = get_list_of_galleries(
            request, lang_code, order_by, page, page_size
        )
        return Response(galleries_data)


class GalleryDetailView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, gallery_id):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        gallery_data = get_gallery_detail(gallery_id, request, lang_code)
        return Response(gallery_data)
