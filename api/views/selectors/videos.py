from api.models import Video
from api.utils import paginate_queryset


def list_videos(lang_code: str, page: int = 1, page_size: int = 10) -> dict:
    queryset = Video.objects.all()
    total_count, queryset = paginate_queryset(queryset, page, page_size)

    videos_data = []
    for video in queryset:
        videos_data.append(
            {
                "id": video.pk,
                "title": video.get_translated_field("title", lang_code),
                "description": video.get_translated_field("description", lang_code),
                "video_link": video.video_link,
            }
        )

    return {
        "videos": videos_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }
