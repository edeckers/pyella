# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import math
import unittest
from argparse import ArgumentTypeError

import pytest

from pyella.maybe import Just, Maybe, Nothing, maybe, nothing, of, pure
from pyella.shared import _identity
from tests.fixtures import is_list_instance_of, random_int, random_str, unique_ints


def _square(value: int) -> int:
    return int(math.pow(value, 2))


def _m_square(value: int) -> Just[int]:
    return Maybe.pure(value).fmap(_square)


# pylint: disable=unused-argument
def _m_fail(value: int) -> Maybe[int]:
    return nothing


class TestMaybe(unittest.TestCase):
    def test_maybe_objects_compare_correctly(self):
        # arrange
        value_match, value_diff = unique_ints(sample_size=2)

        some_random_int = random_int()

        just_match_0 = Just(value_match)
        just_match_1 = Just(value_match)
        just_diff = Just(value_diff)

        nothing_1: Nothing = Nothing()

        # act
        # assert
        self.assertEqual(
            just_match_0,
            just_match_1,
            "The given Just-objects contain the same value, so they shoud be considered Equal",
        )
        self.assertNotEqual(
            just_match_0,
            just_diff,
            # pylint: disable=line-too-long
            "The given Just-objects contain different values, so they shoud be considered Not Equal",
        )
        self.assertNotEqual(nothing, just_match_0, "Nothing should never match a Just")
        self.assertEqual(nothing, nothing_1, "Nothing always matches Nothing")
        self.assertNotEqual(
            some_random_int,
            Maybe.pure(some_random_int),
            # pylint: disable=line-too-long
            "Comparison between Just and non-Maybe should always return False",
        )
        self.assertNotEqual(
            some_random_int,
            nothing,
            # pylint: disable=line-too-long
            "Comparison between Nothing and non-Maybe should always return False",
        )

    def test_creation_of_maybe_with_value_returns_just(self):
        # arrange
        # act
        some_value = random_str()
        results = list(map(lambda fn: fn(some_value), [Maybe.of, of, pure]))
        just_m_of, just_of, just_pure = results

        # assert
        self.assertEqual(
            just_m_of,
            just_of,
            "The methods `Maybe.of`, `of` and `pure` must yield the same results",
        )
        self.assertEqual(
            just_of,
            just_pure,
            "The methods `Maybe.of`, `of` and `pure` must yield the same results",
        )
        self.assertTrue(
            is_list_instance_of(results, Just),
            "All values should be contained successully",
        )

    def test_creation_of_maybe_with_none_returns_nothing(self):
        # arrange
        # act
        results = list(map(lambda fn: fn(None), [Maybe.of, of, pure]))
        nothing_m_of, nothing_of, nothing_pure = results

        # assert
        self.assertEqual(
            nothing_m_of,
            nothing_of,
            "The methods `Maybe.of`, `of` and `pure` must yield the same results",
        )
        self.assertEqual(
            nothing_of,
            nothing_pure,
            "The methods `Maybe.of`, `of` and `pure` must yield the same results",
        )
        self.assertTrue(
            is_list_instance_of(results, Nothing),
            "All values should be contained successully",
        )

    def test_built_in_falsy_objects_other_than_none_return_just(self):
        # arrange
        # act
        # https://docs.python.org/3/library/stdtypes.html#truth-value-testing
        results = list(map(Maybe.of, [0, 0.0, [], (), {}, "", False]))

        # assert
        self.assertTrue(
            is_list_instance_of(results, Just),
            "All values should be contained successully",
        )

    def test_fmap_returns_expected_results(self):
        # arrange
        some_value = random_int()
        some_value_sq = _square(some_value)

        # act
        just_result = pure(some_value).fmap(_square)
        nothing_result = nothing.fmap(_square)

        # assert
        self.assertEqual(
            some_value_sq,
            maybe(-1, _identity, just_result),
            "Calling `fmap` on Just should return Just with the mapping applied to its value",
        )
        self.assertEqual(
            nothing,
            nothing_result,
            "Calling `fmap` on Nothing should successfully return Nothing",
        )

    def test_bind_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_just = pure(some_value)

        expected_just_success = _m_square(some_value)
        expected_just_failure = _m_fail(some_value)

        # act
        just_success_result = some_just.bind(_m_square)
        just_fail_result = some_just.bind(_m_fail)
        nothing_result = nothing.bind(_m_square)

        with pytest.raises(ArgumentTypeError) as invalid_method_error:

            def some_function_not_returning_either(value):
                return value

            some_just.bind(some_function_not_returning_either)

        # assert
        self.assertIsInstance(
            expected_just_success,
            Just,
            "Calling `bind` on Just returns a Maybe, specifically Just for this test case",
        )
        self.assertEqual(
            expected_just_success,
            just_success_result,
            "Calling `bind` on Just returns a Maybe, specifically Just for this test case",
        )
        self.assertIsInstance(
            expected_just_failure,
            Nothing,
            "Calling `bind` on Just returns a Maybe, specifically Nothing for this test case",
        )
        self.assertEqual(
            expected_just_failure,
            just_fail_result,
            "Calling `bind` on Just returns a Maybe, specifically Nothing for this test case",
        )
        self.assertEqual(
            nothing,
            nothing_result,
            "Calling `bind` on Nothing should successfully return Nothing",
        )
        self.assertTrue(
            invalid_method_error.errisinstance(ArgumentTypeError),
            # pylint: disable=line-too-long
            "Calling `bind` with function that doesn't return Maybe should throw an ArgumentTypeError",
        )

    def test_is_nothing_returns_expected_results(self):
        # arrange
        some_just = pure(random_int())

        # act
        # assert
        self.assertTrue(
            nothing.is_nothing(),
            "Calling `is_nothing` on Nothing returns True",
        )
        self.assertFalse(
            some_just.is_nothing(),
            "Calling `is_nothing` on Just returns False",
        )

    def test_maybe_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_just = pure(some_value)

        # act
        # assert
        self.assertEqual(
            -1,
            nothing.maybe(-1, _identity),
            "Calling `maybe` with id-function on Nothing returns fallback value",
        )
        self.assertEqual(
            some_value,
            some_just.maybe(-1, _identity),
            "Calling `maybe` with id-function on Just returns its value",
        )

    def test_from_maybe_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_just = pure(some_value)

        # act
        # assert
        self.assertEqual(
            -1,
            nothing.from_maybe(-1),
            "Calling `from_maybe` on Nothing returns fallback value",
        )
        self.assertEqual(
            some_value,
            some_just.from_maybe(-1),
            "Calling `from_maybe` on Just returns its value",
        )

    def test_replace_returns_expected_results(self):
        # arrange
        some_value = random_str()
        some_value_2 = random_int()

        some_just = Maybe.pure(some_value)

        # act
        just_result = some_just.replace(some_value_2)
        nothing_result = nothing.replace(some_value_2)

        # assert
        self.assertIsInstance(
            nothing_result,
            Nothing,
            "Calling `replace` on Nothing should return Nothing",
        )
        self.assertEqual(
            some_value_2,
            just_result.maybe(-1, _identity),
            "Calling `replace` on Just should successfully return Just with new value",
        )

    def test_to_optional_returns_expected_results(self):
        # arrange
        some_value = random_int()

        some_just = Maybe.pure(some_value)

        # act
        just_result = some_just.to_optional()
        nothing_result = nothing.to_optional()

        # assert
        self.assertIsNone(
            nothing_result,
            "Calling `to_optional` on Nothing should return None",
        )
        self.assertEqual(
            some_value,
            just_result,
            "Calling `to_optional` on Just should successfully return its raw value",
        )

    def test_to_str(self):
        # arrange
        some_value = random_int()

        some_just = Maybe.pure(some_value)

        # act
        just_result = str(some_just)
        nothing_result = str(nothing)

        # assert
        self.assertEqual(
            "Nothing",
            nothing_result,
            "Stringified Nothing should always return 'Nothing'",
        )
        self.assertTrue(
            str(some_value) in just_result,
            "Stringified Just should contain its value",
        )
