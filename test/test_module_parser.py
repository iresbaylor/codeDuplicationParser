from os.path import dirname, join as path_join
from test import __file__ as tests_dir_path
from engine.preprocessing.module_parser import get_modules_from_dir
from engine.nodes.tree import TreeNode


def test_get_modules():
    modules = get_modules_from_dir(
        path_join(dirname(tests_dir_path), "repos/CodeDuplicateTest1"))

    assert isinstance(modules, list)
    assert len(modules) > 0

    for m in modules:
        assert isinstance(m, list)

        for n in m:
            assert isinstance(n, TreeNode)
