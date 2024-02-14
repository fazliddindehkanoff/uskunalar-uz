from django.urls import path

from api.views import ProductDetailAPIView, ProductListAPIView, BlogListAPIView
from api.views.blogs import BlogDetailAPIView

urlpatterns = [
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    path("blog/<int:pk>/", BlogDetailAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("blog-posts/", BlogListAPIView.as_view()),
]
