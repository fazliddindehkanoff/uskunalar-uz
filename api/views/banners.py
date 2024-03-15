from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import list_banners


class BannerListApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(list_banners(request))
