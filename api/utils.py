import os
import environ
import random
import requests

from pathlib import Path
from eskiz_sms import EskizSMS

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
    response = requests.get("https://nbu.uz/en/exchange-rates/json/")

    if response.status_code == 200:
        data = response.json()
        return int(float(data[23]["nbu_buy_price"]))
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def paginate_queryset(queryset, page, page_size):
    total_count = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]
    return total_count, queryset
