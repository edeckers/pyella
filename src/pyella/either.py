# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

"""
Either - Contains the :py:class:`Either[TA, TB] <Either>` type and related
functions. It was strongly inspired by the Haskell ``Data.Either`` module.

More information on the Haskell ``Data.Either`` type can be found here:
https://hackage.haskell.org/package/base/docs/Data-Either.html
"""

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, Iterable, List, Optional, TypeVar, Union, cast

from pyella.maybe import Maybe, nothing
from pyella.shared import _const

TA_co = TypeVar("TA_co", covariant=True)  # pylint: disable=invalid-name
TB_co = TypeVar("TB_co", covariant=True)  # pylint: disable=invalid-name
TC_co = TypeVar("TC_co", covariant=True)  # pylint: disable=invalid-name


class Either(Generic[TA_co, TB_co]):  # pylint: disable=too-few-public-methods
    """
    Represents values with two possibilities: a value of type
    :py:class:`Either[TA, TB] <Either>` is either :py:class:`Left[TA] <Left>` or
    :py:class:`Right[TB] <Right>`.
    """

    value: Union[TA_co, TB_co]  # pylint: disable=unsubscriptable-object

    def bind(
        self, apply: Callable[[TB_co], Either[TA_co, TC_co]]
    ) -> Either[TA_co, TC_co]:
        """
        Alias for :py:func:`bind(self, apply) <bind>`
        """
        return bind(self, apply)

    def chain(self, em1: Either[TA_co, TC_co]) -> Either[TA_co, TC_co]:
        """
        Alias for :py:func:`chain(self, em1) <chain>`
        """
        return chain(self, em1)

    def discard(
        self, apply: Callable[[TB_co], Either[TA_co, TB_co]]
    ) -> Either[TA_co, TB_co]:
        """
        Alias for :py:func:`discard(self, apply) <discard>`
        """
        return discard(self, apply)

    def either(
        self, map_left_: Callable[[TA_co], TC_co], map_right_: Callable[[TB_co], TC_co]
    ) -> TC_co:
        """
        Alias for :py:func:`either(map_left, map_right, self) <either>`
        """
        return either(map_left_, map_right_, self)

    def fmap(self, apply: Callable[[TB_co], TC_co]) -> Either[TA_co, TC_co]:
        """
        Alias for :py:func:`fmap(self, apply) <fmap>`
        """
        return fmap(self, apply)

    def if_left(
        self,
        fallback: TB_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
    ) -> TB_co:
        """
        Alias for :py:func:`if_left(self, fallback) <if_left>`
        """
        return if_left(self, fallback)

    def if_right(
        self,
        fallback: TA_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
    ) -> TA_co:
        """
        Alias for :py:func:`if_right(self, fallback) <if_right>`
        """
        return if_right(self, fallback)

    def is_left(self) -> bool:
        """
        Alias for :py:func:`is_left(self) <is_left>`
        """
        return is_left(self)

    def is_right(self) -> bool:
        """
        Alias for :py:func:`is_right(self) <is_right>`
        """
        return is_right(self)

    def map_left(self, apply: Callable[[TA_co], TC_co]) -> Either[TC_co, TB_co]:
        """
        Alias for :py:func:`map_left(self, apply) <map_left>`
        """
        return map_left(self, apply)

    def replace(
        self, value: TC_co  # type: ignore [misc] # covariant arg ok, b/c function is pure
    ) -> Either[TA_co, TC_co]:
        """
        Alias for :py:func:`replace(self, value) <replace>`
        """
        return replace(self, value)

    def to_maybe(self) -> Maybe[TB_co]:
        """
        Alias for :py:func:`to_maybe(self) <to_maybe>`
        """
        return to_maybe(self)

    def to_optional(self) -> Optional[TB_co]:  # pylint: disable=unsubscriptable-object
        """
        Alias for :py:func:`to_optional(self) <to_optional>`
        """
        return to_optional(self)

    @staticmethod
    def pure(
        value: TB_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
    ) -> Either[TA_co, TB_co]:  # pylint: disable=invalid-name
        """
        Alias for :py:func:`pure(self) <pure>`
        """
        return pure(value)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Either):
            return False

        if __o.is_left() or self.is_left():
            return __o.is_left() and self.is_left() and __o.value == self.value

        return __o.value == self.value


