# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, Iterable, List, Optional, TypeVar, Union, cast

from pyella.maybe import Maybe, nothing
from pyella.shared import _const

TA = TypeVar("TA")  # pylint: disable=invalid-name
TB = TypeVar("TB")  # pylint: disable=invalid-name
TC = TypeVar("TC")  # pylint: disable=invalid-name
TD = TypeVar("TD")  # pylint: disable=invalid-name

"""
The Either type represents values with two possibilities: a value of type
`Either[TA, TB]` is either `Left[TA]` or `Right[TB]`. Its implementation was
closely inspired by the Haskell `Data.Either` type.

More information on the Haskell `Data.Either` type can be found here:
https://hackage.haskell.org/package/base/docs/Data-Either.html
"""


class Either(Generic[TA, TB]):  # pylint: disable=too-few-public-methods
    value: Union[TA, TB]  # pylint: disable=unsubscriptable-object

    def bind(self, map_: Callable[[TB], Either[TA, TC]]) -> Either[TA, TC]:
        """
        Alias for bind(self, map_)
        """
        return bind(self, map_)

    def chain(self, em1: Either[TA, TC]) -> Either[TA, TC]:
        """
        Alias for chain(self, em1)
        """
        return chain(self, em1)

    def discard(self, map_: Callable[[TB], Either[TA, TB]]) -> Either[TA, TB]:
        """
        Alias for discard(self, map_)
        """
        return discard(self, map_)

    def either(
        self, map_left_: Callable[[TA], TC], map_right_: Callable[[TB], TC]
    ) -> TC:
        """
        Alias for either(map_left, map_right, self)
        """
        return either(map_left_, map_right_, self)

    def fmap(self, map_: Callable[[TB], TC]) -> Either[TA, TC]:
        """
        Alias for fmap(self, map_)
        """
        return fmap(self, map_)

    def if_left(self, fallback: TB) -> TB:
        """
        Alias for if_left(self, fallback)
        """
        return if_left(self, fallback)

    def if_right(self, fallback: TA) -> TA:
        """
        Alias for if_right(self, fallback)
        """
        return if_right(self, fallback)

    def is_left(self) -> bool:
        """
        Alias for is_left(self)
        """
        return is_left(self)

    def is_right(self) -> bool:
        """
        Alias for is_right(self)
        """
        return is_right(self)

    def map_left(self, map_: Callable[[TA], TC]) -> Either[TC, TB]:
        """
        Alias for map_left(self, map_)
        """
        return map_left(self, map_)

    def replace(self, value: TC) -> Either[TA, TC]:
        """
        Alias for replace(self, value)
        """
        return replace(self, value)

    def to_maybe(self) -> Maybe[TB]:
        """
        Alias for to_maybe(self)
        """
        return to_maybe(self)

    def to_optional(self) -> Optional[TB]:  # pylint: disable=unsubscriptable-object
        """
        Alias for to_optional(self)
        """
        return to_optional(self)

    @staticmethod
    def pure(value: TB) -> Either[TA, TB]:  # pylint: disable=invalid-name
        """
        Alias for pure(self)
        """
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
    """
    Haskell: `>>=`

    Map the value of a Right to a new Either, i.e. a new Right or Left
    """
    if is_left(em0):
        return cast(Left[TC, TB], em0)

    result = map_(cast(TA, em0.value))
    if not isinstance(result, Either):
        raise ArgumentTypeError("Bind should return Either")

    return result


def chain(em0: Either[TC, TA], em1: Either[TC, TB]) -> Either[TC, TB]:
    """
    Haskell: `>>`

    Discard the current value of a Right and replace it with the given Either
    """
    return bind(em0, lambda _: em1)


def discard(
    em0: Either[TC, TA], map_: Callable[[TA], Either[TC, TB]]
) -> Either[TC, TA]:
    """
    Apply the given function to the value of a Right and discard the result
    """
    return em0.bind(map_).chain(em0)


def replace(self, value: TC) -> Either[TA, TC]:
    """
    Haskell: `(<$)`

    Replace the value of an Either with a new value

    Returns itself if the Either is Left, otherwise a Right with provided value
    """
    return fmap(self, _const(value))


def either(
    map_left_: Callable[[TA], TC], map_right_: Callable[[TB], TC], em0: Either[TA, TB]
) -> TC:
    """
    Haskell: `either`

    Map the value of the given Either with `map_right` if its Right or
    with `map_left` when it's Left.
    """
    return (
        map_left_(cast(TA, em0.value))
        if is_left(em0)
        else map_right_(cast(TB, em0.value))
    )


def fmap(em0: Either[TC, TA], map_: Callable[[TA], TB]) -> Either[TC, TB]:
    """
    Haskell: `fmap`

    Map a function over the value of an Either when it's Right, otherwise return
    itself
    """
    return bind(em0, lambda m0: pure(map_(m0)))


def map_left(em0: Either[TA, TB], map_: Callable[[TA], TC]) -> Either[TC, TB]:
    """
    Haskell: `fmap`

    Map a function over the value of an Either when it's Left, otherwise return
    itself
    """
    return either(lambda e: left(map_(e)), right, em0)


def if_left(em0: Either[TA, TB], fallback: TB) -> TB:
    """
    Haskell: `fromRight`

    Return the contents of a Right or a fallback value if it's Left
    """
    return fallback if em0.is_left() else cast(TB, em0.value)


def if_right(em0: Either[TA, TB], fallback: TA) -> TA:
    """
    Haskell: `fromLeft`

    Return the contents of a Left or a fallback value if it's Right
    """
    return fallback if em0.is_right() else cast(TA, em0.value)


def is_left(em0: Either[TA, TB]) -> bool:
    """
    Haskell: `isLeft`

    Is the given Either a Left?
    """
    return isinstance(em0, Left)


def is_right(em0: Either[TA, TB]) -> bool:
    """
    Haskell: `isRight`

    Is the given Either a Right?
    """
    return not is_left(em0)


def lefts(eithers: Iterable[Either[TA, TB]]) -> List[TA]:
    """
    Haskell: `lefts`

    Return a list of all the Left values in the given list of Eithers
    """
    return list(map(lambda either: cast(TA, either.value), filter(is_left, eithers)))


def rights(eithers: Iterable[Either[TA, TB]]) -> List[TB]:
    """
    Haskell: `rights`

    Return a list of all the Right values in the given list of Eithers
    """
    return list(map(lambda either: cast(TB, either.value), filter(is_right, eithers)))


def left(value: TA) -> Left[TA, TB]:
    "Create a Left with the given value"
    return Left(value)


def right(value: TB) -> Right[TA, TB]:
    "Alias for pure(value)"
    return pure(value)


def to_maybe(
    em0: Either[TA, TB]
) -> Maybe[TB]:  # pylint: disable=unsubscriptable-object
    """
    Haskell: `toMaybe`

    Convert an Either to a Maybe by mapping Left to Nothing and Right to Just
    """
    return either(lambda _: nothing, lambda v: Maybe.of(cast(TB, v)), em0)


def to_optional(
    em0: Either[TA, TB]
) -> Optional[TB]:  # pylint: disable=unsubscriptable-object
    """
    Convert an Either to an Optional by mapping Left to None and Right to its value
    """
    return to_maybe(em0).to_optional()


def pure(value: TA):
    """
    Haskell: `pure`

    Create a Right from a value
    """
    return Right(value)
