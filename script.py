import json
import os
import requests

from django.conf import settings
from api.models import (
    Banner,
    PartnerLogos,
    LineCategory,
    Line,
    SubCategory,
    Product,
    ProductImage,
    ProductFeature,
    Video,
    Work,
)


def save_banner():
    with open("data/banners.json", "r") as file:
        banner_data = json.load(file)

    for data in banner_data:
        Banner.objects.get_or_create(
            id=data["id"],
            banner_image_uz=download_image(data["banner_image_uz"]),
            banner_image_ru=download_image(data["banner_image_ru"]),
            banner_image_en=download_image(data["banner_image_en"]),
            product_url=data["link"],
            created_at=data["created_at"],
        )


def download_image(url):
    try:
        response = requests.get(url, stream=True)
        filename = url.split("/")[-1]
        if response.status_code == 200:
            filepath = os.path.join(settings.MEDIA_ROOT, filename)

            with open(filepath, "wb") as out_file:
                out_file.write(response.content)

        return filename
    except Exception:
        return None


def save_categories():
    url = "https://api.uskunalar.uz/en/api-auth/sub_categories/?page=1&page_size=700"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for sub_category_data in data["results"]:
            sub_category = SubCategory.objects.filter(
                id=sub_category_data.get("id")
            ).first()
            if sub_category:
                sub_category_image = download_image(sub_category_data.get("image"))
                print(sub_category_image)
                sub_category.icon = sub_category_image
                sub_category.save()


def save_partners():
    with open("data/partners.json", "r") as file:
        partner_data = json.load(file)

    for data in partner_data:
        PartnerLogos.objects.create(
            id=data["id"],
            image=download_image(data["image"]),
            created_at=data["created_at"],
        )


def save_line_categories():
    with open("data/lines-category.json", "r") as file:
        line_category_data = json.load(file)

    for data in line_category_data:
        LineCategory.objects.create(
            id=data["id"],
            title_uz=data["category_uz"],
            title_en=data["category_en"],
            title_ru=data["category_ru"],
            created_at=data["created_at"],
        )


def save_lines():
    with open("data/lines.json", "r") as file:
        line_data = json.load(file)

    for data in line_data:
        Line.objects.create(
            id=data["id"],
            title_uz=data["title_uz"],
            title_en=data["title_en"],
            title_ru=data["title_ru"],
            category_id=data["category"]["id"],
            short_description_uz=data["description_uz"],
            short_description_en=data["description_en"],
            short_description_ru=data["description_ru"],
            long_description_en=data["long_description_en"],
            long_description_uz=data["long_description_uz"],
            long_description_ru=data["long_description_ru"],
            price=data["price"],
            view_count=data["views"],
            image=download_image(data["image"]),
            banner=download_image(data["banner"]),
            created_at=data["created_at"],
        )


def save_products():
    for i in range(168, 1325):
        url = f"https://api.uskunalar.uz/en/api-auth/products/{i}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if data["DAF"]:
                cip_type = 1
            elif data["EXW"]:
                cip_type = 2
            else:
                cip_type = 3

            product = Product.objects.create(
                id=data["sku"],
                name_uz=data["title_uz"],
                name_en=data["title_en"],
                name_ru=data["title_ru"],
                short_description_uz=data["short_description_uz"],
                short_description_ru=data["short_description_ru"],
                short_description_en=data["short_description_en"],
                description_uz=data["long_description_uz"],
                description_en=data["long_description_en"],
                description_ru=data["long_description_ru"],
                view_count=data["view_count"],
                created_at=data["created_at"],
                price=data["price"],
                availability_status=1 if data["delivery"] == "Buyurtma orqali" else 2,
                discount=data["discount"],
                category_id=data["category"]["id"],
                subcategory_id=data["subcategory"]["id"],
                cip_type=cip_type,
            )
            for image in data["images"]:
                ProductImage.objects.create(
                    id=image["id"],
                    product=product,
                    image=download_image(image["image"]),
                )
            for product_feat in data["specifications"]:
                ProductFeature.objects.create(
                    id=product_feat["id"],
                    product=product,
                    title_uz=product_feat["product_customer_uz"],
                    title_en=product_feat["product_customer_en"],
                    title_ru=product_feat["product_customer_ru"],
                    value_uz=product_feat["product_number_uz"],
                    value_en=product_feat["product_number_en"],
                    value_ru=product_feat["product_number_ru"],
                )
        print(f"Product: {i} has been saved")


def save_work():
    with open("data/works.json", "r") as file:
        work_data = json.load(file)

    for data in work_data:
        Work.objects.create(
            id=data["id"],
            title_uz=data["title_uz"],
            title_ru=data["title_ru"],
            title_en=data["title_en"],
            short_description_uz=data["short_descriptions_uz"],
            short_description_ru=data["short_descriptions_ru"],
            short_description_en=data["short_descriptions_en"],
            long_description_uz=data["descriptions_uz"],
            long_description_ru=data["descriptions_ru"],
            long_description_en=data["descriptions_en"],
            view_count=data["views"],
            created_at=data["created_at"],
            image=download_image(data["image"]),
        )


def save_videos():
    with open("data/videos.json", "r") as file:
        video_data = json.load(file)

    for data in video_data:
        Video.objects.create(
            id=data["id"],
            title_uz=data["title_uz"],
            title_ru=data["title_ru"],
            title_en=data["title_en"],
            description_uz=data["description_uz"],
            description_ru=data["description_ru"],
            description_en=data["description_en"],
            video_link=data["url"],
            created_at=data["created_at"],
        )


def main():
    # save_banner()
    save_categories()
    # save_partners()
    # save_line_categories()
    # save_lines()
    # save_work()
    # save_videos()
    # save_products()
