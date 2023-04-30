# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, Optional, TypeVar

from pyella.shared import _const, _identity

TA = TypeVar("TA")  # pylint: disable=invalid-name
TB = TypeVar("TB")  # pylint: disable=invalid-name


class Maybe(Generic[TA]):  # pylint: disable=too-few-public-methods
    value: TA

    def bind(self, map_: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
        return bind(self, map_)

    def fmap(self, map_: Callable[[TA], TB]) -> Maybe[TB]:
        return fmap(self, map_)

    def from_maybe(self: Maybe[TA], fallback: TB) -> TB:
        return from_maybe(fallback, self)

    def is_nothing(self) -> bool:
        return is_nothing(self)

    def maybe(self: Maybe[TA], fallback: TB, map_: Callable[[TA], TB]) -> TB:
        return maybe(fallback, map_, self)

    def replace(self, value: TB) -> Maybe[TB]:
        return replace(self, value)

    def to_optional(self) -> Optional[TA]:  # pylint: disable=unsubscriptable-object
        return to_optional(self)

    @staticmethod
    def of(value: TA):  # pylint: disable=invalid-name
        return Maybe.pure(value)

    @staticmethod
    def pure(value: TA):
        return pure(value)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Maybe):
            return False

        if __o.is_nothing() or self.is_nothing():
            return __o.is_nothing() and self.is_nothing()

        return __o.value == self.value


class Just(Maybe[TA]):  # pylint: disable=too-few-public-methods
    value: TA

    def __init__(self, value: TA):
        self.value = value

    def __str__(self) -> str:
        return f"Just({self.value.__str__()})"


class Nothing(Maybe[TA]):  # pylint: disable=too-few-public-methods
    def __str__(self) -> str:
        return "Nothing"


nothing: Nothing = Nothing()


def __identity(value):
    return value


def bind(em0: Maybe[TA], map_: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
    if is_nothing(em0):
        return nothing

    result = map_(em0.value)
    if not isinstance(result, Maybe):
        raise ArgumentTypeError("Bind should return Maybe")

    return result


def fmap(em0: Maybe[TA], map_: Callable[[TA], TB]) -> Maybe[TB]:
    return bind(em0, lambda m0: Just(map_(m0)))


def from_maybe(fallback: TB, em0: Maybe[TA]) -> TB:
    return maybe(fallback, __identity, em0)


def is_nothing(em0: Maybe[TA]) -> bool:
    return isinstance(em0, Nothing)


def maybe(fallback: TB, map_: Callable[[TA], TB], em0: Maybe[TA]) -> TB:
    return fallback if is_nothing(em0) else map_(em0.value)


def replace(self, value: TB) -> Maybe[TB]:
    return fmap(self, _const(value))


def to_optional(
    em0: Maybe[TA],
) -> Optional[TA]:  # pylint: disable=unsubscriptable-object
    return maybe(None, _identity, em0)


def of(value: TA) -> Maybe[TA]:  # pylint: disable=invalid-name
    return nothing if value is None else Just(value)


pure = of  # pylint: disable=invalid-name