class Left(Either[TA_co, TB_co]):  # pylint: disable=too-few-public-methods
    """
    Represents the left side of an :py:class:`Either[TA, TB] <Either>`, often
    used to represent the failure case
    """

    def __init__(self, value: TA_co):
        self.value = value

    def __str__(self) -> str:
        return f"Left({self.value.__str__()})"


class Right(Either[TA_co, TB_co]):  # pylint: disable=too-few-public-methods
    """
    Represents the right side of an :py:class:`Either[TA, TB] <Either>`, often
    used to represent the success case
    """

    def __init__(self, value: TB_co):
        self.value = value

    def __str__(self) -> str:
        return f"Right({self.value.__str__()})"


def bind(
    em0: Either[TC_co, TA_co], apply: Callable[[TA_co], Either[TC_co, TB_co]]
) -> Either[TC_co, TB_co]:
    """
    Map the value of a :py:class:`Right[TA] <Right>` to a new :py:class:`Either[TC, TB] <Either>`

    :raises ArgumentTypeError: If the result of the apply function is not a :py:class:`Either`

    :return: A new :py:class:`Right[TB]` or :py:class:`Left[TC]`

    .. note:: Haskell: `>>= <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:-62--62--61->`__
    """
    if is_left(em0):
        return cast(Left[TC_co, TB_co], em0)

    result = apply(cast(TA_co, em0.value))
    if not isinstance(result, Either):
        raise ArgumentTypeError("Bind should return :py:class:`Either`")

    return result


