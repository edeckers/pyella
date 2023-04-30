from typing import Any, Callable, TypeVar

TA = TypeVar("TA")  # pylint: disable=invalid-name


def _const(value: TA) -> Callable[[Any], TA]:
    return lambda _: value


def _identity(value: TA) -> TA:
    return value
