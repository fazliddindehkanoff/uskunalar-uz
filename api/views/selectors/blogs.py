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
