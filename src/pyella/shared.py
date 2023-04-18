from typing import Callable, TypeVar

TA = TypeVar("TA")
TB = TypeVar("TB")


def _const(a: TA) -> Callable[[TB], TA]:
    return lambda _: a
