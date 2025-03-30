import string
import random


def get_random_code(k=6) -> str:
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    return res
