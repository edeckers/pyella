# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, Iterable, List, Optional, TypeVar, Union, cast

from pyella.maybe import Maybe, nothing
from pyella.shared import _const

TA = TypeVar("TA")
TB = TypeVar("TB")
TC = TypeVar("TC")
TD = TypeVar("TD")


class Either(Generic[TA, TB]):  # pylint: disable=too-few-public-methods
    value: Union[TA, TB]  # pylint: disable=unsubscriptable-object

    def bind(self, map_: Callable[[TB], Either[TA, TC]]) -> Either[TA, TC]:
        return bind(self, map_)

    def chain(self, em1: Either[TA, TB]) -> Either[TA, TB]:
        return chain(self, em1)

    def discard(self, map_: Callable[[TB], Either[TA, TB]]) -> Either[TA, TB]:
        return self.bind(map_).chain(self)

    def either(
        self, map_left_: Callable[[TA], TC], map_right_: Callable[[TB], TC]
    ) -> TC:
        return either(map_left_, map_right_, self)

    def fmap(self, map_: Callable[[TB], TC]) -> Either[TA, TC]:
        return fmap(self, map_)

    def map_left(self, map_: Callable[[TA], TC]) -> Either[TC, TB]:
        return map_left(self, map_)

    def replace(self, value: TC) -> Either[TA, TC]:
        return replace(self, value)

    def if_left(self, fallback: TB) -> TB:
        return if_left(self, fallback)

    def if_right(self, fallback: TA) -> TA:
        return if_right(self, fallback)

    def is_left(self) -> bool:
        return is_left(self)

    def is_right(self) -> bool:
        return is_right(self)

    def to_maybe(self) -> Maybe[TB]:
        return to_maybe(self)

    def to_optional(self) -> Optional[TB]:  # pylint: disable=unsubscriptable-object
        return to_optional(self)

    @staticmethod
    def pure(value: TB) -> Either[TA, TB]:  # pylint: disable=invalid-name
        return pure(value)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Either):
            return False

        if __o.is_left() or self.is_left():
            return __o.is_left() and self.is_left() and __o.value == self.value

        return __o.value == self.value


class Left(Either[TA, TB]):  # pylint: disable=too-few-public-methods
    def __init__(self, value: TA):
        self.value = value

    def __str__(self) -> str:
        return f"Left({self.value.__str__()})"


class Right(Either[TA, TB]):  # pylint: disable=too-few-public-methods
    def __init__(self, value: TB):
        self.value = value

    def __str__(self) -> str:
        return f"Right({self.value.__str__()})"


def bind(em0: Either[TC, TA], map_: Callable[[TA], Either[TC, TB]]) -> Either[TC, TB]:
    if is_left(em0):
        return cast(Left[TC, TB], em0)

    result = map_(cast(TA, em0.value))
    if not isinstance(result, Either):
        raise ArgumentTypeError("Bind should return Either")

    return result


def chain(em0: Either[TC, TA], em1: Either[TC, TB]) -> Either[TC, TB]:
    return bind(em0, lambda _: em1)


def either(
    map_left_: Callable[[TA], TC], map_right_: Callable[[TB], TC], em0: Either[TA, TB]
) -> TC:
    return (
        map_left_(cast(TA, em0.value))
        if is_left(em0)
        else map_right_(cast(TB, em0.value))
    )


def fmap(em0: Either[TC, TA], map_: Callable[[TA], TB]) -> Either[TC, TB]:
    return bind(em0, lambda m0: pure(map_(m0)))


def map_left(em0: Either[TA, TB], map_: Callable[[TA], TC]) -> Either[TC, TB]:
    return either(lambda e: left(map_(e)), right, em0)


def if_left(em0: Either[TA, TB], fallback: TB) -> TB:
    return fallback if em0.is_left() else cast(TB, em0.value)


def if_right(em0: Either[TA, TB], fallback: TA) -> TA:
    return fallback if em0.is_right() else cast(TA, em0.value)


def is_left(em0: Either[TA, TB]) -> bool:
    return isinstance(em0, Left)


def is_right(em0: Either[TA, TB]) -> bool:
    return not is_left(em0)


def left(value: TA) -> Either[TA, TB]:
    return Left(value)


def lefts(eithers: Iterable[Either[TA, TB]]) -> List[TA]:
    return list(map(lambda either: cast(TA, either.value), filter(is_left, eithers)))


def replace(self, value: TC) -> Either[TA, TC]:
    return fmap(self, _const(value))


def rights(eithers: Iterable[Either[TA, TB]]) -> List[TB]:
    return list(map(lambda either: cast(TB, either.value), filter(is_right, eithers)))


def right(value: TB) -> Either[TA, TB]:
    return Right(value)


def to_maybe(
    em0: Either[TA, TB]
) -> Maybe[TB]:  # pylint: disable=unsubscriptable-object
    return either(lambda _: nothing, lambda v: Maybe.of(cast(TB, v)), em0)


def to_optional(
    em0: Either[TA, TB]
) -> Optional[TB]:  # pylint: disable=unsubscriptable-object
    return to_maybe(em0).to_optional()


pure = Right  # pylint: disable=invalid-name
