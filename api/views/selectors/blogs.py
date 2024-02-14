from api.models import Blog


def get_blog_posts_list(request, lang_code: str) -> list:
    blog_posts = []
    for blog_post in Blog.objects.all():
        blog_posts.append(
            get_blog_detail(request=request, blog_post=blog_post, lang_code=lang_code)
        )

    return blog_posts


def get_blog_detail(request, blog_post: Blog, lang_code: str) -> dict:
    return {
        "title": blog_post.get_translated_field(
            field_name="title", lang_code=lang_code
        ),
        "content": blog_post.get_translated_field(
            field_name="content", lang_code=lang_code
        ),
        "cover_image": request.build_absolute_uri(blog_post.cover.url),
    }


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
            "content": post.get_translated_field("content", lang_code),
            "created_at": post.created_at,
        }
        # Add more data as needed
        blog_posts_data.append(post_data)

    return blog_posts_data
