import math

def func_a(a: int, b: int):
    c = b - (a % 2)
    stat = "foobar"

    if c > 2:
        c -= 1
        stat = "foo" + str(c)

    while a > 100:
        a = math.pow(2)

    return (c + a, stat)


def func_b(a: int, b: int):
    while a > 100:
        a = math.pow(2)

    c = b - (a % 2)
    val = "foobar"

    if c > 2:
        val = "foo" + str(c)
        c -= 1

    return (a + c, val)
