from typing import Callable, TypeVar

TA = TypeVar("TA")  # pylint: disable=invalid-name
TB = TypeVar("TB")  # pylint: disable=invalid-name


def _const(value: TA) -> Callable[[TB], TA]:
    return lambda _: value


def _identity(value: TA) -> TA:
    return value
