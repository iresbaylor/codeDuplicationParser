"""Module containing tests for the Oxygen algorithm (single-repo only)."""

from os.path import join as path_join
import json

from test import test_repo1_dir, oxygen_test_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.oxygen.oxygen import oxygen


def test_oxygen_not_none():
    """Check if running Oxygen on a valid repo returns a non-empty result."""
    modules = get_modules_from_dir(test_repo1_dir)

    assert modules

    result = oxygen(modules)

    assert result
    assert result.clones


def test_simple_1():
    test_path = path_join(oxygen_test_dir, "simple_test_1")

    expected_file = open(path_join(test_path, "result.json"))
    expected = json.load(expected_file)

    modules = get_modules_from_dir(path_join(test_path, "source1"))
    actual = json.loads(oxygen(modules).json())

    assert expected == actual
