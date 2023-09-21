# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import math
import unittest
from argparse import ArgumentTypeError
from random import sample
from typing import Callable, List

import pytest  # pylint: disable=import-error

from pyella.either import Either, Left, Right, either, left, lefts, pure, right, rights
from pyella.maybe import nothing
from pyella.shared import _identity
from tests.fixtures import (
    BaseClass,
    SubClass,
    is_list_instance_of,
    random_int,
    random_str,
    unique_ints,
)


def _square(value: int) -> int:
    return int(math.pow(value, 2))


def _m_square(value: int) -> Either[str, int]:
    either_value: Either[str, int] = Either.pure(value)

    return either_value.fmap(_square)


# pylint: disable=unused-argument
def _m_fail(value: int) -> Either[str, int]:
    return left(random_str())


class TestEither(unittest.TestCase):
    def test_either_objects_compare_correctly(self):
        # arrange
        value_match, value_diff = unique_ints(sample_size=2)
        left_value = random_str()
        left_value_diff = random_str()

        right_match_0: Either[str, int] = Either.pure(value_match)
        right_match_1: Either[str, int] = Either.pure(value_match)
        right_diff: Either[str, int] = Either.pure(value_diff)

        left_match_0: Either[str, int] = left(left_value)
        left_match_1: Either[str, int] = left(left_value)
        left_diff: Either[str, int] = left(left_value_diff)

        some_random_int = random_int()

        # act
        # assert
        self.assertEqual(
            right_match_0,
            right_match_1,
            "The given Right-objects contain the same value, so they shoud be considered Equal",
        )
        self.assertNotEqual(
            right_match_0,
            right_diff,
            # pylint: disable=line-too-long
            "The given Right-objects contain different values, so they shoud be considered Not Equal",
        )
        self.assertNotEqual(
            left_match_0, right_match_0, "Left should never match a Right"
        )
        self.assertEqual(
            left_match_0,
            left_match_1,
            "The given Left-objects contain the same value, so they shoud be considered Equal",
        )
        self.assertNotEqual(
            left_match_0,
            left_diff,
            # pylint: disable=line-too-long
            "The given Left-objects contain different values, so they shoud be considered Not Equal",
        )
        self.assertNotEqual(
            some_random_int,
            Either.pure(some_random_int),
            # pylint: disable=line-too-long
            "Comparison between Right and non-Either should always return False",
        )
        self.assertNotEqual(
            some_random_int,
            left(some_random_int),
            # pylint: disable=line-too-long
            "Comparison between Left and non-Either should always return False",
        )

    def test_creation_of_either_with_right_returns_expected_results(self):
        # arrange
        some_random_value = random_int()

        right_initializers: List[Callable[[int], Either[str, int]]] = [
            Right,
            right,
            pure,
        ]

        # act
        results: List[Either[str, int]] = list(
            map(lambda fn: fn(some_random_value), right_initializers)
        )

        # assert
        right_class, right_fn, right_pure = results

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
        some_random_left_value = random_str()

        left_initializers: List[Callable[[str], Either[str, int]]] = [Left, left]

        # act
        results: List[Either[str, int]] = list(
            map(lambda fn: fn(some_random_left_value), left_initializers)
        )

        # assert
        left_class_of, left_fn_of = results

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

        some_right: Either[str, int] = pure(some_value)
        some_left: Either[str, int] = left(some_left_value)

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
            either(lambda _: -1, _identity, right_result),
            "Calling `fmap` on Right should return Right with the mapping applied to its value",
        )
        self.assertEqual(
            -1,
            either(lambda _: -1, _identity, left_result),
            "Calling `fmap` on Left should successfully return Left",
        )

    def test_map_left_returns_expected_results(self):
        # arrange
        some_value = random_str()

        some_left_value = random_int()
        some_value_sq = _square(some_left_value)

        some_right: Either[int, str] = pure(some_value)
        some_left: Either[int, str] = left(some_left_value)

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
            either(_identity, lambda _: -1, left_result),
            "Calling `map_left` on Left should return Left with the mapping applied to its value",
        )
        self.assertEqual(
            -1,
            either(_identity, lambda _: -1, right_result),
            "Calling `map_left` on Right should successfully return Right",
        )

    def test_bind_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_right: Either[str, int] = pure(some_value)

        either_right = _m_square(some_value)
        either_left = _m_fail(some_value)

        # act
        right_bind_right_result = some_right.bind(_m_square)
        right_bind_left_result = some_right.bind(_m_fail)
        left_bind_right_result = either_left.bind(_m_square)

        with pytest.raises(ArgumentTypeError) as invalid_method_error:

            def some_function_not_returning_either(value):
                return value

            some_right.bind(some_function_not_returning_either)

        # assert
        self.assertEqual(
            either_right,
            right_bind_right_result,
            "Calling `bind` on Right returns an Either, specifically Right for this test case",
        )
        self.assertIsInstance(
            right_bind_left_result,
            Left,
            "Calling `bind` on Right returns an Either, specifically Left for this test case",
        )
        self.assertEqual(
            either_left,
            left_bind_right_result,
            "Calling `bind` on Left returns the same Left",
        )
        self.assertTrue(
            invalid_method_error.errisinstance(ArgumentTypeError),
            # pylint: disable=line-too-long
            "Calling `bind` with function that doesn't return Either should throw an ArgumentTypeError",
        )

    def test_rights_and_lefts_return_expected_results(self):
        # arrange
        right_values = unique_ints()

        left_values = [random_str(), random_str()]

        some_rights: List[Either[str, int]] = list(map(right, right_values))  # type: ignore
        some_lefts: List[Either[str, int]] = list(map(left, left_values))  # type: ignore

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

        some_right: Either[int, str] = Either.pure(some_value)
        some_left: Either[int, str] = left(some_left_value)

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

    def test_chain_returns_expected_results(self):
        # arrange
        some_value = random_int()
        some_value_2 = random_int()

        some_left_value = random_str()

        some_right: Either[str, int] = Either.pure(some_value)
        some_right_2: Either[str, int] = Either.pure(some_value_2)
        some_left: Either[str, int] = left(some_left_value)

        # act
        right_result = some_right.chain(some_right_2)
        left_result = some_left.chain(some_right_2)

        # assert
        self.assertEqual(
            some_right_2,
            right_result,
            "Chaining Right with Right should return the latter Right",
        )
        self.assertEqual(
            some_left,
            left_result,
            "Chaining Left with Right should return unaltered Left",
        )

    def test_discard_returns_expected_results(self):
        # arrange
        some_right: Either[str, int] = Either.pure(random_int())
        some_left: Either[str, int] = left(random_str())

        # act
        right_result = some_right.discard(_m_square)
        left_result = some_left.discard(_m_square)

        # assert
        self.assertEqual(
            some_right,
            right_result,
            "Calling `discard` on Right will return the same Right",
        )
        self.assertEqual(
            some_left,
            left_result,
            "Calling `discard` on Left will return the same Left",
        )

    def test_either_returns_expected_results(self):
        # arrange
        some_value = random_int()
        some_left_value = random_str()

        some_right: Either[str, int] = Either.pure(some_value)
        some_left: Either[str, int] = left(some_left_value)

        # act
        # assert
        self.assertEqual(
            -1,
            some_left.either(lambda _: -1, _identity),
            "Calling `either` with id-function on Left returns fallback value",
        )
        self.assertEqual(
            1,
            some_left.either(
                lambda value: 1 if value == some_left_value else -1, _identity
            ),
            "Left side of function of `either` is called with Left value",
        )
        self.assertEqual(
            some_value,
            some_right.either(lambda _: -1, _identity),
            "Calling `either` with id-function on Right returns its value",
        )

    def test_to_maybe_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_right: Either[str, int] = Either.pure(some_value)
        some_left: Either[str, int] = left(random_str())

        # act
        right_result = some_right.to_maybe()
        left_result = some_left.to_maybe()

        # assert
        self.assertEqual(
            some_value,
            right_result.maybe(-1, _identity),
            "Calling `to_maybe` on Right should return Just containing its value",
        )
        self.assertEqual(
            nothing,
            left_result,
            "Calling `to_maybe` on Left should return `nothing`",
        )

    def test_to_optional_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_right: Either[str, int] = Either.pure(some_value)
        some_left: Either[str, int] = left(random_str())

        # act
        right_result = some_right.to_optional()
        left_result = some_left.to_optional()

        # assert
        self.assertEqual(
            some_value,
            right_result,
            "Calling `to_optional` on Right should return its raw value",
        )
        self.assertIsNone(
            left_result,
            "Calling `to_optional` on Left should return None",
        )

    def test_to_str(self):
        # arrange
        some_value = random_int()
        some_left_value = random_str()

        some_right: Either[str, int] = Either.pure(some_value)
        some_left: Either[str, int] = left(some_left_value)

        # act
        right_result = str(some_right)
        left_result = str(some_left)

        # assert
        self.assertTrue(
            str(some_value) in right_result,
            "Stringified Right should contain its value",
        )
        self.assertTrue(
            str(some_left_value) in left_result,
            "Stringified Left should contain its value",
        )

    def test_more_specific_type_is_allowed(self):
        # arrange
        some_value = random_int()

        def this_triggers_mypy_incompatible_return_value_when_types_not_covariant(  # pylint: disable=duplicate-code
            value: int,
        ) -> Either[None, BaseClass]:
            subclassed_value = SubClass(value)

            none_or_subclassed_value: Either[None, SubClass] = Either.pure(
                subclassed_value
            )

            return none_or_subclassed_value

        # act
        result = (
            this_triggers_mypy_incompatible_return_value_when_types_not_covariant(
                some_value
            )
            .fmap(lambda sc: sc.value)
            .if_left(-1)
        )

        # assert
        self.assertTrue(
            some_value == result,
            "Result should equal the generated value contained in the Either",
        )
