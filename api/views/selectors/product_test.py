from random import sample
from datetime import timedelta

from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.db.models import Q
from django.core.cache import cache

from api.models import Product
from api.utils import get_currency_rate, paginate_queryset


def _calc_product_cost(product: Product, currency_rate, in_uzs=False) -> str:
    price = product.price
    min_price = product.min_price
    max_price = product.max_price
    price_extra = 0
    min_price_extra = 0
    max_price_extra = 0

    if in_uzs:
        extra_payment_percent = 13.5
        currency_symbol = ""
    else:
        extra_payment_percent = 0
        currency_rate = 1
        currency_symbol = "$"

    if price and price != 0:
        price_extra += round(
            ((price + (price * extra_payment_percent) / 100)) * currency_rate, 2
        )
        if in_uzs:
            price += price_extra
        return f"{currency_symbol}{price:,}"

    elif min_price is not None and max_price is not None:
        min_price_extra += round(
            ((min_price + (min_price * extra_payment_percent) / 100)) * currency_rate, 2
        )
        max_price_extra += round(
            ((max_price + (max_price * extra_payment_percent) / 100)) * currency_rate, 2
        )

        if in_uzs:
            min_price += min_price_extra
            max_price += max_price_extra

        try:
            return f"{currency_symbol}{min_price:,} - {currency_symbol}{max_price:,}"  # noqa
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
    extra_payment_percent = 13.5 if in_uzs else 0
    price = product.price
    min_price = product.min_price
    max_price = product.max_price
    if min_price is not None and max_price is not None:
        min_discounted_price = discount_calc(
            min_price * currency_rate,
            discount,
        )
        max_discounted_price = discount_calc(
            max_price * currency_rate,
            discount,
        )
    if price and price != 0:
        discounted_price = discount_calc(price * currency_rate, discount)

    if discount > 0:
        if price and price != 0:
            return f"{currency_symbol}{discounted_price + (discounted_price * extra_payment_percent)/100 :,}"  # noqa
        else:
            return f"{currency_symbol}{min_discounted_price + (min_discounted_price * extra_payment_percent)/100 :,} - {currency_symbol}{max_discounted_price + (max_discounted_price * extra_payment_percent)/100 :,}"  # noqa
    return ""


def product_detail(
    request,
    lang_code: str,
    product_id: str,
) -> dict:

    if "," in product_id:
        currency_rate = get_currency_rate()
        product_ids = product_id.split(",")
        return get_products_list(
            queryset="",
            lang_code=lang_code,
            request=request,
            currency_rate=currency_rate,
            product_ids=product_ids,
        )
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

        if not product.approved:
            raise NotFound("Bu mahsulot hozirda sotuvda mavjud emas")

        product.view_count += 1
        product.save()

        product_data = {
            "id": product.pk,
            "has_discount": product.discount > 0,
            "discount_persentage": product.discount,
            "images": [
                request.build_absolute_uri(image.image.url).replace(
                    "http://", "https://"
                )
                for image in product.images.all()
            ],
            "background_image": (
                request.build_absolute_uri(product.background_image.image.url)
                if product.background_image
                else ""
            ).replace("http://", "https://"),
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
            "category_id": product.category.id,
            "subcategory_id": product.subcategory.id,
            "subcategory": (
                product.subcategory.get_translated_field("title", lang_code)
                if product.subcategory
                else None
            ),
            "availability_status": product.get_availability_status_display(
                lang_code=lang_code
            ),
            "video_url": product.video_url,
            "view_count": product.view_count,
            "is_new": product.created_at >= timezone.now() - timedelta(days=7),
            "related_products": get_products_list(
                product.related_products.all(),
                lang_code=lang_code,
                request=request,
                currency_rate=currency_rate,
            ),
            "similar_products": get_products_list(
                Product.objects.filter(
                    category=product.category, subcategory=product.subcategory
                ).exclude(pk=product_id),
                lang_code=lang_code,
                request=request,
                currency_rate=currency_rate,
            ),
            "country": product.supplier.country if product.supplier else "",
            "supplier_logo": (
                request.build_absolute_uri(product.supplier.logo.url)
                if product.supplier and product.supplier.logo and product.show_supplier
                else ""
            ).replace("http://", "https://"),
            "tags": [tag for tag in product.tags.split(",")],
            "price": {
                "incoterms": product.get_cip_type_display(),
                "absolute_price_in_usd": product.price,
                "min_price_in_usd": product.min_price,
                "max_price_in_usd": product.max_price,
                "absolute_price_in_uzs": (
                    product.price * currency_rate
                    if product.show_cost_in_uzs and product.price
                    else ""
                ),
                "min_price_in_uzs": (
                    product.min_price * currency_rate
                    if product.show_cost_in_uzs
                    else ""
                ),
                "max_price_in_uzs": (
                    product.max_price * currency_rate
                    if product.show_cost_in_uzs
                    else ""
                ),
                "price_with_discount_in_usd": _calc_product_cost_with_disc(
                    product=product, currency_rate=currency_rate
                ),
                "price_with_discount_in_uzs": (
                    _calc_product_cost_with_disc(
                        product=product,
                        in_uzs=True,
                        currency_rate=currency_rate,
                    )
                    if product.show_cost_in_uzs
                    else ""
                ),
                "by_models": [
                    {
                        "name": product_price.model,
                        "price_in_usd": product_price.price,
                        "price_in_uzs": product_price.price * currency_rate,
                        "is_active": product_price.is_active,
                    }
                    for product_price in product.prices.all()
                ],
            },
        }

        # cache.set(cache_key, product_data, timeout=60 * 5)

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
        if search_query.isdigit():
            queryset = queryset.filter(
                Q(id=search_query)
                | Q(name_uz__icontains=search_query)
                | Q(name_ru__icontains=search_query)
                | Q(name_en__icontains=search_query)
                | Q(short_description_uz__icontains=search_query)
                | Q(short_description_ru__icontains=search_query)
                | Q(short_description_en__icontains=search_query)
                | Q(tags__icontains=search_query)
            )
        else:
            queryset = queryset.filter(
                Q(name_uz__icontains=search_query)
                | Q(name_ru__icontains=search_query)
                | Q(name_en__icontains=search_query)
                | Q(short_description_uz__icontains=search_query)
                | Q(short_description_ru__icontains=search_query)
                | Q(short_description_en__icontains=search_query)
                | Q(tags__icontains=search_query)
            )

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

    cache.set(cache_key, updated_data, timeout=60 * 5)
    return updated_data


