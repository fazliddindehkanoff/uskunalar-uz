from django.urls import path

from api.views import (
    ProductDetailAPIView,
    ProductListAPIView,
    BlogListAPIView,
    BlogDetailAPIView,
    PartnersLogoListAPIView,
    CategoryListApiView,
    UserVerificationView,
    UserRegistrationView,
    GoogleLoginAPIView,
)

urlpatterns = [
    path("partner-logos/", PartnersLogoListAPIView.as_view()),
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    path("blog/<int:pk>/", BlogDetailAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("categories/", CategoryListApiView.as_view()),
    path("blog-posts/", BlogListAPIView.as_view()),
    path("auth/register/", UserRegistrationView.as_view()),
    path("auth/phone-verification/", UserVerificationView.as_view()),
    path("auth/google/", GoogleLoginAPIView.as_view(), name="google_login"),
]
