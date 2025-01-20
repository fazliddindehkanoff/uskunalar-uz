import os
import environ
import random
import requests

from pathlib import Path
from django.db.models import Model
from eskiz_sms import EskizSMS

from api.models import SubCategory, Product

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


def send_sms(code: str, phone_num: str) -> None:
    eskiz = EskizSMS(env("SMS_EMAIL"), env("SMS_PASSWORD"))
    if len(phone_num) < 12:
        phone_num = "998" + phone_num
    eskiz.send_sms(phone_num, message=code)


def generate_code() -> int:
    return random.randint(100000, 999999)


def get_currency_rate():
    response = requests.get("https://cbu.uz/en/arkhiv-kursov-valyut/json/")

    if response.status_code == 200:
        data = response.json()
        return int(float(data[0]["rate"]))
    else:
        print(f"Failed to retrieve the page. {response.status_code}")


def paginate_queryset(queryset, page, page_size):
    total_count = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]
    return total_count, queryset


def get_list_of_object_ids(Object: Model, **filters) -> list:
    object_ids = []
    for object in Object.objects.filter(**filters):
        object_ids.append({"pk": object.pk})

    return object_ids


def set_sub_category_status(category_id: int, status: bool) -> None:
    for subcategory in SubCategory.objects.filter(
        category_id=category_id,
    ):
        subcategory.available = status
        subcategory.save()


def set_product_status(category_id: int, status: bool) -> None:
    for product in Product.objects.filter(category_id=category_id):
        product.approved = status
        product.save()


def get_number_of_unapproved_products(request) -> int:
    unapproved_products_count = Product.objects.filter(approved=False).count()
    if unapproved_products_count > 0 and request.user.is_superuser:
        return unapproved_products_count
    return ""


def get_number_of_products(request) -> int:
    unapproved_products_count = Product.objects.filter(approved=True).count()
    if unapproved_products_count > 0 and request.user.is_superuser:
        return unapproved_products_count
    return ""
