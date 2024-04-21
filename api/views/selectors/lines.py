from rest_framework.exceptions import NotFound

from api.models import Line


def list_line_posts(
    request,
    lang_code: str,
    search_query: str = "",
    order_by: str = "created_at",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    queryset = Line.objects.all()

    # Searching
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)

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
    line_posts_data = []
    for post in queryset:
        post_data = {
            "id": post.pk,
            "title": post.get_translated_field("title", lang_code),
            "image_url": request.build_absolute_uri(post.image.url),
            "banner_url": request.build_absolute_uri(post.banner.url),
            "category": post.category.get_translated_field("title", lang_code),
            "short_description": post.get_translated_field(
                "short_description", lang_code
            ),
            "view_count": post.view_count,
            "created_at": post.created_at,
        }
        line_posts_data.append(post_data)

    return line_posts_data


def line_post_detail(lang_code: str, line_post_id: int, request) -> dict:
    line_post = Line.objects.filter(pk=line_post_id).first()

    if line_post:
        line_post.view_count += 1
        line_post.save()
        return {
            "id": line_post.pk,
            "title": line_post.get_translated_field("title", lang_code),
            "price": line_post.price,
            "category": line_post.category.get_translated_field("title", lang_code),
            "short_description": line_post.get_translated_field(
                "short_description", lang_code
            ),
            "long_description": line_post.get_translated_field(
                "long_description", lang_code
            ),
            "image_url": request.build_absolute_uri(line_post.image.url),
            "banner_url": request.build_absolute_uri(line_post.banner.url),
            "view_count": line_post.view_count,
            "created_at": line_post.created_at,
        }

    else:
        raise NotFound("There is no line post with given id")
