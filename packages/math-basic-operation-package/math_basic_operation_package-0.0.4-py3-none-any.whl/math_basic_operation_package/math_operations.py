def add(a: float, b: float) -> float:
    return a + b


def divide(a: float, b: float) -> float:
    if b != 0:
        return a / b


    raise ZeroDivisionError("Invalid value")


def multiple(a: float, b: float) -> float:
    return a * b


def subtract(a: float, b: float) -> float:
    return a - b
