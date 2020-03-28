"""Module containing tests for single-repo mode of the Chlorine algorithm."""

from os.path import join as path_join
import json

from test import test_repo1_dir, chlorine_single_test_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.chlorine.chlorine import chlorine_single_repo


def test_chlorine_single_not_none():
    """Check if single-repo mode of Chlorine returns non-empty result."""
    dir = test_repo1_dir
    modules = get_modules_from_dir(test_repo1_dir)

    assert modules

    result = chlorine_single_repo(modules)

    assert result
    assert result.clones


def test_simple_test_1():
    test_path = path_join(chlorine_single_test_dir, "simple_test_1")

    expected_file = open(path_join(test_path, "result.json"))
    expected = json.load(expected_file)

    modules = get_modules_from_dir(path_join(test_path, "source"))
    actual = json.loads(chlorine_single_repo(modules).json())

    assert expected == actual
