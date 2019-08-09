"""Module containing tests for two-repo mode of the Chlorine algorithm."""

from . import test_repo1_dir, test_repo2_dir
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
