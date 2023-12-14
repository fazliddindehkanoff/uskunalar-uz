from rest_framework.views import APIView
from rest_framework.response import Response
from api.views.selectors import product_detail


class ProductDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")
        return Response(
            product_detail(request=request, lang_code=lang_code, product_id=pk)
        )
