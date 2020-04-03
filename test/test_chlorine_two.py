"""Module containing tests for two-repo mode of the Chlorine algorithm."""

from os.path import join as path_join
import json

from test import test_repo1_dir, test_repo2_dir, chlorine_double_test_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.chlorine.chlorine import chlorine_two_repos


def test_chlorine_two_not_none():
    """Check if two-repo mode of Chlorine returns non-empty result."""
    modules1 = get_modules_from_dir(test_repo1_dir)
    assert modules1

    modules2 = get_modules_from_dir(test_repo2_dir)
    assert modules2

    result = chlorine_two_repos(modules1, modules2)

    assert result
    assert result.clones


def test_simple_test_1():
    test_path = path_join(chlorine_double_test_dir, "simple_test_1")

    expected_file = open(path_join(test_path, "result.json"))
    expected = json.load(expected_file)

    modules1 = get_modules_from_dir(path_join(test_path, "source1"))
    modules2 = get_modules_from_dir(path_join(test_path, "source2"))
    actual = json.loads(chlorine_two_repos(modules1, modules2).json())

    assert expected == actual
