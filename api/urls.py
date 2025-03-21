from django.urls import path

from api.views import (
    ProductDetailAPIView,
    ProductListAPIView,
    BlogListAPIView,
    BlogDetailAPIView,
    PartnersLogoListAPIView,
    CategoryListApiView,
    SubCategoryListApiView,
    UserVerificationView,
    UserRegistrationView,
    GoogleLoginAPIView,
    BannerListApiView,
    LineListAPIView,
    LineDetailAPIView,
    LineCategoryListApiView,
    VideoListAPIView,
    VideoDetailApiView,
    WorkListAPIView,
    WorkDetailAPIView,
    LoginView,
    WorkSitemapApiView,
    LineSitemapApiView,
    ProductSitemapApiView,
    VideoSitemapApiView,
    GalleryListView,
    GalleryDetailView,
    ProductDetailTestAPIView,
    ProductListTestAPIView,
)

urlpatterns = [
    path("auth/register/", UserRegistrationView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/phone-verification/", UserVerificationView.as_view()),
    path("auth/google/", GoogleLoginAPIView.as_view(), name="google_login"),
    path("banners/", BannerListApiView.as_view()),
    path("blog-posts/", BlogListAPIView.as_view()),
    path("blog-posts/<int:pk>/", BlogDetailAPIView.as_view()),
    path("line-posts/", LineListAPIView.as_view()),
    path("line-posts/<int:pk>/", LineDetailAPIView.as_view()),
    path("categories/", CategoryListApiView.as_view()),
    path("sub-categories/", SubCategoryListApiView.as_view()),
    path("line-categories/", LineCategoryListApiView.as_view()),
    path("partner-logos/", PartnersLogoListAPIView.as_view()),
    path("videos/", VideoListAPIView.as_view()),
    path("videos/<int:pk>/", VideoDetailApiView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("products/<str:pk>/", ProductDetailAPIView.as_view()),
    path("products-test/", ProductListTestAPIView.as_view()),
    path("products-test/<str:pk>/", ProductDetailTestAPIView.as_view()),
    path("works/", WorkListAPIView.as_view()),
    path("works/<int:pk>/", WorkDetailAPIView.as_view()),
    path("sitemaps/products/", ProductSitemapApiView.as_view()),
    path("sitemaps/lines/", LineSitemapApiView.as_view()),
    path("sitemaps/works/", WorkSitemapApiView.as_view()),
    path("sitemaps/videos/", VideoSitemapApiView.as_view()),
    path("galleries/", GalleryListView.as_view()),
    path("galleries/<int:gallery_id>/", GalleryDetailView.as_view()),
]
