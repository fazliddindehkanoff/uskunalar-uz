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
    BannerListApiView,
)

urlpatterns = [
    path("auth/register/", UserRegistrationView.as_view()),
    path("auth/phone-verification/", UserVerificationView.as_view()),
    path("auth/google/", GoogleLoginAPIView.as_view(), name="google_login"),
    path("banners/", BannerListApiView.as_view()),
    path("blog-posts/", BlogListAPIView.as_view()),
    path("blog-post/<int:pk>/", BlogDetailAPIView.as_view()),
    path("categories/", CategoryListApiView.as_view()),
    path("partner-logos/", PartnersLogoListAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    path("sub_categories/", CategoryListApiView.as_view()),
]
