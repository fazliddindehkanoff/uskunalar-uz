import os
import environ

from pathlib import Path
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests

from api.models import SMSCode
from api.utils import generate_code, send_sms

User = get_user_model()
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


class UserRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)


class UserVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    verification_code = serializers.CharField(max_length=6)


class UserRegistrationView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data["password"]
            user = User.objects.create_user(username=phone_number, password=password)
            code = generate_code()
            SMSCode.objects.create(code=code, user=user)
            send_sms(code, phone_number)
            return Response(
                {"user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserVerificationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        verification_code = serializer.validated_data["verification_code"]
        try:
            user = User.objects.get(username=phone_number)
            SMSCode.objects.get(user=user, code=verification_code)
        except SMSCode.DoesNotExist or User.DoesNotExist:
            return Response(
                {"error": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save()

        return Response(
            {"message": "User activated successfully.", "user_id": user.pk},
            status=status.HTTP_200_OK,
        )


class GoogleLoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.data.get("id_token")
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            env("GOOGLE_OAUTH_KEY"),
        )
        # TODO: Create or Update user using full name and email
        full_name = idinfo.get("name")
        email = idinfo.get("email")

        return Response({"ok": True})
