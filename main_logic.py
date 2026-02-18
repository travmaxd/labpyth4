from string import ascii_lowercase, ascii_uppercase
from random import choice
import operator


def abs_generator(a: int, b: int):
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a и b должны быть целыми числами")
    if a >= b:
        raise ValueError("a должно быть меньше b")

    for num in range(a, b + 1):
        yield abs(num)


chars = ascii_lowercase + ascii_uppercase + "0123456789!?@#$*"


def password_generator(length=12):
    if length <= 0:
        raise ValueError("Длина пароля должна быть > 0")

    while True:
        yield "".join(choice(chars) for _ in range(length))


def multiply_lists(list1, list2):
    for a, b in zip(list1, list2):
        yield a * b