def get_products_list(
    queryset,
    lang_code,
    request,
    currency_rate,
    product_ids=None,
):
    if product_ids:
        queryset = Product.objects.filter(pk__in=product_ids)

    return [
        {
            "id": product.pk,
            "name": product.get_translated_field("name", lang_code),
            "price_in_usd": _calc_product_cost(
                product=product, currency_rate=currency_rate
            ),
            "price_in_uzs": (
                _calc_product_cost(
                    product=product, in_uzs=True, currency_rate=currency_rate
                )
                if product.show_cost_in_uzs
                else ""
            ),
            "has_discount": product.discount > 0,
            "discount_persentage": product.discount,
            "images": [
                request.build_absolute_uri(image.image.url).replace(
                    "http://", "https://"
                )
                for image in product.images.all()
            ],
            "background_image": (
                request.build_absolute_uri(product.background_image.image.url)
                if product.background_image
                else ""
            ).replace("http://", "https://"),
            "video_url": product.video_url,
            "availability_status_readable": product.get_availability_status_display(  # noqa
                lang_code=lang_code
            ),
            "availability_status": (
                "inStock" if product.availability_status == 1 else "outStock"
            ),
            "is_new": product.created_at >= timezone.now() - timedelta(days=7),
            "view_count": product.view_count,
            "country": product.supplier.country if product.supplier else "",
            "supplier_logo": (
                request.build_absolute_uri(product.supplier.logo.url)
                if product.supplier and product.supplier.logo and product.show_supplier
                else ""
            ).replace("http://", "https://"),
            "specifications": [
                {
                    "title": feature.get_translated_field("title", lang_code),
                    "value": feature.get_translated_field("value", lang_code),
                }
                for feature in product.specifications.all()
            ],
            "price": {
                "incoterms": product.get_cip_type_display(),
                "absolute_price_in_usd": product.price,
                "min_price_in_usd": product.min_price,
                "max_price_in_usd": product.max_price,
                "absolute_price_in_uzs": (
                    product.price * currency_rate
                    if product.show_cost_in_uzs and product.price
                    else ""
                ),
                "min_price_in_uzs": (
                    product.min_price * currency_rate
                    if product.show_cost_in_uzs
                    else ""
                ),
                "max_price_in_uzs": (
                    product.max_price * currency_rate
                    if product.show_cost_in_uzs
                    else ""
                ),
                "price_with_discount_in_usd": _calc_product_cost_with_disc(
                    product=product, currency_rate=currency_rate
                ),
                "price_with_discount_in_uzs": (
                    _calc_product_cost_with_disc(
                        product=product,
                        in_uzs=True,
                        currency_rate=currency_rate,
                    )
                    if product.show_cost_in_uzs
                    else ""
                ),
                "by_models": [
                    {
                        "name": product_price.model,
                        "price_in_usd": product_price.price,
                        "price_in_uzs": product_price.price * currency_rate,
                        "is_active": product_price.is_active,
                    }
                    for product_price in product.prices.all()
                ],
            },
        }
        for product in queryset
    ]
