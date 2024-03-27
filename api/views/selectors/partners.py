from api.models import PartnerLogos


def list_partners_logo(request) -> list:
    partners_list = []

    for partner in PartnerLogos.objects.all():
        partners_list.append(
            {
                "image": request.build_absolute_uri(partner.image.url),
            }
        )

    return partners_list
