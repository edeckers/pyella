# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.


# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import unittest
from dataclasses import dataclass
from random import randint

from pyella.reader import Reader, ask, bind, pure
from pyella.shared import _const


@dataclass(frozen=True)
class Environment:
    some_value: int


class TestReader(unittest.TestCase):
    def test_reader_objects_compare_correctly(self):
        # arrange
        def times2(some_value: int):
            return some_value * 2

        def times3(some_value: int):
            return some_value * 3

        r0_2 = Reader(times2)
        r1_2 = Reader(times2)

        r2_3 = Reader(times3)

        # act
        # assert
        self.assertEqual(
            r0_2,
            r1_2,
            "The given Reader-objects contain the same function, so they should be considered Equal",
        )
        self.assertNotEqual(
            r0_2,
            r2_3,
            # pylint: disable=line-too-long
            "The given Reader-objects contain different functions, so they should be considered Not Equal",
        )

    def test_reader_reads_and_applies_environment_data_correctly(self):
        # arrange

        random_value = randint(0, 100)  # nosec # B311 random in test is safe

        environment = Environment(random_value)

        def times2(env: Environment) -> int:
            return env.some_value * 2

        def multiply_env_by_2() -> Reader[Environment, int]:
            return bind(ask(), lambda env: pure(_const(times2(env))))

        def env_multiplication_as_tuple() -> Reader[Environment, tuple[str, int]]:
            return multiply_env_by_2().fmap(lambda x: (str(x), x))

        # act
        result_str, result_int = env_multiplication_as_tuple().run_reader(environment)

        # assert
        expected_int = 2 * random_value

        self.assertEqual(
            str(expected_int),
            result_str,
            "The resulting string position of the tuple doesn't match the expected integer",
        )
        self.assertEqual(
            expected_int,
            result_int,
            "The resulting integer position of the tuple doesn't match the expected integer",
        )
