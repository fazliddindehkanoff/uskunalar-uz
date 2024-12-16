from rest_framework.exceptions import NotFound
from django.db.models import Q

from api.models import Line
from api.utils import get_currency_rate


def _calc_line_cost(line, currency_rate, in_uzs=False) -> str:
    price = line.price
    min_price = line.min_price
    max_price = line.max_price

    if in_uzs:
        extra_payment_percent = 13.5
        currency_symbol = ""
    else:
        extra_payment_percent = 0
        currency_rate = 1
        currency_symbol = "$"

    if price and price != 0:
        price += round(((price * extra_payment_percent) / 100) * currency_rate, 2)
        return f"{currency_symbol}{price:,}"

    elif min_price is not None and max_price is not None:
        min_price += round(
            ((min_price * extra_payment_percent) / 100) * currency_rate, 2
        )
        max_price += round(
            ((max_price * extra_payment_percent) / 100) * currency_rate, 2
        )
        try:
            return f"{currency_symbol}{min_price:,} - {currency_symbol}{max_price:,}"
        except Exception:
            return f"there is an error with id:{line.pk}"
    return ""


def _calc_line_cost_with_disc(line, currency_rate, in_uzs=False) -> str:
    discount = line.discount_percent
    currency_rate = currency_rate if in_uzs else 1
    currency_symbol = "" if in_uzs else "$"
    extra_payment_percent = 13.5 if in_uzs else 0
    price = line.price
    min_price = line.min_price
    max_price = line.max_price

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
            return f"{currency_symbol}{discounted_price + (discounted_price * extra_payment_percent)/100 :,}"
        else:
            return f"{currency_symbol}{min_discounted_price + (min_discounted_price * extra_payment_percent)/100 :,} - {currency_symbol}{max_discounted_price + (max_discounted_price * extra_payment_percent)/100 :,}"
    return ""


def discount_calc(price: int, discount: int) -> int:
    return price - (price * discount) // 100


def list_line_posts(
    request,
    lang_code: str,
    category_id: int = 0,
    search_query: str = "",
    order_by: str = "created_at",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    # Only show approved lines
    queryset = Line.objects.filter(approved=True)

    if category_id > 0:
        queryset = queryset.filter(category_id=category_id)

    # Searching
    if search_query:
        queryset = queryset.filter(
            Q(title_uz__icontains=search_query)
            | Q(title_ru__icontains=search_query)
            | Q(title_en__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(tag__icontains=search_query)
        )

    # Ordering
    if order_by:
        queryset = queryset.order_by(order_by)

    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    total_count = queryset.count()
    queryset = queryset[start:end]

    # Formatting the result
    line_posts_data = get_line_posts_list(
        queryset=queryset, lang_code=lang_code, request=request
    )

    return {
        "line_posts": line_posts_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }


def get_line_posts_list(queryset, lang_code, request):
    currency_rate = get_currency_rate()
    line_posts_data = []
    for post in queryset:
        post_data = {
            "id": post.pk,
            "title": post.get_translated_field("title", lang_code),
            "images": [
                request.build_absolute_uri(image.url).replace(
                    "http://",
                    "https://",
                )
                for image in post.images.all()
            ],
            "banner_url": request.build_absolute_uri(post.banner.url).replace(
                "http://", "https://"
            ),
            "category": post.category.get_translated_field("title", lang_code),
            "short_description": post.get_translated_field(
                "short_description", lang_code
            ),
            "view_count": post.view_count,
            "created_at": post.created_at,
            "price_in_usd": _calc_line_cost(
                line=post,
                currency_rate=currency_rate,
            ),
            "price_in_uzs": _calc_line_cost(
                line=post, in_uzs=True, currency_rate=currency_rate
            ),
            "discount_percent": post.discount_percent,
            "has_discount": post.discount_percent > 0,
            "price_with_discount_in_usd": _calc_line_cost_with_disc(
                line=post, currency_rate=currency_rate
            ),
            "price_with_discount_in_uzs": _calc_line_cost_with_disc(
                line=post, in_uzs=True, currency_rate=currency_rate
            ),
            "cip_type": post.get_cip_type_display(),
            "yt_link": post.yt_link,
            "tags": [tag for tag in post.tag.split(",")],
            "supplier": (
                {
                    "id": post.supplier.id,
                    "name": post.supplier.name,
                    "logo_url": (
                        request.build_absolute_uri(
                            post.supplier.logo.url,
                        ).replace("http://", "https://")
                    ),
                }
                if post.supplier and post.show_supplier_logo
                else None
            ),
        }
        line_posts_data.append(post_data)

    return line_posts_data


def line_post_detail(lang_code: str, line_post_id: int, request) -> dict:
    try:
        line_post = Line.objects.get(pk=line_post_id, approved=True)
    except Line.DoesNotExist:
        raise NotFound("There is no line post with given id")

    if line_post:
        line_post.view_count += 1
        line_post.save()
        currency_rate = get_currency_rate()

        # Get similar lines from the same category
        similar_lines = Line.objects.filter(
            category=line_post.category, approved=True
        ).exclude(pk=line_post_id)[:9]

        return {
            "id": line_post.pk,
            "title": line_post.get_translated_field("title", lang_code),
            "price_in_usd": _calc_line_cost(
                line=line_post, currency_rate=currency_rate
            ),
            "price_in_uzs": _calc_line_cost(
                line=line_post, in_uzs=True, currency_rate=currency_rate
            ),
            "discount_percent": line_post.discount_percent,
            "has_discount": line_post.discount_percent > 0,
            "price_with_discount_in_usd": _calc_line_cost_with_disc(
                line=line_post, currency_rate=currency_rate
            ),
            "price_with_discount_in_uzs": _calc_line_cost_with_disc(
                line=line_post, in_uzs=True, currency_rate=currency_rate
            ),
            "cip_type": line_post.get_cip_type_display(),
            "yt_link": line_post.yt_link,
            "category": line_post.category.get_translated_field(
                "title",
                lang_code,
            ),
            "short_description": line_post.get_translated_field(
                "short_description", lang_code
            ),
            "long_description": line_post.get_translated_field(
                "long_description", lang_code
            ),
            "tags": [tag for tag in line_post.tag.split(",") if tag],
            "images": [
                request.build_absolute_uri(image.url).replace(
                    "http://",
                    "https://",
                )
                for image in line_post.images.all()
            ],
            "banner_url": request.build_absolute_uri(
                line_post.banner.url,
            ).replace("http://", "https://"),
            "view_count": line_post.view_count,
            "created_at": line_post.created_at,
            "supplier": (
                {
                    "id": line_post.supplier.id,
                    "name": line_post.supplier.name,
                    "logo_url": (
                        request.build_absolute_uri(line_post.supplier.logo.url).replace(
                            "http://", "https://"
                        )
                        if line_post.supplier and line_post.supplier.logo
                        else None
                    ),
                }
                if line_post.supplier and line_post.show_supplier_logo
                else None
            ),
            "similar_lines": get_line_posts_list(
                queryset=similar_lines, lang_code=lang_code, request=request
            ),
        }

    else:
        raise NotFound("There is no line post with given id")
