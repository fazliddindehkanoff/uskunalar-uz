from rest_framework.response import Response
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests


class GoogleLoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.data.get("id_token")
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            "215605722722-6rlk671c8391hno3cj0duvhs57qtsmm7.apps.googleusercontent.com",
        )
        # TODO: Create or Update user using full name and email
        full_name = idinfo.get("name")
        email = idinfo.get("email")

        return Response({"ok": True})
