from django.urls import path

from api.views import HomeAPIView

urlpatterns = [
    path("home/", HomeAPIView.as_view()),
]
