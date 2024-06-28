from random import sample
from datetime import timedelta

from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.core.cache import cache

from api.models import Product
from api.utils import get_currency_rate, paginate_queryset
from .suppliers import get_supplier_data


def _calc_product_cost(product: Product, currency_rate, in_uzs=False) -> str:
    if in_uzs:
        currency_symbol = ""
    else:
        currency_rate = 1
        currency_symbol = "$"

    if product.price and product.price != 0:
        return f"{currency_symbol}{product.price * currency_rate:,}"
    elif product.min_price is not None and product.max_price is not None:
        try:
            return f"{currency_symbol}{product.min_price * currency_rate:,} - {currency_symbol}{product.max_price * currency_rate:,}"  # noqa
        except Exception:
            return f"there is an error with id:{product.pk}"
    return ""


def discount_calc(price: int, discount: int) -> int:
    return price - (price * discount) // 100


def _calc_product_cost_with_disc(
    product: Product,
    currency_rate,
    in_uzs=False,
) -> str:
    discount = product.discount
    currency_rate = currency_rate if in_uzs else 1
    currency_symbol = "" if in_uzs else "$"

    if discount > 0:
        if product.price and product.price != 0:
            return f"{currency_symbol}{discount_calc(product.price * currency_rate, discount):,}"  # noqa
        else:
            return f"{currency_symbol}{discount_calc(product.min_price * currency_rate, discount):,} - {currency_symbol}{discount_calc(product.max_price * currency_rate, discount):,}"  # noqa
    return ""


def product_detail(
    request,
    lang_code: str,
    product_id: int,
) -> dict:
    cache_key = f"product_detail_{product_id}_{lang_code}"
    product_data = cache.get(cache_key)

    if not product_data:
        currency_rate = get_currency_rate()
        product = (
            Product.objects.select_related(
                "category", "subcategory", "background_image"
            )
            .prefetch_related("images", "specifications", "related_products")
            .filter(pk=product_id)
            .first()
        )

        if not product:
            raise NotFound("There is no product with given id")

        product.view_count += 1
        product.save()

        product_data = {
            "id": product.pk,
            "price_in_usd": _calc_product_cost(
                product=product, currency_rate=currency_rate
            ),
            "price_in_uzs": _calc_product_cost(product=product, in_uzs=True),
            "has_discount": product.discount > 0,
            "discount_persentage": product.discount,
            "price_with_discount_in_usd": _calc_product_cost_with_disc(
                product=product, currency_rate=currency_rate
            ),
            "price_with_discount_in_uzs": _calc_product_cost_with_disc(
                product=product, in_uzs=True, currency_rate=currency_rate
            ),
            "images": [
                request.build_absolute_uri(image.image.url)
                for image in product.images.all()
            ],
            "background_image": (
                request.build_absolute_uri(product.background_image.image.url)
                if product.background_image
                else ""
            ),
            "specifications": [
                {
                    "title": feature.get_translated_field("title", lang_code),
                    "value": feature.get_translated_field("value", lang_code),
                }
                for feature in product.specifications.all()
            ],
            "name": product.get_translated_field("name", lang_code),
            "description": product.get_translated_field(
                "description",
                lang_code,
            ),
            "short_description": product.get_translated_field(
                "short_description", lang_code
            ),
            "category": (
                product.category.get_translated_field("title", lang_code)
                if product.category
                else None
            ),
            "subcategory": (
                product.subcategory.get_translated_field("title", lang_code)
                if product.subcategory
                else None
            ),
            "availability_status": product.get_availability_status_display(
                lang_code=lang_code
            ),
            "cip_type": product.get_cip_type_display(),
            "view_count": product.view_count,
            "is_new": product.created_at >= timezone.now() - timedelta(days=7),
            "related_products": get_products_list(
                product.related_products.all(),
                lang_code=lang_code,
                request=request,
            ),
            "similar_products": get_products_list(
                Product.objects.filter(
                    category=product.category, subcategory=product.subcategory
                ).exclude(pk=product_id),
                lang_code=lang_code,
                request=request,
            ),
            "supplier": get_supplier_data(product.supplier),
        }

        cache.set(cache_key, product_data, timeout=60 * 15)

    return product_data


def list_products(
    request,
    lang_code: str,
    random: bool = False,
    category_id: int = 0,
    sub_category_id: int = 0,
    search_query: str = "",
    order_by: str = "views",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    cache_key = f"product_list_{category_id}_{sub_category_id}_{search_query}_{order_by}_{page}_{page_size}_{lang_code}"  # noqa
    cached_data = cache.get(cache_key)

    # Query the total count of products matching the criteria
    queryset = Product.objects.filter(approved=True)

    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    if category_id != 0:
        queryset = queryset.filter(category_id=category_id)

    if sub_category_id != 0:
        queryset = queryset.filter(subcategory_id=sub_category_id)

    total_count = queryset.count()

    # Check if the total count in cache matches the current total count
    if cached_data and cached_data["total_count"] == total_count:
        return cached_data

    if order_by:
        queryset = queryset.order_by(order_by)

    total_count, queryset = paginate_queryset(queryset, page, page_size)

    if random:
        queryset = sample(list(queryset), len(queryset))

    currency_rate = get_currency_rate()
    products_data = get_products_list(
        queryset=queryset,
        lang_code=lang_code,
        request=request,
        currency_rate=currency_rate,
    )

    updated_data = {
        "products": products_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }

    cache.set(cache_key, updated_data, timeout=60 * 5)  # Cache for 15 minutes

    return updated_data


def get_products_list(queryset, lang_code, request, currency_rate):
    return [
        {
            "id": product.pk,
            "name": product.get_translated_field("name", lang_code),
            "price_in_usd": _calc_product_cost(
                product=product, currency_rate=currency_rate
            ),
            "price_in_uzs": _calc_product_cost(
                product=product, in_uzs=True, currency_rate=currency_rate
            ),
            "has_discount": product.discount > 0,
            "discount_persentage": product.discount,
            "price_with_discount_in_usd": _calc_product_cost_with_disc(
                product=product,
            ),
            "price_with_discount_in_uzs": _calc_product_cost_with_disc(
                product=product, in_uzs=True
            ),
            "images": [
                request.build_absolute_uri(image.image.url)
                for image in product.images.all()
            ],
            "background_image": (
                request.build_absolute_uri(product.background_image.image.url)
                if product.background_image
                else ""
            ),
            "cip_type": product.get_cip_type_display(),
            "availability_status_readable": product.get_availability_status_display(  # noqa
                lang_code=lang_code
            ),
            "availability_status": (
                "inStock" if product.availability_status == 1 else "outStock"
            ),
            "is_new": product.created_at >= timezone.now() - timedelta(days=7),
            "view_count": product.view_count,
            "specifications": [
                {
                    "title": feature.get_translated_field("title", lang_code),
                    "value": feature.get_translated_field("value", lang_code),
                }
                for feature in product.specifications.all()
            ],
        }
        for product in queryset
    ]
