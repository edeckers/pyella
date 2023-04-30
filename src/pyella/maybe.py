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
        """
        Alias for bind(self, map_)
        """
        return bind(self, map_)

    def fmap(self, map_: Callable[[TA], TB]) -> Maybe[TB]:
        """
        Alias for fmap(self, map_)
        """
        return fmap(self, map_)

    def from_maybe(self, fallback: TA) -> TA:
        """
        Alias for from_maybe(fallback, self)
        """
        return from_maybe(fallback, self)

    def is_nothing(self) -> bool:
        """
        Alias for is_nothing(self)
        """
        return is_nothing(self)

    def maybe(self: Maybe[TA], fallback: TB, map_: Callable[[TA], TB]) -> TB:
        """
        Alias for maybe(fallback, map_, self)
        """
        return maybe(fallback, map_, self)

    def replace(self, value: TB) -> Maybe[TB]:
        """
        Alias for replace(self, value)
        """
        return replace(self, value)

    def to_optional(self) -> Optional[TA]:  # pylint: disable=unsubscriptable-object
        """
        Alias for to_optional(self)
        """
        return to_optional(self)

    @staticmethod
    def of(value: TA):  # pylint: disable=invalid-name
        """
        Alias for of(value)
        """
        return of(value)

    @staticmethod
    def pure(value: TA):
        """
        Alias for pure(value)
        """
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


def bind(em0: Maybe[TA], map_: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
    """
    Map the value of a Just to a new Maybe, i.e. a new Just or Nothing
    """
    if is_nothing(em0):
        return nothing

    result = map_(em0.value)
    if not isinstance(result, Maybe):
        raise ArgumentTypeError("Bind should return Maybe")

    return result


def fmap(em0: Maybe[TA], map_: Callable[[TA], TB]) -> Maybe[TB]:
    """
    Map a function over the value of a Maybe when it's Just, otherwise return Nothing
    """
    return bind(em0, lambda m0: Just(map_(m0)))


def from_maybe(fallback: TA, em0: Maybe[TA]) -> TA:
    """
    Return the value of a Maybe when it's Just, otherwise return a fallback value
    """
    return maybe(fallback, _identity, em0)


def is_nothing(em0: Maybe[TA]) -> bool:
    """
    Is the gievn Maybe Nothing?
    """
    return isinstance(em0, Nothing)


def maybe(fallback: TB, map_: Callable[[TA], TB], em0: Maybe[TA]) -> TB:
    """
    Map and return the given Maybe when it's Just, otherwise return a fallback value
    """
    return fallback if is_nothing(em0) else map_(em0.value)


def replace(em0: Maybe[TA], value: TB) -> Maybe[TB]:
    """
    Replace the value of a Maybe with a new value

    Returns Nothing if the Maybe is Nothing, otherwise a Just with provided value
    """
    to_value: Callable[[TA], TB] = _const(value)

    return fmap(em0, to_value)


def to_optional(
    em0: Maybe[TA],
) -> Optional[TA]:  # pylint: disable=unsubscriptable-object
    """
    Convert a Maybe to an Optional

    Returns None if the Maybe is Nothing, otherwise its value
    """
    return maybe(None, _identity, em0)


def of(value: TA) -> Maybe[TA]:  # pylint: disable=invalid-name
    """
    Alias for pure(value)
    """
    return pure(value)


def pure(value: TA):
    """
    Create a Maybe from a value

    Returns Nothing if the value is None, otherwise Just(value)
    """
    return nothing if value is None else Just(value)
