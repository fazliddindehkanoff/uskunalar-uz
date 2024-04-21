from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import work_detail, list_works


class WorkListAPIView(APIView):
    def get(self, request):
        order_by = request.query_params.get("order_by")
        query = request.query_params.get("search")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

        works = list_works(
            request,
            lang_code=lang_code,
            search_query=query,
            order_by=order_by,
            page=page,
            page_size=page_size,
        )

        return Response(works)


class WorkDetailAPIView(APIView):
    def get(self, request, pk):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

        work_data = work_detail(lang_code=lang_code, work_id=pk, request=request)
        return Response(work_data)
