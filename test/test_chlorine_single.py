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


def run_test(test_dir):
    test_path = path_join(chlorine_single_test_dir, test_dir)

    expected_file = open(path_join(test_path, "result.json"))
    expected = json.load(expected_file)

    modules = get_modules_from_dir(path_join(test_path, "source"))
    actual = json.loads(chlorine_single_repo(modules).json())

    assert expected == actual


def test_simple_1():
    run_test("simple_test_1")


def test_simple_2():
    run_test("simple_test_2")


def test_simple_3():
    run_test("simple_test_3")


def test_multi_file():
    run_test("multi_file")


def test_external_1():
    run_test("external_test_1")
