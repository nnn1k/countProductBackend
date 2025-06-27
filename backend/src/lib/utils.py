import asyncio
import string
import random
import sys
from asyncio import WindowsSelectorEventLoopPolicy


def get_random_code(k=6) -> str:
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    return res


def check_platform():
    # Установка политики цикла событий
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
