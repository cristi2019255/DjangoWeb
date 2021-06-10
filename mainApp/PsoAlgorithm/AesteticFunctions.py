from math import *

p = 10


def F1(x1, x2):
    return (x1 or x2) % 255


def F2(x1, x2):
    return (p & x2) % 255


def F3(x1, x2):
    return (x1 / (1 + x2 + p)) % 255


def F4(x1, x2):
    return (x1 * x2) % 255


def F5(x1, x2):
    return (x1 + x2) % 255


def F6(x1, x2):
    return abs(x1 - x2) % 255


def F7(x1, x2):
    return 255 - x1 % 255


def F8(x1, x2):
    return abs(255 - cos(x1))


def F9(x1, x2):
    return abs(255 * tan((x1 % 45) * (pi / 180)))


def F10(x1, x2):
    return abs(255 * tan(x1) % 255)


def F11(x1, x2):
    return sqrt(x1 ** 2 + x2 ** 2) % 255


def F12(x1, x2):
    return x1 % (p + 1) + 255 - p


def F13(x1, x2):
    return (x1 + x2) / 2 % 255


def F14(x1, x2):
    if (x1 < x2):
        return 255 * ((x1 + 1) / (x2 + 1))
    else:
        return 255 * ((x2 + 1) / (x1 + 1))


def F15(x1, x2):
    return abs(sqrt(abs(x1 ** 2 + x2 ** 2 - 2 * (p ** 2))) % 255)


functions = [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15]
