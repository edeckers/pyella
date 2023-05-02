# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from random import randint, sample
from typing import Any, List
from uuid import uuid4


def is_list_instance_of(items: List[Any], clazz: type) -> bool:
    return len(items) == len(list(filter(lambda item: isinstance(item, clazz), items)))


def unique_ints(floor: int = 0, ceil: int = 10, sample_size: int = 10) -> List[int]:
    return sample(range(floor, ceil), sample_size)  # nosec


def random_int(floor: int = 0, ceil: int = 10) -> int:
    # B311 Standard pseudo-random generators are not suitable for security
    return randint(floor, ceil)  # nosec


def random_str() -> str:
    return uuid4().hex
