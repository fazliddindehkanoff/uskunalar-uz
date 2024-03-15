from api.models import Banner


def list_banners(request) -> list:
    banners = []
    lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE")

    for banner in Banner.objects.all():
        banners.append(
            {
                "product_url": banner.product_url,
                "image_url": request.build_absolute_uri(
                    banner.get_translated_field("banner_image", lang_code=lang_code).url
                ),
            }
        )

    return banners
