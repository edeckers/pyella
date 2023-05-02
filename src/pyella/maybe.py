# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.


"""
Maybe - Contains the Maybe type and related functions. Its implementation
was strongly inspired by the Haskell ``Data.Maybe`` type.

More information on the Haskell ``Data.Maybe`` type can be found here:
https://hackage.haskell.org/package/base/docs/Data-Maybe.html
"""

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, Optional, TypeVar

from pyella.shared import _const, _identity

TA = TypeVar("TA")  # pylint: disable=invalid-name
TB = TypeVar("TB")  # pylint: disable=invalid-name


class Maybe(Generic[TA]):  # pylint: disable=too-few-public-methods
    """
    Provides a way to handle values that may or may not be present: A value of
    type ``Maybe[A]`` is either ``Nothing`` or ``Just[A]``.
    """

    value: TA

    def bind(self, apply: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
        """
        Alias for :py:func:`bind(self, apply) <bind>`
        """
        return bind(self, apply)

    def chain(self, em1: Maybe[TB]) -> Maybe[TB]:
        """
        Alias for :py:func:`chain(self, em1) <chain>`
        """
        return chain(self, em1)

    def discard(self, apply: Callable[[TA], Maybe[TB]]) -> Maybe[TA]:
        """
        Alias for :py:func:`discard(self, apply) <discard>`
        """
        return discard(self, apply)

    def fmap(self, apply: Callable[[TA], TB]) -> Maybe[TB]:
        """
        Alias for :py:func:`fmap(self, apply) <fmap>`
        """
        return fmap(self, apply)

    def from_maybe(self, fallback: TA) -> TA:
        """
        Alias for :py:func:`from_maybe(fallback, self) <from_maybe>`
        """
        return from_maybe(fallback, self)

    def is_nothing(self) -> bool:
        """
        Alias for :py:func:`is_nothing(self) <is_nothing>`
        """
        return is_nothing(self)

    def maybe(self: Maybe[TA], fallback: TB, apply: Callable[[TA], TB]) -> TB:
        """
        Alias for :py:func:`maybe(fallback, apply, self) <maybe>`
        """
        return maybe(fallback, apply, self)

    def replace(self, value: TB) -> Maybe[TB]:
        """
        Alias for :py:func:`replace(self, value) <replace>`
        """
        return replace(self, value)

    def to_optional(self) -> Optional[TA]:  # pylint: disable=unsubscriptable-object
        """
        Alias for :py:func:`to_optional(self) <to_optional>`
        """
        return to_optional(self)

    @staticmethod
    def of(value: TA):  # pylint: disable=invalid-name
        """
        Alias for :py:func:`of(value) <of>`
        """
        return of(value)

    @staticmethod
    def pure(value: TA):
        """
        Alias for :py:func:`pure(value) <pure>`
        """
        return pure(value)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Maybe):
            return False

        if __o.is_nothing() or self.is_nothing():
            return __o.is_nothing() and self.is_nothing()

        return __o.value == self.value


class Just(Maybe[TA]):  # pylint: disable=too-few-public-methods
    """
    An instance of type ``Just[A]`` contains a value of type ``A``.
    """

    value: TA

    def __init__(self, value: TA):
        self.value = value

    def __str__(self) -> str:
        return f"Just({self.value.__str__()})"


class Nothing(Maybe[TA]):  # pylint: disable=too-few-public-methods
    """
    An instance of type ``Nothing`` contains no value.
    """

    def __str__(self) -> str:
        return "Nothing"


nothing: Nothing = Nothing()


def bind(em0: Maybe[TA], apply: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
    """
    Map the value of a :py:class:`Just[TA] <Just>` to a new :py:class:`Maybe[TB] <Maybe>`

    :raises ArgumentTypeError: If the result of the apply function is not a :py:class:`Maybe`

    .. note:: Haskell: `>>= <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:-62--62--61->`_
    """
    if is_nothing(em0):
        return nothing

    result = apply(em0.value)
    if not isinstance(result, Maybe):
        raise ArgumentTypeError("Bind should return Maybe")

    return result


def chain(em0: Maybe[TA], em1: Maybe[TB]) -> Maybe[TB]:
    """
    Discard the current value of a :py:class:`Just[TA] <Just>` and replace it with the given :py:class:`Maybe[TA] <Maybe>`

    .. note:: Haskell: `>> <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:-62--62->`_
    """
    return bind(em0, lambda _: em1)


def discard(em0: Maybe[TA], apply: Callable[[TA], Maybe[TB]]) -> Maybe[TA]:
    """
    Apply the given function to the value of a :py:class:`Just[TA] <Just>` and discard the result
    """
    return em0.bind(apply).chain(em0)


def fmap(em0: Maybe[TA], apply: Callable[[TA], TB]) -> Maybe[TB]:
    """
    Map a function over the value of a :py:class:`Maybe[TA] <Maybe>` when it's :py:class:`Just[TA] <Just>`, otherwise return :py:class:`Nothing`

    .. note:: Haskell: `fmap <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:fmap>`_
    """
    return bind(em0, lambda m0: Just(apply(m0)))


def from_maybe(fallback: TA, em0: Maybe[TA]) -> TA:
    """
    Return the value of a Maybe when it's Just, otherwise return a fallback value

    .. note:: Haskell: `fromMaybe <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:fromMaybe>`_
    """
    return maybe(fallback, _identity, em0)


def is_nothing(em0: Maybe[TA]) -> bool:
    """
    Is the given Maybe Nothing?

    .. note:: Haskell: `isNothing <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:isNothing>`_
    """
    return isinstance(em0, Nothing)


def maybe(fallback: TB, apply: Callable[[TA], TB], em0: Maybe[TA]) -> TB:
    """
    Map and return the value of the given :py:class:`Maybe[TA]` when it's :py:class:`Just[TA] <Just>`, otherwise return a fallback value

    :return: Mapped :py:class:`Just` value or fallback when :py:class:`Nothing`

    .. note:: Haskell: `pure <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:maybe>`_
    """
    return fallback if is_nothing(em0) else apply(em0.value)


def replace(em0: Maybe[TA], value: TB) -> Maybe[TB]:
    """
    Replace the value of a :py:class:`Maybe` with a new value.

    :return: :py:class:`Nothing` if the :py:class:`Maybe` is :py:class:`Nothing`, otherwise a :py:class:`Just` with provided value

    .. note:: Haskell: `<$ <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:-60--36->`__
    """
    return fmap(em0, _const(value))


def pure(value: TA):
    """
    Create a :py:class:`Maybe[TA] <Maybe>` from a value

    :return: :py:class:`Nothing` if the value is ``None``, otherwise :py:class:`Just(value) <Just>`

    .. note:: Haskell: `pure <https://hackage.haskell.org/package/base/docs/Data-Maybe.html#v:pure>`__
    """
    return nothing if value is None else Just(value)


def to_optional(
    em0: Maybe[TA],
) -> Optional[TA]:  # pylint: disable=unsubscriptable-object
    """
    Convert a :py:class:`Maybe[TA] <Maybe>` to an
    `Optional[TA] <https://docs.python.org/3/library/typing.html#typing.Optional>`_

    :return: ``None`` if the :py:class:`Maybe` is :py:class:`Nothing`, otherwise its value
    """
    return maybe(None, _identity, em0)


def of(value: TA) -> Maybe[TA]:  # pylint: disable=invalid-name
    """
    Alias for :py:func:`pure(value) <bind>`
    """
    return pure(value)
