from django.urls import path

from api.views import HomeAPIView, ProductDetailAPIView

urlpatterns = [
    path("home/", HomeAPIView.as_view()),
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
]
