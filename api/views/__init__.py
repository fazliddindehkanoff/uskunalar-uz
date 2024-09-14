from .authentication import (  # noqa
    UserRegistrationView,
    UserVerificationView,
    GoogleLoginAPIView,
    LoginView,
)
from .banners import BannerListApiView  # noqa
from .blogs import (  # noqa
    BlogListAPIView,
    BlogDetailAPIView,
    LineListAPIView,
    LineDetailAPIView,
    VideoListAPIView,
    VideoDetailApiView,
)
from .categories import (  # noqa
    CategoryListApiView,
    SubCategoryListApiView,
    LineCategoryListApiView,
)
from .products import ProductDetailAPIView, ProductListAPIView  # noqa
from .partners import PartnersLogoListAPIView  # noqa
from .works import WorkDetailAPIView, WorkListAPIView  # noqa
from .sitemaps import (  # noqa
    LineSitemapApiView,
    ProductSitemapApiView,
    VideoSitemapApiView,
    WorkSitemapApiView,
)
from .gallery import GalleryListView, GalleryDetailView  # noqa
