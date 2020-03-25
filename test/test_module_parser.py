"""Module containing unit tests for the module parser."""

from test import test_repo1_dir
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.nodes.tree import TreeNode


def test_get_modules():
    """Check if any modules are parsed from a valid directory. Check types."""
    modules = get_modules_from_dir(test_repo1_dir)

    assert isinstance(modules, list)
    assert len(modules) > 0

    for m in modules:
        assert isinstance(m, list)

        for n in m:
            assert isinstance(n, TreeNode)
