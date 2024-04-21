from rest_framework.exceptions import NotFound

from api.models import Blog


def list_blog_posts(
    request,
    lang_code: str,
    search_query: str = "",
    order_by: str = "created_at",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    queryset = Blog.objects.all()

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
    blog_posts_data = get_blog_posts_list(
        queryset=queryset, lang_code=lang_code, request=request
    )

    return {
        "blog_posts": blog_posts_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }


def get_blog_posts_list(queryset, lang_code, request):
    blog_posts_data = []
    for post in queryset:
        post_data = {
            "id": post.pk,
            "title": post.get_translated_field("title", lang_code),
            "cover_url": (
                request.build_absolute_uri(post.cover.url) if post.cover else ""
            ),
            "content": post.get_translated_field("content", lang_code),
            "view_count": post.view_count,
            "created_at": post.created_at,
        }
        blog_posts_data.append(post_data)

    return blog_posts_data


def blog_post_detail(lang_code: str, blog_post_id: int, request) -> dict:
    blog_post = Blog.objects.filter(pk=blog_post_id).first()

    if blog_post:
        blog_post.view_count += 1
        blog_post.save()
        return {
            "id": blog_post.pk,
            "title": blog_post.get_translated_field("title", lang_code),
            "cover_url": (
                request.build_absolute_uri(blog_post.cover.url)
                if blog_post.cover
                else ""
            ),
            "content": blog_post.get_translated_field("content", lang_code),
            "view_count": blog_post.view_count,
            "created_at": blog_post.created_at,
        }

    else:
        raise NotFound("There is no product with given id")
