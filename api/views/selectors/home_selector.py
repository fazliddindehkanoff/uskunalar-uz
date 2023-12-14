from api.models import Partner, Category, Product, Banner, SubCategory


def get_home_page_data(lang_code: str) -> dict:
    result = {}
    result["partners"] = get_partners_list()
    result["categories"] = get_categories_list("uz")
    result["banners"] = get_banners_list("uz")
    return result


def get_partners_list() -> list:
    result = []
    partners = Partner.objects.all()
    for partner in partners:
        result.append({"url": partner.image.url})

    return result


def get_banners_list(lang_code: str) -> list:
    result = []
    banners = Banner.objects.all()
    for banner in banners:
        result.append(
            {
                "banner_image_url": banner.get_translated_field(
                    "banner_image", lang_code
                ).url,
                "url": banner.product_url,
            }
        )
    return result


def get_categories_list(lang_code: str) -> list:
    result = []
    categories = Category.objects.all()
    for category in categories:
        result.append(
            {
                "title": category.get_translated_field("title", lang_code),
                "icon": category.icon.url,
                "products_count": category.products.all().count(),
            }
        )
    return result
