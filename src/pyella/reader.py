# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

"""
Reader - Contains the :py:class:`Reader[TE, TA] <Reader>` type and related
functions. It was strongly inspired by the Haskell ``Control.Monad.Reader`` module.

More information on the Haskell ``Control.Monad.Reader`` type can be found here:
https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from pyella.shared import _const

TE_co = TypeVar("TE_co", covariant=True)  # pylint: disable=invalid-name
TA_co = TypeVar("TA_co", covariant=True)  # pylint: disable=invalid-name
TC_co = TypeVar("TC_co", covariant=True)  # pylint: disable=invalid-name


@dataclass(frozen=True)
class Reader(Generic[TE_co, TA_co]):  # pylint: disable=too-few-public-methods
    """
    Represents a computation, which can read values from a shared environment, pass values from function to function,
    and execute sub-computations in a modified environment.
    """

    run_reader: Callable[[TE_co], TA_co]

    def bind(
        self, apply: Callable[[TA_co], Reader[TE_co, TC_co]]
    ) -> Reader[TE_co, TC_co]:
        """
        Alias for :py:func:`bind(self, apply) <bind>`
        """
        return bind(self, apply)

    def chain(self, em1: Reader[TE_co, TC_co]) -> Reader[TE_co, TC_co]:
        """
        Alias for :py:func:`chain(self, em1) <chain>`
        """
        return chain(self, em1)

    def discard(
        self, apply: Callable[[TA_co], Reader[TE_co, TA_co]]
    ) -> Reader[TE_co, TA_co]:
        """
        Alias for :py:func:`discard(self, apply) <discard>`
        """
        return discard(self, apply)

    def fmap(self, apply: Callable[[TA_co], TC_co]) -> Reader[TE_co, TC_co]:
        """
        Alias for :py:func:`fmap(self, apply) <fmap>`
        """
        return fmap(self, apply)

    @staticmethod
    def pure(
        run_reader: Callable[[TE_co], TA_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
    ) -> Reader[TE_co, TA_co]:  # pylint: disable=invalid-name
        """
        Alias for :py:func:`pure(run_reader) <pure>`
        """
        return pure(run_reader)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Reader):
            return False

        return __o.run_reader == self.run_reader


def ask() -> Reader[TE_co, TE_co]:  # type: ignore [misc] # covariant arg ok, b/c function is pure
    """
    Retrieves the monad environment.

    .. note:: Haskell: `ask <https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html#v:ask>`__
    """
    return Reader(lambda v: v)


def bind(
    em0: Reader[TE_co, TA_co], apply: Callable[[TA_co], Reader[TE_co, TC_co]]
) -> Reader[TE_co, TC_co]:
    """
    Passes the inherited environment to both subcomputations, first the original `Reader [TE, TA]` and
    then the result of the function `TA -> Reader [TE, TC]`

    .. note:: Haskell: `>>= <https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html#v:-62--62--61->`__
    """

    def _bind(environment: TE_co) -> TC_co:  # type: ignore [misc] # covariant arg ok, b/c function is pure
        environment_1 = em0.run_reader(environment)

        return apply(environment_1).run_reader(environment)

    return Reader(_bind)


def chain(
    em0: Reader[TC_co, TE_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
    em1: Reader[TC_co, TA_co],
) -> Reader[TC_co, TA_co]:
    """
    Discard the current value of a :py:class:`Reader[TE,TA] <Reader>` and replace it with the given :py:class:`Reader[TC, TB] <Reader>`

    .. note:: Haskell: `>> <https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html#v:-62--62->`__
    """
    return bind(em0, lambda _: em1)


def discard(
    em0: Reader[TC_co, TE_co], apply: Callable[[TE_co], Reader[TC_co, TA_co]]
) -> Reader[TC_co, TE_co]:
    """
    Apply the given function to the value of a :py:class:`Reader[TE,TA] <Reader>` and discard the result
    """
    return em0.bind(apply).chain(em0)


def replace(
    self, value: TC_co  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> Reader[TE_co, TC_co]:
    """
    Replace the value of an :py:class:`Reader` with a new value

    :return: a :py:class:`Reader[TE,TA] <Reader>` with provided value

    .. note:: Haskell: `<$ <https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html#v:-60--36->`__
    """
    return fmap(self, _const(value))


def fmap(
    em0: Reader[TE_co, TA_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
    apply: Callable[[TA_co], TC_co],
) -> Reader[TE_co, TC_co]:  # type: ignore [misc] # covariant arg ok, b/c function is pure
    """
    Map a function over the value of a :py:class:`Reader[TE,TA] <Reader>`

    .. note:: Haskell: `fmap <https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html>`__
    """
    return bind(em0, lambda m0: pure(lambda _: apply(m0)))


def pure(
    run_reader: Callable[[TE_co], TA_co],  # type: ignore [misc] # covariant arg ok, b/c function is pure
) -> Reader[TE_co, TA_co]:
    """
    Create a :py:class:`Reader[TE,TA] <Reader>` from a function

    .. note:: Haskell: `pure <https://hackage.haskell.org/package/mtl-2.3.1/docs/Control-Monad-Reader.html#v:pure>`__
    """
    return Reader(run_reader)
