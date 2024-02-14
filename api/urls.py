from django.urls import path

from api.views import ProductDetailAPIView, ProductListAPIView, BlogListAPIView

urlpatterns = [
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("blog/", BlogListAPIView.as_view()),
]
