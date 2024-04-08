from random import sample
from datetime import datetime, timedelta

from rest_framework.exceptions import NotFound
from django.utils import timezone

from api.models import Product
from api.utils import get_currency_rate
from .supplier import get_supplier_data


def _calc_product_cost(product: Product, in_uzs=False) -> str:

    if in_uzs:
        currency_rate = get_currency_rate()
    else:
        currency_rate = 1

    if product.price and product.price != 0:
        return f"{product.price*currency_rate:,}"
    elif product.min_price is not None and product.min_price is not None:
        try:
            return (
                f"{product.min_price*currency_rate:,}-{product.max_price*currency_rate}"
            )
        except Exception:
            return f"there is an error with id:{product.pk}"


def discount_calc(price: int, discount: int) -> str:
    return price - (price * discount) / 100


def _calc_product_cost_with_disc(product: Product, in_uzs=False) -> str:
    discount = product.discount
    currency_rate = 1
    if in_uzs:
        currency_rate = get_currency_rate()
    if discount > 0:
        if product.price and product.price != 0:
            return f"{discount_calc(product.price*currency_rate, discount):,}"
        else:
            return f"{discount_calc(product.min_price*currency_rate, discount):,}-{discount_calc(product.max_price*currency_rate, discount):,}"


def product_detail(request, lang_code: str, product_id: int) -> dict:
    product_data = {}
    product = Product.objects.filter(pk=product_id).first()

    if product:
        product.view_count += 1
        product.save()

        product_data["id"] = product.pk
        product_data["price_in_usd"] = _calc_product_cost(product=product)
        product_data["price_in_uzs"] = _calc_product_cost(product=product, in_uzs=True)
        product_data["has_discount"] = product.discount > 0
        product_data["price_with_discount_in_usd"] = _calc_product_cost_with_disc(
            product=product
        )
        product_data["price_with_discount_in_uzs"] = _calc_product_cost_with_disc(
            product=product, in_uzs=True
        )
        product_data["images"] = [
            request.build_absolute_uri(image.image.url)
            for image in product.images.all()
        ]
        product_data["background_image"] = (
            request.build_absolute_uri(product.background_image.image.url)
            if product.background_image
            else ""
        )

        product_data["specifications"] = [
            {
                "title": feature.get_translated_field("title", lang_code),
                "value": feature.get_translated_field("value", lang_code),
            }
            for feature in product.specifications.all()
        ]
        product_data["name"] = product.get_translated_field("name", lang_code)
        product_data["description"] = product.get_translated_field(
            "description", lang_code
        )
        product_data["short_description"] = product.get_translated_field(
            "short_description", lang_code
        )

        product_data["category"] = (
            product.category.get_translated_field("title", lang_code)
            if product.category
            else None
        )
        product_data["subcategory"] = (
            product.subcategory.get_translated_field("title", lang_code)
            if product.subcategory
            else None
        )

        product_data["availability_status"] = product.get_availability_status_display(
            lang_code=lang_code
        )
        product_data["discount"] = product.discount
        product_data["cip_type"] = product.get_cip_type_display()
        product_data["view_count"] = product.view_count
        product_data["related_products"] = get_products_list(
            product.related_products.all(),
            lang_code=lang_code,
            request=request,
        )
        product_data["similar_products"] = get_products_list(
            Product.objects.filter(
                category=product.category, subcategory=product.subcategory
            ).exclude(pk=product_id),
            lang_code=lang_code,
            request=request,
        )
        product_data["supplier"] = get_supplier_data(product.supplier)

    else:
        raise NotFound("There is no product with given id")
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
    queryset = Product.objects.all()

    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    if category_id != 0:
        queryset = queryset.filter(category_id=category_id)

    if sub_category_id != 0:
        queryset = queryset.filter(subcategory_id=sub_category_id)

    total_count = queryset.count()

    if random:
        queryset = sample(list(queryset), len(queryset))

    if order_by:
        queryset = queryset.order_by(order_by)

    start = (page - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]

    products_data = get_products_list(
        queryset=queryset, lang_code=lang_code, request=request
    )

    return {
        "products": products_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }


def get_products_list(queryset, lang_code, request):
    products_data = []
    for product in queryset:
        product_data = {
            "id": product.pk,
            "name": product.get_translated_field("name", lang_code),
            "price_in_usd": _calc_product_cost(product=product),
            "price_in_uzs": _calc_product_cost(product=product, in_uzs=True),
            "has_discount": product.discount > 0,
            "price_with_discount_in_usd": _calc_product_cost_with_disc(product=product),
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
            "availability_status_readable": product.get_availability_status_display(
                lang_code=lang_code
            ),
            "availability_status": (
                "inStock" if product.availability_status == 1 else "outStock"
            ),
            "is_new": product.created_at >= timezone.now() - timedelta(days=7),
            "view_count": product.view_count,
        }
        product_data["specifications"] = [
            {
                "title": feature.get_translated_field("title", lang_code),
                "value": feature.get_translated_field("value", lang_code),
            }
            for feature in product.specifications.all()
        ]
        products_data.append(product_data)

    return products_data
