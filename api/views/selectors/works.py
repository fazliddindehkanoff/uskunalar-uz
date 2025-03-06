from api.models import Work
from api.utils import paginate_queryset
from django.shortcuts import get_object_or_404


def get_works_list(queryset, lang_code, request):
    works_data = []
    for work in queryset:
        work_data = {
            "id": work.pk,
            "title": work.get_translated_field("title", lang_code),
            "short_description": work.get_translated_field(
                "short_description", lang_code
            ),
            "image_url": request.build_absolute_uri(work.image.url).replace(
                "http://", "https://"
            ),
            "view_count": work.view_count,
        }
        works_data.append(work_data)
    return works_data


def list_works(
    request,
    lang_code: str,
    search_query: str = "",
    order_by: str = "created_at",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    queryset = Work.objects.all()

    # Searching
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)

    # Ordering
    if order_by:
        queryset = queryset.order_by(order_by)

    total_count = queryset.count()

    # Pagination
    total_count, queryset = paginate_queryset(queryset, page, page_size)

    # Formatting the result
    works_data = get_works_list(
        queryset=queryset,
        lang_code=lang_code,
        request=request,
    )

    return {
        "works": works_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }


def work_detail(lang_code: str, work_id: int, request) -> dict:
    work = get_object_or_404(Work, pk=work_id)
    work.view_count += 1
    work.save()

    return {
        "id": work.pk,
        "title": work.get_translated_field("title", lang_code),
        "short_description": work.get_translated_field(
            "short_description",
            lang_code,
        ),
        "long_description": work.get_translated_field(
            "long_description",
            lang_code,
        ),
        "image_url": request.build_absolute_uri(work.image.url).replace(
            "http://", "https://"
        ),
        "yt_url": work.yt_url,
        "view_count": work.view_count,
    }
