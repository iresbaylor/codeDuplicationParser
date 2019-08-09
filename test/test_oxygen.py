"""Module containing tests for the Oxygen algorithm (single-repo only)."""

from . import test_repo1_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.algorithms.oxygen.oxygen import oxygen


def test_oxygen_not_none():
    modules = get_modules_from_dir(test_repo1_dir)

    assert modules

    result = oxygen(modules)

    assert result
    assert result.clones
