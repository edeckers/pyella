# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

"""
This script contains shared functions and types used by the
other modules in this library. It is not intended to be used
outside of it. 
"""

from typing import Any, Callable, TypeVar

TA = TypeVar("TA")  # pylint: disable=invalid-name


def _const(value: TA) -> Callable[[Any], TA]:
    return lambda _: value


def _identity(value: TA) -> TA:
    return value
