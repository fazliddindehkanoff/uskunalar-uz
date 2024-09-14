from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator, EmptyPage

from api.models import Gallery


def get_list_of_galleries(
    request, lang_code="uz", order_by="created_at", page=1, page_size=10
):
    galleries = Gallery.objects.all().order_by(order_by)
    paginator = Paginator(galleries, page_size)

    try:
        paginated_galleries = paginator.page(page)
    except EmptyPage:
        paginated_galleries = paginator.page(paginator.num_pages)

    galleries_data = []
    for gallery in paginated_galleries:
        gallery_data = {
            "id": gallery.pk,
            "title": gallery.get_translated_field("title", lang_code),
            "images": [
                request.build_absolute_uri(image.image.url).replace(
                    "http://", "https://"
                )
                for image in gallery.images.all()
            ],
            "short_description": gallery.get_translated_field(
                "short_description", lang_code
            ),
            "view_count": gallery.view_count,
            "created_at": gallery.created_at,
        }
        galleries_data.append(gallery_data)

    return {
        "results": galleries_data,
        "page": page,
        "total_pages": paginator.num_pages,
        "total_count": paginator.count,
    }


def get_gallery_detail(gallery_id, request, lang_code="uz"):
    gallery = Gallery.objects.filter(pk=gallery_id).first()
    if gallery:
        gallery.view_count += 1
        gallery.save()
        return {
            "id": gallery.pk,
            "title": gallery.get_translated_field("title", lang_code),
            "images": [
                request.build_absolute_uri(image.image.url).replace(
                    "http://", "https://"
                )
                for image in gallery.images.all()
            ],
            "short_description": gallery.get_translated_field(
                "short_description", lang_code
            ),
            "description": gallery.get_translated_field(
                "description",
                lang_code,
            ),
            "view_count": gallery.view_count,
            "created_at": gallery.created_at,
        }
    else:
        raise NotFound("There is no gallery with given id")