def chain(
    em0: Either[TC_co, TA_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
    em1: Either[TC_co, TB_co],
) -> Either[TC_co, TB_co]:
    """
    Discard the current value of a :py:class:`Right[TA] <Right>` and replace it with the given :py:class:`Either[TC, TB] <Either>`

    .. note:: Haskell: `>> <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:-62--62->`__
    """
    return bind(em0, lambda _: em1)


def discard(
    em0: Either[TC_co, TA_co], apply: Callable[[TA_co], Either[TC_co, TB_co]]
) -> Either[TC_co, TA_co]:
    """
    Apply the given function to the value of a :py:class:`Right[TA] <Right>` and discard the result
    """
    return em0.bind(apply).chain(em0)


def replace(
    self, value: TC_co  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> Either[TA_co, TC_co]:
    """
    Replace the value of an :py:class:`Either` with a new value

    :return: itself if the :py:class:`Either` is :py:class:`Left`, otherwise a :py:class:`Right[TC] <Right>` with provided value

    .. note:: Haskell: `<$ <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:-60--36->`__
    """
    return fmap(self, _const(value))


def either(
    map_left_: Callable[[TA_co], TC_co],
    map_right_: Callable[[TB_co], TC_co],
    em0: Either[TA_co, TB_co],
) -> TC_co:
    """
    Map the value of the given :py:class:`Either` with `map_right_` if its :py:class:`Right` or
    with `map_left_` when it's :py:class:`Left`.

    .. note:: Haskell: `either <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:either>`_
    """
    return (
        map_left_(cast(TA_co, em0.value))
        if is_left(em0)
        else map_right_(cast(TB_co, em0.value))
    )


def fmap(
    em0: Either[TC_co, TA_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
    apply: Callable[[TA_co], TB_co],
) -> Either[TC_co, TB_co]:
    """
    Map a function over the value of an :py:class:`Either` when it's :py:class:`Right[TA] <Right>`, otherwise return
    itself

    .. note:: Haskell: `fmap <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:fmap>`__
    """
    return bind(em0, lambda m0: pure(apply(m0)))


def map_left(
    em0: Either[TA_co, TB_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
    apply: Callable[[TA_co], TC_co],
) -> Either[TC_co, TB_co]:
    """
    Map a function over the value of an :py:class:`Either` when it's :py:class:`Left`, otherwise return
    itself

    .. note:: Haskell: `first <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:first>`_
    """
    return either(lambda e: left(apply(e)), right, em0)


def if_left(
    em0: Either[TA_co, TB_co],
    fallback: TB_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> TB_co:
    """
    Return the contents of a :py:class:`Right[TB] <Right>` or a fallback value if it's :py:class:`Left`

    .. note:: Haskell: `fromRight <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:fromRight>`_
    """
    return fallback if em0.is_left() else cast(TB_co, em0.value)


def if_right(
    em0: Either[TA_co, TB_co],
    fallback: TA_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> TA_co:
    """
    Return the contents of a :py:class:`Left` or a fallback value if it's :py:class:`Right`

    .. note:: Haskell: `fromLeft <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:fromLeft>`_
    """
    return fallback if em0.is_right() else cast(TA_co, em0.value)


def is_left(em0: Either[TA_co, TB_co]) -> bool:
    """
    Is the given :py:class:`Either` a :py:class:`Left`?

    .. note:: Haskell: `isLeft <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:isLeft>`_
    """
    return isinstance(em0, Left)


def is_right(em0: Either[TA_co, TB_co]) -> bool:
    """
    Is the given :py:class:`Either` a :py:class:`Right`?

    .. note:: Haskell: `isRight <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:isRight>`_
    """
    return not is_left(em0)


def lefts(eithers: Iterable[Either[TA_co, TB_co]]) -> List[TA_co]:
    """
    Return a list of all the :py:class:`Left` values in the given list of :py:class:`Eithers <Either>`

    .. note:: Haskell: `lefts <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:lefts>`_
    """
    return list(map(lambda either: cast(TA_co, either.value), filter(is_left, eithers)))


def rights(eithers: Iterable[Either[TA_co, TB_co]]) -> List[TB_co]:
    """
    Return a list of all the :py:class:`Right` values in the given list of :py:class:`Eithers <Either>`

    .. note:: Haskell: `rights <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:rights>`_
    """
    return list(
        map(lambda either: cast(TB_co, either.value), filter(is_right, eithers))
    )


def left(
    value: TA_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> Left[TA_co, TB_co]:
    "Create a :py:class:`Left[TA] <Left>` with the given value"
    return Left(value)


def right(
    value: TB_co,  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> Right[TA_co, TB_co]:
    "Alias for :py:func:`pure(value) <pure>`"
    return pure(value)


def to_maybe(
    em0: Either[TA_co, TB_co]  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> Maybe[TB_co]:  # pylint: disable=unsubscriptable-object
    """
    Convert an :py:class:`Either[TA, TB] <Either>` to a :py:class:`Maybe[TB] <Maybe>` by
    mapping :py:class:`Left` to :py:class:`Nothing` and :py:class:`Right` to :py:class:`Just[TB] <Just>`

    .. note:: Haskell: `toMaybe <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:toMaybe>`_
    """
    return either(lambda _: nothing, lambda v: Maybe.of(cast(TB_co, v)), em0)


def to_optional(
    em0: Either[TA_co, TB_co]
) -> Optional[TB_co]:  # pylint: disable=unsubscriptable-object
    """
    Convert an :py:class:`Either[TA, TB] <Either>` to an
    `Optional[TB] <https://docs.python.org/3/library/typing.html#typing.Optional>`_
    by mapping :py:class:`Left[TA] <Left>` to ``None`` and :py:class:`Right[TB] <Right>`
    to its value

    :return: ``None`` if the :py:class:`Either` is :py:class:`Left`, otherwise its value
    """
    return to_maybe(em0).to_optional()


def pure(value: TA_co):  # type: ignore [misc] # covariant arg ok, b/c function is pure
    """
    Create a :py:class:`Right[TA] <Right>` from a value

    .. note:: Haskell: `pure <https://hackage.haskell.org/package/base/docs/Data-Either.html#v:pure>`__
    """
    return Right(value)
