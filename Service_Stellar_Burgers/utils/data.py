import random
import string
import time

def generate_email():
    base = "test_user"
    cohort = "10"
    random_digits = ''.join(random.choices(string.digits, k=3))
    timestamp = str(int(time.time()))[-6:]
    return f"{base}_{cohort}_{random_digits}_{timestamp}@yandex.ru"

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_name():
    return "TestUser"