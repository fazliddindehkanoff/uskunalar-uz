from datetime import timedelta
import os
import environ

from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG") == "1"
SITE_ID = 1
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    # unfold admin stuff
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    # django built in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # external apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "mdeditor",
    "drf_yasg",
    "ckeditor",
    "ckeditor_uploader",
    "adminsortable2",
    "django_ckeditor_5",
    # local apps
    "api",
]

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",  # Use the full toolbar configuration
        "versionCheck": False,  # Disable version check
        "extraPlugins": ",".join(
            [
                "uploadimage",  # Enable image uploading
            ]
        ),
        # "removePlugins": "image",  # Remove default image plugin
        "filebrowserUploadUrl": "/ckeditor/upload/",  # URL for file uploads
        "filebrowserImageUploadUrl": "/ckeditor/upload/",
    },
}

X_FRAME_OPTIONS = "SAMEORIGIN"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
CSRF_TRUSTED_ORIGINS = [
    "https://admin.uskunalar.uz",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://uskunalar.uz",
    "https://www.uskunalar.uz",
    "https://uskunalaruz.netlify.app",
]

CORS_ALLOW_HEADERS = [
    "Accept-Language",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "api.CustomUser"
LANGUAGES = [
    ("en", _("English")),
    ("uz", _("Uzbek")),
    ("ru", _("Russian")),
]
DEFAULT_LANGUAGE = "uz"

UNFOLD = {
    "SITE_TITLE": "Uskunalar.uz",
    "SITE_HEADER": "  ",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("logo.png"),
    "SITE_SYMBOL": "speed",
    "THEME": "light",
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
    "DASHBOARD_CALLBACK": "config.views.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:api_customuser_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Products"),
                        "icon": "box",
                        "link": lambda request: reverse_lazy(
                            "admin:api_product_changelist"
                        ),
                        "badge": "api.utils.get_number_of_products",
                    },
                    {
                        "title": _("Unapproved Products"),
                        "icon": "pending_actions",
                        "link": lambda request: reverse_lazy(
                            "admin:api_unapprovedproduct_changelist"
                        ),
                        "badge": "api.utils.get_number_of_unapproved_products",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:api_category_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Subcategories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:api_subcategory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Suppliers"),
                        "icon": "store",
                        "link": reverse_lazy("admin:api_supplier_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Blogs"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Blog"),
                        "icon": "article",
                        "link": reverse_lazy("admin:api_blog_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Videos"),
                        "icon": "video_library",
                        "link": reverse_lazy("admin:api_video_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Works"),
                        "icon": "work",
                        "link": reverse_lazy("admin:api_work_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Galleries"),
                        "icon": "photo",
                        "link": reverse_lazy("admin:api_gallery_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Linyalar"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Lines"),
                        "icon": "list",
                        "link": reverse_lazy("admin:api_line_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Line Categories"),
                        "icon": "list",
                        "link": reverse_lazy("admin:api_linecategory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Banners"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Banners"),
                        "icon": "image",
                        "link": reverse_lazy("admin:api_banner_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Background Banners"),
                        "icon": "image",
                        "link": reverse_lazy("admin:api_backgroundbanner_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Partner Logos"),
                        "icon": "image",
                        "link": reverse_lazy("admin:api_partnerlogos_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
}

X_FRAME_OPTIONS = "SAMEORIGIN"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)
