from api.models import Partner


def list_partners(request) -> list:
    partners_list = []

    for partner in Partner.objects.all():
        partners_list.append({"image": request.build_absolute_uri(partner.image.url)})

    return partners_list
