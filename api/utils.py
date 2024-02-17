import os
import environ
import random

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
