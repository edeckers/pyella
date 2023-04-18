# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import math
import unittest
from random import sample
from typing import List

from pyella.either import Either, Left, Right, either, left, lefts, pure, right, rights
from tests.fixtures import (
    identity,
    is_list_instance_of,
    random_int,
    random_str,
    unique_ints,
)


def _square(value: int) -> int:
    return int(math.pow(value, 2))


class TestEither(unittest.TestCase):
    def test_creation_of_either_with_right_returns_expected_results(self):
        # arrange
        # act
        some_random_value = random_str()
        results = list(map(lambda fn: fn(some_random_value), [Right, right, pure]))
        right_class, right_fn, right_pure = results

        # assert
        self.assertEqual(
            right_class,
            right_fn,
            "The methods `Right`, `right` and `pure` must yield the same results",
        )
        self.assertEqual(
            right_fn,
            right_pure,
            "The methods `Right`, `right` and `pure` must yield the same results",
        )
        self.assertTrue(
            is_list_instance_of(results, Right),
            "All values should be contained successully",
        )

    def test_creation_of_either_with_left_returns_expected_results(self):
        # arrange
        # act
        results = list(map(lambda fn: fn(None), [Left, left]))
        left_class_of, left_fn_of = results

        # assert
        self.assertEqual(
            left_class_of,
            left_fn_of,
            "The methods `Left` and `left` must yield the same results",
        )
        self.assertTrue(
            is_list_instance_of(results, Left),
            "All values should be contained successully",
        )

    def test_fmap_returns_expected_results(self):
        # arrange
        some_value = random_int()
        some_value_sq = _square(some_value)

        some_left_value = random_str()

        some_right = pure(some_value)
        some_left = left(some_left_value)

        # act
        right_result = some_right.fmap(_square)
        left_result = some_left.fmap(_square)

        # assert
        self.assertIsInstance(
            right_result,
            Right,
            "Calling `fmap` on Right should return Right with the mapping applied to its value",
        )
        self.assertEqual(
            some_value_sq,
            either(lambda _: -1, identity, right_result),
            "Calling `fmap` on Right should return Right with the mapping applied to its value",
        )
        self.assertEqual(
            -1,
            either(lambda _: -1, identity, left_result),
            "Calling `fmap` on Left should successfully return Left",
        )

    def test_map_left_returns_expected_results(self):
        # arrange
        some_value = random_str()

        some_left_value = random_int()
        some_value_sq = _square(some_left_value)

        some_right = pure(some_value)
        some_left = left(some_left_value)

        # act
        right_result = some_right.map_left(_square)
        left_result = some_left.map_left(_square)

        # assert
        self.assertIsInstance(
            left_result,
            Left,
            "Calling `map_left` on Left should return Left with the mapping applied to its value",
        )
        self.assertEqual(
            some_value_sq,
            either(identity, lambda _: -1, left_result),
            "Calling `map_left` on Left should return Left with the mapping applied to its value",
        )
        self.assertEqual(
            -1,
            either(identity, lambda _: -1, right_result),
            "Calling `map_left` on Right should successfully return Right",
        )

    def test_rights_and_lefts_return_expected_results(self):
        # arrange
        right_values = unique_ints()

        left_values = [random_str(), random_str()]

        some_rights: List[Right[str, int]] = list(map(right, right_values))
        some_lefts: List[Left[str, int]] = list(map(left, left_values))

        rights_and_lefts: List[Either[str, int]] = some_rights + some_lefts

        shuffled_results = sample(rights_and_lefts, len(rights_and_lefts))

        # act
        rights_result = sorted(rights(shuffled_results))
        lefts_result = sorted(lefts(shuffled_results))

        # assert
        self.assertListEqual(
            sorted(right_values),
            rights_result,
            # pylint: disable=line-too-long
            "Calling `rights` on a list of Eithers should return a list of their unwrapped Right values",
        )
        self.assertListEqual(
            sorted(left_values),
            lefts_result,
            # pylint: disable=line-too-long
            "Calling `lefts` on a list of Eithers should return a list of their unwrapped Left values",
        )

    def test_replace_returns_expected_results(self):
        # arrange
        some_value = random_str()
        some_value_2 = random_int()

        some_left_value = random_int()

        some_right = Either.pure(some_value)
        some_left = left(some_left_value)

        # act
        right_result = some_right.replace(some_value_2)
        left_result = some_left.replace(some_value_2)

        # assert
        self.assertIsInstance(
            left_result,
            Left,
            "Calling `replace` on Left should return unalterted Left value",
        )
        self.assertEqual(
            some_left_value,
            left_result.if_right(-1),
            "Calling `replace` on Left should return unalterted Left value",
        )
        self.assertEqual(
            some_value_2,
            right_result.if_left(-1),
            "Calling `replace` on Right should successfully return Right with new value",
        )
