from concurrent.futures import ThreadPoolExecutor
from random import choice
from main_logic import chars


def generate_one(length):
    return "".join(choice(chars) for _ in range(length))


def parallel_passwords(n, length=12):
    if n < 0:
        raise ValueError("n должно быть >= 0")

    with ThreadPoolExecutor() as ex:
        return list(ex.map(lambda _: generate_one(length), range(n)))
