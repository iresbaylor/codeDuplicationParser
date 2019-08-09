"""Module containing tests for single-repo mode of the Chlorine algorithm."""

from . import test_repo1_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.chlorine.chlorine import chlorine_single_repo


def test_chlorine_single_not_none():
    """Check if single-repo mode of Chlorine returns non-empty result."""
    modules = get_modules_from_dir(test_repo1_dir)

    assert modules

    result = chlorine_single_repo(modules)

    assert result
    assert result.clones
