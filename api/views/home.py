from rest_framework.views import APIView
from rest_framework.response import Response
from api.views.selectors import get_home_page_data


class HomeAPIView(APIView):
    def get(self, request):
        return Response(get_home_page_data("uz"))
